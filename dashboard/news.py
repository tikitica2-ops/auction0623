import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any

# Mock news dataset for fallback cache (Safe Fallback)
MOCK_NEWS = [
    {
        "title": "서울 아파트 낙찰가율 90% 돌파... 수도권 경매 열기 확산",
        "link": "https://news.naver.com",
        "press": "AntiG 경매경제"
    },
    {
        "title": "대항력 있는 임차인 조심... 빌라 경매 입찰 시 권리분석 핵심포인트",
        "link": "https://news.naver.com",
        "press": "법률경매뉴스"
    },
    {
        "title": "상가 경매 시장 양극화 지속... 유치권 신고 물건 입찰 시 주의사항",
        "link": "https://news.naver.com",
        "press": "경매플래너"
    },
    {
        "title": "민사집행법 개정안 발의... 법원 경매 절차 대금 납부 방식 다양화 추진",
        "link": "https://news.naver.com",
        "press": "국가법률일보"
    },
    {
        "title": "지방 토지 경매 매각가율 하락세... 실수요자 위주 소액 입찰 증가",
        "link": "https://news.naver.com",
        "press": "부동산메일"
    }
]

def fetch_auction_news(limit: int = 5) -> List[Dict[str, str]]:
    """
    Scrapes latest real estate auction news from Naver News Search.
    If it fails due to network or markup changes, falls back to pre-recorded mock news.
    """
    url = "https://search.naver.com/search.naver?where=news&query=부동산+경매&sm=tab_opt&sort=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return MOCK_NEWS[:limit]
            
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select(".news_area")
        
        if not articles:
            return MOCK_NEWS[:limit]
            
        news_list = []
        for article in articles[:limit]:
            # Title & Link
            title_el = article.select_one(".news_tit")
            if not title_el:
                continue
            title = title_el.get_text().strip()
            link = title_el.get("href")
            
            # Press Info
            press_el = article.select_one(".info.press")
            press = press_el.get_text().strip() if press_el else "부동산 경매 피드"
            # Remove "선정" or other extra text if present
            press = press.replace("언론사 선정", "").strip()
            
            news_list.append({
                "title": title,
                "link": link,
                "press": press
            })
            
        if len(news_list) == 0:
            return MOCK_NEWS[:limit]
            
        return news_list
        
    except Exception as e:
        print(f"Error fetching news (falling back to mock news): {e}")
        return MOCK_NEWS[:limit]

if __name__ == "__main__":
    # Test news fetch
    news = fetch_auction_news(3)
    for n in news:
        print(f"[{n['press']}] {n['title']} -> {n['link']}")
