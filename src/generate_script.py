import os
import random
import requests

def create_script(topics):
    """
    Gemini APIを使用して、取得したニュースから「やわらかライフスタイル型」のラジオ台本を生成します。
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")
    
    # 取得した全ニュースをリスト化してプロンプトに渡す
    topics_list_str = "\n".join([f"- {t['keyword']}: {t['news_context']}" for t in topics])
    
    prompt = f"""
あなたは、「朝のコーヒーのお供に。ほっと一息つける世間の話題と豆知識」をコンセプトにした
Podcast番組『おはようトリビア・カフェ』のパーソナリティです。
優しくて落ち着いた、少し砕けたトーンで話します。

【本日のニューストピック一覧】
{topics_list_str}

【指示】
上記のトピック一覧の中から、スポーツ（W杯など）やエンタメなど、リスナーが朝からワクワクするような、または「へぇ〜！」と声が出るような最も面白そうなトピックを1つ選んでください。
選んだトピックに関連する「ゆるい雑学や豆知識」を1つ交えて、約2〜3分（文字数で600〜800文字程度）で話せるラジオの台本を作成してください。

【構成のルール】
1. オープニング（挨拶、天気の話題や季節の挨拶など、リラックスした入り）
2. ニュースの紹介（「さて、今日世間で話題になっているのは〜」という感じで、硬くならずに）
3. 雑学の紹介（そのニュースに関連する、知っていると少し楽しい豆知識）
4. エンディング（今日も良い一日を、という前向きな締め）

【出力形式の絶対ルール】
必ず以下のフォーマット通りに出力し、それ以外の前置きや解説は一切含めないでください。
「台本：」以降の文章は、そのまま音声合成エンジン（TTS）に流し込むため、ト書き（笑など）は入れずセリフのみにしてください。

キーワード：[選んだトピックのキーワードを短く記載]
台本：
[ここから台本の本文を開始]
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts":[{"text": prompt}]}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Gemini API Error: {response.status_code} - {response.text}")
        
    result = response.json()
    output_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
    
    # 出力からキーワードと台本を抽出
    keyword = "本日のトレンド"
    script_text = output_text
    
    if "台本：" in output_text:
        parts = output_text.split("台本：")
        keyword_part = parts[0].replace("キーワード：", "").strip()
        if keyword_part:
            keyword = keyword_part
        script_text = parts[1].strip()
    
    return keyword, script_text

if __name__ == "__main__":
    # テスト用
    sample_topics = [{'keyword': 'コーヒー', 'news_context': '新作のカフェラテが大ヒット'}]
    try:
        keyword, script = create_script(sample_topics)
        print(f"Keyword: {keyword}")
        print("Script:")
        print(script)
    except Exception as e:
        print(f"Error: {e}")
