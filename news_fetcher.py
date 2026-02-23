import feedparser

# Feeds defined by the user
FEEDS = {
    "main": "https://dailycoffeenews.com/feed/",
    "sub": "https://news.google.com/rss/search?q=%E3%82%B9%E3%83%9A%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%86%E3%82%A3%E3%82%B3%E3%83%BC%E3%83%92%E3%83%BC+OR+%E3%82%B3%E3%83%BC%E3%83%92%E3%83%BC%E5%B8%82%E5%A0%B4&hl=ja&gl=JP&ceid=JP:ja"
}

def fetch_latest_news():
    """
    Fetches news and categorizes them into 'main' and 'sub'.
    Returns a dict with 'main' and 'sub' lists of articles.
    """
    results = {"main": [], "sub": []}
    
    for category, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            # Fetch generously, we will limit the count in main.py
            for entry in feed.entries[:10]:
                title = entry.get('title', '')
                link = entry.get('link', '')
                summary = entry.get('summary', '')
                if not summary and 'content' in entry:
                    summary = entry.content[0].value
                
                if link:
                    results[category].append({
                        'title': title,
                        'link': link,
                        'summary': summary,
                        'category': category,
                        'source': feed.feed.title if hasattr(feed.feed, 'title') else url
                    })
        except Exception as e:
            print(f"Error fetching {category} feed ({url}): {e}")
            
    return results
