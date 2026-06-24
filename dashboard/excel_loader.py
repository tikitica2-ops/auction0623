import os
import pandas as pd
from typing import Dict, List, Any

def load_auction_excel() -> Dict[str, Any]:
    """
    Parses 'c:\\AI-Agent\\auction0623\\법원경매물건_14건.xlsx' using pandas.
    Classifies 3 predefined items as 'recommended' and the rest 11 items as 'general'.
    """
    filepath = r"c:\AI-Agent\auction0623\법원경매물건.xls"
    if not os.path.exists(filepath):
        for alt_name in ["법원경매물건.xlsx", "법원경매물건_14건.xlsx", "법원경매물건_14건 - 복사본.xlsx"]:
            alt_path = os.path.join(r"c:\AI-Agent\auction0623", alt_name)
            if os.path.exists(alt_path):
                filepath = alt_path
                break
        else:
            return {"recommended": [], "general": []}
        
    try:
        # Load excel file
        df = pd.read_excel(filepath)
        
        # Drop empty rows and non-data footer text row
        df_clean = df.dropna(subset=['사건번호'])
        # Filter out rows starting with '※'
        df_clean = df_clean[~df_clean['사건번호'].str.startswith('※', na=True)]
        
        # Convert to records list
        records = df_clean.to_dict(orient='records')
        
        # Predefined recommended 사건번호s
        recommended_cases = [
            '2024타경6190',   # 강남구 도곡동 도곡한신아파트
            '2024타경71157',  # 하남시 감이동 포웰시티푸르지오라포레
            '2025타경103783'  # 종로구 평창동 단독주택
        ]
        
        recommended_list = []
        general_list = []
        
        for r in records:
            case_no = str(r.get('사건번호', '')).strip()
            
            # Clean values for presentation
            appraisal = r.get('감정평가액(원)', 0)
            minimum_bid = r.get('최저매각가격(원)', 0)
            
            # Calculate discount percent
            discount = 0
            if pd.notna(appraisal) and appraisal > 0:
                discount = int(round((1 - (minimum_bid / appraisal)) * 100))
                
            r['discount_percent'] = discount
            
            # Formatted currencies
            r['appraisal_formatted'] = f"{appraisal:,.0f}원" if pd.notna(appraisal) else "미상"
            r['minimum_bid_formatted'] = f"{minimum_bid:,.0f}원" if pd.notna(minimum_bid) else "미상"
            
            # Classify
            is_rec = False
            for rec_case in recommended_cases:
                if rec_case in case_no:
                    is_rec = True
                    break
                    
            if is_rec:
                # Add recommendation reason
                if '2024타경6190' in case_no:
                    r['recommend_reason'] = "대한민국 최고 수준의 학군지이자 강남 도곡동 중심부 대단지 아파트. 1회 유찰되어 20% 메리트 확보."
                    r['recommend_tag'] = "강남 초입지"
                elif '2024타경71157' in case_no:
                    r['recommend_reason'] = "송파구 오륜동에 인접한 감일지구의 신축 준대형 아파트 단지. 2회 유찰로 감정가 대비 51%의 파격적인 가격 혜택."
                    r['recommend_tag'] = "반값 대단지"
                elif '2025타경103783' in case_no:
                    r['recommend_reason'] = "종로구 평창동 전통 고급 단독주택지. 661㎡(약 200평)의 넓은 대지 지분 일괄 매각으로, 3회 유찰되어 감정가 대비 48% 할인."
                    r['recommend_tag'] = "희소 고급주택"
                recommended_list.append(r)
            else:
                general_list.append(r)
                
        return {
            "recommended": recommended_list,
            "general": general_list
        }
    except Exception as e:
        import traceback
        with open(r"c:\AI-Agent\auction0623\excel_error.txt", "w", encoding="utf-8") as f:
            f.write(f"Error: {e}\n")
            f.write(traceback.format_exc())
        print(f"Error loading Excel file: {e}")
        return {"recommended": [], "general": []}
