import os
import google.generativeai as genai
import random

def create_script(topics):
    """
    Gemini APIを使用して、取得したニュースから「やわらかライフスタイル型」のラジオ台本を生成します。
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")
    
    genai.configure(api_key=api_key)
    
    #  Gemini 1.5 Flash (高速・低コストモデル) を使用
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # ピックアップするニュースをランダムに1〜2つ選ぶ
    selected_topic = random.choice(topics)
    keyword = selected_topic['keyword']
    context = selected_topic['news_context']
    
    prompt = f"""
あなたは、「朝のコーヒーのお供に。ほっと一息つける世間の話題と豆知識」をコンセプトにした
Podcast番組『おはようトリビア・カフェ』のパーソナリティです。
優しくて落ち着いた、少し砕けたトーンで話します。

本日の世間の注目キーワード: {keyword}
関連するニュース: {context}

このキーワードに関する「へぇ〜！」と声が出るような、ゆるい雑学や豆知識を1つ交えて、
約2〜3分（文字数で600〜800文字程度）で話せるラジオの台本を作成してください。

【構成のルール】
1. オープニング（挨拶、天気の話題や季節の挨拶など、リラックスした入り）
2. ニュースの紹介（「さて、今日世間で話題になっているのは〜」という感じで、硬くならずに）
3. 雑学の紹介（そのニュースに関連する、知っていると少し楽しい豆知識）
4. エンディング（今日も良い一日を、という前向きな締め）

【出力のルール】
- 余計な説明書き（「オープニング:」などの見出しや、(笑)などのト書き）は一切入れず、
  そのまま音声合成エンジン（TTS）に流し込んで自然に聞こえる「セリフのみ」を出力してください。
- 記号（！や？など）は自然な間を作るのに役立ちますが、過剰にならないようにしてください。
"""
    
    response = model.generate_content(prompt)
    
    script_text = response.text.strip()
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
