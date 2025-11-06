"""KIS MCP 서버에서 단일 종목의 현재가를 조회하는 간단한 헬퍼 함수."""

from typing import Any, Dict
import os
import requests
from ..config import KIS_BASE
TR_ID = os.getenv("TR_ID_PRICE") # 단일 시세 조회 tr_id
url=f"{KIS_BASE}/uapi/domestic-stock/v1/quotations/inquire-price"


def get_price(token: str, appkey: str, appsecret: str, code: str = "005930", market_div_code: str = "J") -> Dict[str, Any]:
    """
    한국투자증권(KIS) MCP 현재가 조회 API를 호출해 응답 JSON을 반환한다.

    Args:
        token: `oauth2/tokenP`에서 발급받은 Bearer 토큰.
        appkey: KIS 애플리케이션 키.
        appsecret: KIS 애플리케이션 시크릿.
        code: 조회할 6자리 종목코드(기본값: 삼성전자 `005930`).

    Returns:
        dict: KIS API가 반환하는 JSON 응답(에러 정보 포함 가능).

    주의:
        - 모의/실전 환경에 따라 베이스 URL과 TR ID가 달라질 수 있으므로 문서를 확인할 것.
        - `fid_cond_mrkt_div_code`는 시장 구분 코드(J: 유가증권), 필요 시 다른 값으로 교체한다.
    """
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": appkey,
        "appsecret": appsecret,
        "tr_id": TR_ID,
    }
    params = {
        "fid_cond_mrkt_div_code": market_div_code,  # 시장 구분 (J=유가증권, U=코스닥 등)
        "fid_input_iscd": code,  # 조회 대상 종목코드
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
