import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def get_trending_topics():
    """
    Yahooニュースの主要トピックスRSSから、本日のニュースを取得します。
    """
    url = 'https://news.yahoo.co.jp/rss/topics/top-picks.xml'
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # XMLのパース
        root = ET.fromstring(response.content)
        
        trends = []
        for item in root.findall('.//item'):
            title = item.find('title').text
            description = item.find('description').text if item.find('description') is not None else ""
            
            trends.append({
                'keyword': title,
                'news_context': description
            })
            
        return trends[:5]  # トップ5件を返す
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

if __name__ == "__main__":
    topics = get_trending_topics()
    for t in topics:
        print(t)
