from youtube_transcript_api import YouTubeTranscriptApi
import providers
import json
import re
from typing import List, Dict, Any

# Curated Video IDs & Fallback Cached summaries from the channel '김딸기' (@kimddalky)
CURATED_VIDEOS = {
    "dlssAA_Uyg4": {
        "title": "아슬아슬 진퇴양난 사면초가 주택",
        "channel": "김딸기",
        "summary": [
            "진입 도로가 협소하고 지적도상 맹지에 가까워 건축물 대장과 실질 통행 가능 도로 여부를 정밀 확인해야 합니다.",
            "주변 인프라가 미비하고 지형 경사도가 높아 향후 재매각 시 환금성(매도 편의성)이 크게 떨어질 우려가 있습니다.",
            "감정가 대비 유찰이 많이 진행되었더라도, 현장 임장을 통해 진입로의 불법 점유나 물리적 하자를 직접 파악해야 합니다."
        ],
        "keywords": ["#맹지진단", "#진입로분석", "#현장임장"]
    },
    "kHgEWe5OkPQ": {
        "title": "자전거로 바다3분 주변이 황량해서 무서운 180평집",
        "channel": "김딸기",
        "summary": [
            "바다와 인접하여 세컨하우스나 펜션 부지로 좋으나 주변 편의시설이 전무해 고립된 입지적 단점이 존재합니다.",
            "180평 대지의 넓은 면적 대비 가격 메리트가 있어 보이지만, 용도지역이 보전관리 혹은 계획관리지역인지 규제 분석이 우선입니다.",
            "바다 인근 외곽 토지는 시세 거품이 있을 수 있으므로 인근 최근 실거래 사례를 통해 냉정한 입찰가 산출이 중요합니다."
        ],
        "keywords": ["#세컨하우스", "#토지규제분석", "#실거래가대조"]
    },
    "PUJy4qkb_5k": {
        "title": "온천이나 금광이 터지지 않고선 말이 안되는 전원주택단지",
        "channel": "김딸기",
        "summary": [
            "시행사의 개발 중단으로 인해 진입로 포장, 상하수도, 전기 인입 등 필수 기반시설 공사가 미완성된 상태입니다.",
            "토지 낙찰 시 지분 매각이거나 제시외 건물이 포함되어 법정지상권 성립 가능성이 있는지 권리 분석을 마쳐야 합니다.",
            "단순한 분양 홍보 호재에 현혹되지 않고, 실제로 건축 행위 허가가 유효한지 관할 지자체에 확인해 보아야 합니다."
        ],
        "keywords": ["#전원주택지", "#기반시설하자", "#건축허가"]
    }
}

def get_video_list() -> List[Dict[str, str]]:
    """
    Returns the list of curated videos with titles and channels for dashboard preview.
    """
    video_list = []
    for vid, data in CURATED_VIDEOS.items():
        video_list.append({
            "video_id": vid,
            "title": data["title"],
            "channel": data["channel"]
        })
    return video_list

def get_youtube_summary(video_id: str) -> Dict[str, Any]:
    """
    Retrieves the transcript of the video and generates a summary using LLM.
    If transcript extraction or LLM call fails, falls back to pre-recorded mock summaries.
    """
    fallback_data = CURATED_VIDEOS.get(video_id)
    if not fallback_data:
        return {
            "video_id": video_id,
            "title": "알 수 없는 동영상",
            "channel": "김딸기",
            "summary": ["영상 정보를 가져올 수 없습니다."],
            "keywords": ["#경매"]
        }
        
    try:
        # Try to get transcript
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["ko"])
        full_text = " ".join([item["text"] for item in transcript_list])
        
        # Call LLM for summarization
        llm = providers.get_llm(temperature=0.0)
        
        system_prompt = (
            "당신은 부동산 경매 교육 동영상 분석 및 요약 전문가입니다.\n"
            "제공된 동영상 자막 텍스트를 분석하여 학습자를 위한 핵심 내용 요약을 작성해 주세요.\n\n"
            "다음 규칙을 반드시 지켜야 합니다:\n"
            "1. 3개의 한국어 완성형 문장으로 요약하여 JSON 리스트 형태로 반환할 것.\n"
            "2. 동영상 내용과 밀접한 연관이 있는 한국어 해시태그 3개를 JSON 리스트 형태로 추출할 것.\n"
            "3. 반드시 아래의 JSON 포맷 형식을 엄격히 지켜 응답해야 합니다. 다른 텍스트나 코드 마크업(```json 등)은 절대 섞지 마세요.\n\n"
            "JSON 출력 형식:\n"
            "{\n"
            "  \"summary\": [\n"
            "    \"핵심 요약 문장 1\",\n"
            "    \"핵심 요약 문장 2\",\n"
            "    \"핵심 요약 문장 3\"\n"
            "  ],\n"
            "  \"keywords\": [\n"
            "    \"#해시태그1\",\n"
            "    \"#해시태그2\",\n"
            "    \"#해시태그3\"\n"
            "  ]\n"
            "}"
        )
        
        user_prompt = f"동영상 자막:\n{full_text[:4000]}"
        
        response = llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        content = response.content.strip()
        
        # Clean potential markdown wrapping
        if content.startswith("```json"):
            content = content.split("```json", 1)[1]
        if content.endswith("```"):
            content = content.rsplit("```", 1)[0]
        content = content.strip()
        
        parsed_res = json.loads(content)
        
        return {
            "video_id": video_id,
            "title": fallback_data["title"],
            "channel": fallback_data["channel"],
            "summary": parsed_res.get("summary", fallback_data["summary"]),
            "keywords": parsed_res.get("keywords", fallback_data["keywords"])
        }
        
    except Exception as e:
        # Graceful fallback in case of no subtitles, network errors, or parser failures
        print(f"YouTube Summary Error (falling back to cache for {video_id}): {e}")
        res = fallback_data.copy()
        res["video_id"] = video_id
        return res
