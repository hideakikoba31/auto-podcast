import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def get_trending_topics():
    """
    Yahooニュースの主要トピックスRSSから、本日のニュースを取得します。
    """
    urls = [
        'https://news.yahoo.co.jp/rss/topics/sports.xml',          # スポーツ（W杯など）
        'https://news.yahoo.co.jp/rss/topics/entertainment.xml',   # エンタメ
        'https://news.yahoo.co.jp/rss/topics/top-picks.xml'        # 主要トピックス
    ]
    
    trends = []
    try:
        for url in urls:
            response = requests.get(url)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            # 各フィードから上位3件ずつ取得して多様性を確保
            for item in root.findall('.//item')[:3]:
                title = item.find('title').text
                description = item.find('description').text if item.find('description') is not None else ""
                
                trends.append({
                    'keyword': title,
                    'news_context': description
                })
                
        return trends
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

if __name__ == "__main__":
    topics = get_trending_topics()
    for t in topics:
        print(t)
