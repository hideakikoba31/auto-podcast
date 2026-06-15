import os
import sys
from datetime import datetime
import pytz

# srcディレクトリ内のモジュールをインポート
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fetch_news import get_trending_topics
from generate_script import create_script
from generate_audio import synthesize_speech
from mix_audio import mix_audio_with_bgm
from update_rss import add_episode_to_rss

def main():
    print("=== おはようトリビア・カフェ 自動生成プログラム開始 ===")
    
    # 1. ニュースの取得
    print("1. トレンドニュースを取得中...")
    topics = get_trending_topics()
    if not topics:
        print("エラー: トレンドの取得に失敗しました。終了します。")
        sys.exit(1)
        
    print("2. Gemini APIによる台本を生成中...")
    try:
        keyword, script = create_script(topics)
        print(f"-> 採用されたキーワード: {keyword}")
        print("【生成された台本】")
        print(script)
        print("------------------")
    except Exception as e:
        print(f"エラー: 台本の生成に失敗しました: {e}")
        sys.exit(1)

    # 3. 音声の生成
    print("3. Google Cloud TTSによる音声を生成中...")
    raw_audio_path = "assets/raw_audio.mp3"
    try:
        synthesize_speech(script, raw_audio_path)
    except Exception as e:
        print(f"エラー: 音声の生成に失敗しました: {e}")
        sys.exit(1)

    # 4. BGMとの合成
    print("4. 音声とBGMを合成中...")
    jst = pytz.timezone('Asia/Tokyo')
    now_str = datetime.now(jst).strftime('%Y%m%d')
    final_audio_path = f"assets/episodes/episode_{now_str}.mp3"
    bgm_path = "assets/ensolarado.mp3"
    
    try:
        mix_audio_with_bgm(raw_audio_path, bgm_path, final_audio_path)
    except Exception as e:
        print(f"エラー: 音声のミックスに失敗しました: {e}")
        sys.exit(1)

    # 5. RSSの更新
    print("5. RSSフィードを更新中...")
    title = f"{datetime.now(jst).strftime('%m月%d日')}の話題: {keyword}の豆知識"
    description = f"本日のトレンド「{keyword}」に関する雑学をお届けします。\n\n---\nAIパーソナリティによる自動生成Podcastです。"
    
    # ユーザーが確認しやすいようにテキストファイルとして保存しておく
    info_path = f"assets/episodes/episode_{now_str}_info.txt"
    try:
        with open(info_path, "w", encoding="utf-8") as f:
            f.write(f"【エピソードタイトル】\n{title}\n\n")
            f.write(f"【概要（説明文）】\n{description}\n\n")
            f.write(f"【読み上げ台本】\n{script}\n")
        print(f"-> エピソード情報を保存しました: {info_path}")
    except Exception as e:
        print(f"警告: エピソード情報の保存に失敗しました: {e}")

    # GitHubのパスに対応するためファイル名のみ渡す（update_rss.pyのロジックに依存）
    relative_audio_path = f"assets/episodes/episode_{now_str}.mp3"
    
    try:
        add_episode_to_rss(title, description, relative_audio_path, "feed.xml")
    except Exception as e:
        print(f"エラー: RSSの更新に失敗しました: {e}")
        sys.exit(1)
        
    print("=== すべての処理が完了しました！ ===")

if __name__ == "__main__":
    main()
