 # 프로젝트의 루트 디렉터리를 /으로 표기함
 ## 25.11.06 ai파트
 - /KIS/config/: LLM, KIS api 연동 및 교육 디렉터리
 - /KIS/config/pyproect.toml 기준으로 uv로 파이썬 가상환경 설정, 의존성 패키지 설치
 - /KIS/config/자동매매/ 디렉터리는 KIS 토큰 할당받아 보기 위한 테스트 디렉터리
 - **/.env 파일에 환경 변수(KIS key, 가상계좌번호, openai api key, TR_ID 등) 등록**
 - **KIS/config/openai_kis_connect/ 디렉터리에 툴 및 주요 호출 API 코딩**
    - openai_call.py: KIS app key, app secret을 통해 KIS 토큰 할당 및 openai 채팅 기능 구현(테스트 필요) *37번라인 하드코딩된것인지 확인해보고 수정필요*
    - get_price.py: 단일 시세 조회 api 툴
        - 시가총액 상위 1000개의 기업 크롤링(crolling.py)
        - 기업명, 종목 코드, 시장 구분 코드(유가증권, 코스닥 등) 나열된 데이터셋을 json파일로 제작(market_code.json)
        - LLM에게 입력된 데이터의 기업명을 통해 종목 코드를 뽑아서 get_price.py:36,37에 입력 예정
        