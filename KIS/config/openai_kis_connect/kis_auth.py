# 토큰 발급 API 호출 헬퍼

import requests
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from .config import KIS_BASE, APP_KEY, APP_SECRET

_cached_token: Optional[str] = None
_token_expiry: Optional[datetime] = None

def get_kis_token() -> Optional[str]:
    """
    메모리 캐시 방식으로 KIS access_token을 발급 또는 재사용합니다.

    Returns:
        Optional[str]: 유효한 access_token, 실패 시 None
    """
    global _cached_token, _token_expiry

    if _cached_token and _token_expiry and datetime.now() < _token_expiry:
        return _cached_token

    url = f"{KIS_BASE}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    payload: Dict[str, Any] = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        _cached_token = data.get("access_token")
        expires_in = data.get("expires_in",3600) # 기본 토큰 만료시간 3600초
        _token_expiry = datetime.now() + timedelta(seconds=int(expires_in) - 30)

        return _cached_token
    except Exception as e:
        print(f"[ERROR] 토큰 발급 실패: {e}")
        return None
