# AI 팀 전용 데이터·모델·LLM 가이드

## 우리가 맡을 서비스 경계
- **celery-worker / ai-processor**: 투자 시뮬레이션 연산, 위험 점수 계산, LLM 호출을 실행하는 메인 워커입니다. 고정 큐 이름(`ai_tasks`)을 사용하고, 작업별 시간 제한과 재시도 정책을 명시하세요.
- **celery-beat / scheduler**: 시세 수집, 리포트 생성, 모델 재학습 예약을 담당합니다. 모든 주기 작업은 `jobs.yaml`로 선언해 코드/스케줄을 한 곳에서 관리합니다.
- **etl-worker**: `open-trading-api`를 이용해 한국투자증권 데이터를 가져오는 컨테이너입니다. API 호출 실패 시 슬랙 알림을 보내고, 성공 로그는 MySQL/MinIO에 적재합니다.
- **minio**: 모델 아티팩트와 LLM 응답·리포트를 저장하는 스토리지. 버킷 정책(`reports`, `models`, `prompts`)을 분리해 접근 권한을 단계별로 제어합니다.
- **redis**: Celery 브로커 및 캐시. TTL을 사용해 LLM 응답 캐시를 관리하고, 장애 시 자동 복구 절차를 준비합니다.

## 필수 파이썬 스택
- **Python 3.13 + uv**: 모든 패키지 관리는 `uv` 기반으로 통일합니다. `pyproject.toml`에 `celery`, `openai`, `pandas`, `numpy`, `scikit-learn`, `tenacity` 등을 선언하고 `uv sync`로 설치하세요.
- **데이터 처리**: `pandas`로 시세/체결 데이터를 정리하고, 지표 계산은 `ta` 혹은 `vectorbt` 등 가벼운 라이브러리를 활용합니다.
- **모델 관리**: 기본 추천/위험 점수는 scikit-learn 혹은 LightGBM으로 구성하고, 모델 버전은 MLflow 없이도 `models/{timestamp}/model.pkl` 구조로 MinIO에 저장해 추적합니다.
- **구성 관리**: Pydantic `BaseSettings`로 API 키, 모델 파라미터, 임계값을 환경 변수에서 읽어 하드코딩을 피하세요.

## 데이터 수집 파이프라인
1. `open-trading-api` 스크립트를 래핑한 Celery 태스크를 작성해 토큰 발급 → 시세/체결/주문 API 호출을 순차 실행합니다.
2. 응답 JSON은 `pandas`로 정규화하고, MySQL 테이블(`market_prices`, `trade_logs`, `threat_events`)에 업서트합니다.
3. 대용량 파일(원본 JSON, 백테스트 결과)은 MinIO `raw-data` 버킷에 버전별로 저장합니다.
4. 실패 시 지수형 재시도(`tenacity`)와 슬랙/메일 알림을 사용하고, 오류 원인은 `etl_failures` 테이블로 기록합니다.

## AI 추천 & 위협 대응 워크플로
- **기본 로직**: 과거 시세, 사용자 시나리오 파라미터를 결합해 위험 점수, 추천 종목, 방어 전략 후보를 계산합니다. 계산은 Celery 태스크(`compute_risk`, `generate_recommendations`, `plan_mitigation`)로 나눕니다.
- **LLM 후처리**: ChatGPT API는 Celery 작업(`summarize_recommendation`, `draft_alert`)에서 호출하고, 입력 프롬프트/응답을 MinIO `prompts` 버킷에 JSON으로 저장합니다.
- **폴백 전략**: LLM이 실패하면 캐시된 최신 보고서를 반환하거나 ‘재시도중’ 메시지를 전달합니다. 모든 LLM 호출은 토큰 사용량을 MySQL `llm_usage` 테이블에 기록합니다.
- **실시간 이벤트**: 급락/위협 알림이 필요하면 Redis Pub/Sub 또는 Django Channels로 메시지를 푸시하고, Celery 태스크는 이벤트큐에 결과를 밀어 넣습니다.

## 품질 보증 & 평가 루틴
- **테스트**: `chk_ai.py`, `chk_etl.py`, `chk_llm.py` 세 가지 스크립트를 유지합니다. 데이터 스키마, 모델 예측 범위, LLM 응답 포맷을 검증합니다.
- **평가 지표**: 추천 정확도(히트율), 위험 점수 과대/과소 비율, LLM 유효 응답률을 주간 단위로 계산해 Grafana 패널로 노출합니다.
- **리플레이 환경**: 샌드박스 DB를 마련해 주요 Celery 태스크가 과거 데이터를 다시 돌릴 수 있게 하여 회귀 테스트를 수행합니다.
- **보안**: API 키는 `.env`/`kis_devlp.yaml` 또는 Vault에 저장하고, 실행 시에는 환경 변수로 주입합니다. MinIO 객체는 서버 사이드 암호화, LLM 로그는 민감 정보 마스킹을 적용합니다.

## 운영 자동화 체크리스트
1. Celery 워커/비트 컨테이너 헬스체크를 Compose에 등록하고, 재시작 정책을 `on-failure`로 설정합니다.
2. Slack/Email 알림을 위해 `health_monitor.py`를 작성해 큐 길이, 실패 태스크 수, LLM 응답 지연을 감시합니다.
3. 모델 업데이트 프로세스: (a) 새 데이터 스냅샷 확보 → (b) 노트북/스크립트로 학습 → (c) `models.json` 메타데이터 갱신 → (d) Celery 태스크에서 새 버전 로드.
4. 주간 점검: 오브젝트 스토리지 용량, 토큰 사용량, API 한도, 실패 로그를 리뷰하고 `mdfiles/AIfeedback.md`에 주요 변경사항을 기록합니다.
5. 재해 복구: MinIO와 MySQL 덤프를 하루 1회 스냅샷으로 남기고, 복구 절차 문서를 `docs/recovery.md`로 유지합니다.

## AI 팀 작업 우선순위 (이 순서면 완주 가능)
1. Python 환경/uv 설정 → Celery 기본 큐와 Redis 연결 구성.
2. `open-trading-api` 기반 데이터 수집 태스크 작성 및 MySQL/MinIO 적재 파이프라인 구축.
3. 기본 추천/위험 모델 구현, 결과 테이블/리포트 API 정의.
4. ChatGPT API 연동, 프롬프트 템플릿/응답 저장 구조 완성.
5. 자동화 스케줄러(celery-beat)와 모니터링/알림 스크립트 배포.
6. 테스트/평가 루틴과 모델 버전 관리, 복구 시나리오까지 문서화.
