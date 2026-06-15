import os
from feedgen.feed import FeedGenerator
import pytz
from datetime import datetime

# GitHub PagesのURLに置き換えてください
# 例: https://username.github.io/repository-name/
BASE_URL = "https://your-github-username.github.io/your-repo-name/"

def add_episode_to_rss(title, description, mp3_filename, feed_file="feed.xml"):
    """
    PodcastのRSSフィードを作成または更新し、新しいエピソードを追加します。
    """
    fg = FeedGenerator()
    fg.load_extension('podcast')
    
    # 既存のフィードがあれば読み込む (今回は簡易的に毎回新規作成ベースで追記するロジック、
    # 実際はxmlをパースするか、過去の履歴DBから生成し直すのが一般的です。
    # ここではシンプルにするため、feedgenの機能を使い毎回最新エピソード1件をパースではなく
    # 既存のフィードに新しいエントリを追加する形をとりますが、feedgenは追記が少し特殊です。
    # 実運用では、エピソードリストをJSON等で保存し、そこから全エピソードのRSSを毎回作り直すのが堅牢です。)
    
    # 今回は簡略化のため、常に新しいRSSとして最新数件を含めるような作りにするか、
    # 既存のfeed.xmlを読み込んでパースする実装が必要です。
    # 今回は「エピソードリストを保持するJSON（episodes.json）」からRSSを生成する方式にします。
    import json
    episodes_db = "episodes.json"
    
    episodes = []
    if os.path.exists(episodes_db):
        with open(episodes_db, "r", encoding="utf-8") as f:
            episodes = json.load(f)
            
    # 新しいエピソードを追加
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    
    # mp3のファイルサイズを取得
    file_size = os.path.getsize(mp3_filename) if os.path.exists(mp3_filename) else 0
    
    # GitHub Pages上のMP3のURL
    mp3_url = f"{BASE_URL}{mp3_filename}"

    new_ep = {
        "title": title,
        "description": description,
        "url": mp3_url,
        "file_size": file_size,
        "pub_date": now.strftime("%a, %d %b %Y %H:%M:%S %z"),
        "guid": f"{BASE_URL}episode/{now.strftime('%Y%md%H%M%S')}"
    }
    
    episodes.insert(0, new_ep) # 先頭に追加
    
    # 保存
    with open(episodes_db, "w", encoding="utf-8") as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)
        
    # RSSの生成
    fg.title('おはようトリビア・カフェ')
    fg.link(href=BASE_URL, rel='alternate')
    fg.description('朝のコーヒーのお供に。ほっと一息つける世間の話題と豆知識をお届けするポッドキャストです。')
    fg.language('ja')
    fg.podcast.itunes_category('Society & Culture')
    # fg.podcast.itunes_image(f"{BASE_URL}assets/cover.jpg") # カバー画像があれば設定
    
    for ep in episodes:
        fe = fg.add_entry()
        fe.id(ep["guid"])
        fe.title(ep["title"])
        fe.description(ep["description"])
        fe.enclosure(ep["url"], str(ep["file_size"]), 'audio/mpeg')
        fe.published(ep["pub_date"])
        
    fg.rss_file(feed_file)
    print(f"RSS feed updated: {feed_file}")
    
if __name__ == "__main__":
    add_episode_to_rss("テストエピソード", "これはテストです", "assets/episodes/test.mp3")
