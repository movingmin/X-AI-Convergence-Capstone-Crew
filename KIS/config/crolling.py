import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def get_market_top_1000(pages: int = 20) -> pd.DataFrame:
    """
    네이버 금융에서 KOSPI 시가총액 상위 종목을 크롤링하여 DataFrame으로 반환
    KIS 가상환경에 는 BeautifulSoup가 그뭐냐 의존성 패키지가 아니므로 사용 전에 install하길 바람
    $ uv pip install beautifulsoup4

    Args:
        pages (int): 크롤링할 페이지 수 (한 페이지당 50종목)

    Returns:
        pd.DataFrame: 종목명, 종목코드, 시가총액 포함된 데이터프레임
    """
    base_url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page=" # sosok=0은 코스피, sosok=1은 코스닥 크롤링
    headers = {"User-Agent": "Mozilla/5.0"}  # 네이버 차단 회피용 UA
    result = []

    for page in range(1, pages + 1):
        url = f"{base_url}{page}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # HTML 테이블 파싱
        table = soup.select_one("table.type_2")
        rows = table.select("tbody tr")

        for row in rows:
            cols = row.select("td")
            if len(cols) < 2:
                continue  # 빈 행 skip

            link = cols[1].select_one("a")
            if not link:
                continue

            name = link.text.strip()  # 종목명
            href = link.get("href")
            code = href.split("code=")[-1]  # 종목코드 추출

            # 시가총액 (숫자로 변환 시도)
            market_cap = cols[6].text.strip().replace(",", "")
            market_cap = int(market_cap) if market_cap.isdigit() else None

            result.append({
                "종목명": name,
                "종목코드": code,
                "시가총액": market_cap
            })

    return pd.DataFrame(result)

def convert_to_json_map(df: pd.DataFrame) -> dict:
    """
    DataFrame을 JSON 형태의 딕셔너리로 변환

    {"종목명": {"code": "종목코드", "market": "J"}}
    시장 구분은 현재 KOSPI 기준으로 "J" 고정

    Args:
        df (pd.DataFrame): 크롤링 결과 DataFrame

    Returns:
        dict: 변환된 JSON 구조 딕셔너리
    """
    result = {}
    for _, row in df.iterrows():
        name = row["종목명"]
        code = row["종목코드"]
        result[name] = {"code": code, "market": "U"}  # KOSPI는 market = J KOSDAQ은 market = U
    return result

# 실행 절차
if __name__ == "__main__":
    df = get_market_top_1000(pages=20)  # 시총 상위 1000 종목
    json_map = convert_to_json_map(df)

    # JSON 저장
    with open("stock_list.json", "w", encoding="utf-8") as f: # 파일이름기본값: stock_list.json
        json.dump(json_map, f, ensure_ascii=False, indent=2)

    print("✅ stock_list.json 생성 완료 (상위 시총 종목 기준)")
