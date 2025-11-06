# 환경변수 호출 설정파일

import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로딩

KIS_ENV = os.getenv("KIS_ENV", "mock")
KIS_BASE_REAL = os.getenv("KIS_BASE_REAL")
KIS_BASE_MOCK = os.getenv("KIS_BASE_MOCK")
KIS_BASE = os.getenv("KIS_BASE_REAL") if KIS_ENV == "real" else os.getenv("KIS_BASE_MOCK")


APP_KEY= os.getenv("KIS_APP_KEY")
APP_SECRET = os.getenv("KIS_APP_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")