import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def get_trending_topics():
    """
    Google Trendsの日本のRSSフィードから、本日のトレンドキーワードと関連ニュースを取得します。
    """
    url = 'https://trends.google.co.jp/trends/trendingsearches/daily/rss?geo=JP'
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # XMLのパース
        root = ET.fromstring(response.content)
        
        trends = []
        # namespace (ht) が含まれているため、find時に注意
        ns = {'ht': 'https://trends.google.co.jp/trends/trendingsearches/daily'}
        
        for item in root.findall('.//item'):
            title = item.find('title').text
            # 関連するニュースのタイトルも取得（より文脈をAIに持たせるため）
            news_title = ""
            news_item = item.find('ht:news_item', ns)
            if news_item is not None:
                news_item_title = news_item.find('ht:news_item_title', ns)
                if news_item_title is not None:
                    news_title = news_item_title.text
                    
            trends.append({
                'keyword': title,
                'news_context': news_title
            })
            
        return trends[:5]  # トップ5件を返す
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

if __name__ == "__main__":
    topics = get_trending_topics()
    for t in topics:
        print(t)
