import asyncio
from dashboard.news import fetch_auction_news
from dashboard.youtube import get_video_list, get_youtube_summary, CURATED_VIDEOS

async def load_dashboard_data(news_limit: int = 5):
    """
    Loads both Naver news feed and all YouTube video summaries in parallel
    using asyncio.to_thread to prevent blocking the Streamlit server thread.
    """
    # Fetch news in thread
    news_task = asyncio.to_thread(fetch_auction_news, limit=news_limit)
    
    # Fetch all video summaries in parallel threads
    video_ids = list(CURATED_VIDEOS.keys())
    youtube_tasks = [asyncio.to_thread(get_youtube_summary, vid) for vid in video_ids]
    
    # Run concurrently
    results = await asyncio.gather(news_task, *youtube_tasks)
    
    news_feed = results[0]
    youtube_summaries = results[1:]
    
    return {
        "news": news_feed,
        "youtube": youtube_summaries
    }

if __name__ == "__main__":
    # Smoke test of async loader
    import time
    start = time.time()
    data = asyncio.run(load_dashboard_data(3))
    end = time.time()
    
    print(f"Async loader completed in {end - start:.2f} seconds.")
    print(f"Fetched {len(data['news'])} news articles.")
    print(f"Fetched {len(data['youtube'])} YouTube summaries.")
