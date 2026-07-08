import feedparser
from urllib.parse import quote

def get_filtered_news(topic, start_date, end_date):
    search_query = f'{topic} after:{start_date} before:{end_date}'
    
    encoded_query = quote(search_query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    # Parse the RSS Feed
    feed = feedparser.parse(rss_url)
    
    print(f"--- Found {len(feed.entries)} articles for '{topic}' between {start_date} and {end_date} ---\n")
    
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        published = entry.published  # Timestamp string from the provider
        source = entry.source.text if hasattr(entry, 'source') else "Unknown Source"
        
        print(f"Title: {title}")
        print(f"Source: {source}")
        print(f"Published: {published}")
        print(f"Link: {link}")
        print("-" * 60)
