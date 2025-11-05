# X-AI Convergence Capstone Crew

AI 기반 보안 투자 최적화 시뮬레이터를 설계하는 프로젝트입니다. 한국투자증권 Open API 데이터를 토대로 투자·위협 시나리오를 시뮬레이션하고, 웹 대시보드와 AI 분석 엔진을 결합해 의사결정을 돕는 것이 목표입니다.

## 미션 요약
- 보안 위협 수준과 예산 제약을 반영한 투자 시뮬레이션 환경 구축
- Django REST API + 웹 대시보드를 통한 운영자 워크플로 제공
- Celery 기반 AI 추천·위협 대응 엔진과 외부 LLM 보조 설명 결합
- Docker Compose로 단일 서버(네이버 클라우드) 배포 체계 마련

## 핵심 시스템
- **데이터 수집·저장**: 한국투자증권 Open API 스크립트를 활용해 MySQL·MinIO에 시세, 주문, 리포트 데이터를 적재합니다.
- **AI 추천 & 위협 엔진**: Celery 워커가 위험 점수 계산, 종목 추천, 대응 전략 수립을 담당하며 필요 시 ChatGPT API로 설명을 보조합니다.
- **웹 애플리케이션**: Django+DRF가 인증, 시나리오 CRUD, 리포트 API를 제공하고, 웹 포털/모바일 에이전트가 이를 소비합니다.
- **모니터링 & 운영**: Compose 환경에 Redis, 모니터링 스택을 포함하고, Fail-safe·비밀 관리 정책을 문서화합니다.

## 기술 스택 기준
- **Backend**: Python 3.13, Django 5, Django REST Framework, Celery, Redis
- **Data**: MySQL 8.4, MinIO (S3 호환), pandas/scikit-learn 기반 분석
- **Infra**: Docker Compose, 네이버 클라우드 Ubuntu 24.04 단일 서버, `uv sync`로 의존성 정렬
- **AI & LLM**: ChatGPT API(비동기 호출, 토큰 로깅), 내부 추천 모델(위험 점수·대응 전략)
- **Testing**: `chk_*.py` 실행 스크립트를 `uv run python <path>` 패턴으로 유지

## 개발 환경 셋업
- **Python 버전 고정**: `.python-version`은 3.13입니다. 처음 클론한 뒤 `uv python install 3.13`을 실행해 동일한 런타임을 설치하세요.
- **의존성 동기화**:
  1. 레포지토리 루트에서 `uv sync --no-cache`를 실행하면 `.venv/`가 생성되고 Django, DRF, Celery[redis], pandas, scikit-learn, MinIO, OpenAI SDK, `pymysql` 등이 설치됩니다.
  2. 네이티브 MySQL 드라이버가 필요하면 시스템 패키지로 `libmysqlclient-dev` 계열을 설치한 다음 `uv sync --extra db`를 실행해 `mysqlclient`를 추가하세요. 기본 커넥터는 `pymysql`이므로 초기 개발은 시스템 의존성 없이 진행 가능합니다.
- **작업 명령 예시**:
  - Django 서버: `uv run python manage.py runserver`
  - Celery 워커: `uv run celery -A config worker -l info`
  - Celery 비트: `uv run celery -A config beat -l info`
  - 테스트: `uv run --extra tests pytest`
  - 린트: `uv run --extra lint ruff check .`
- **환경 변수 관리**: `.env` 또는 `kis_devlp.yaml`에 `REDIS_URL`, MySQL 접속 정보, OpenAI API Key 등을 보관하고 Git에는 올리지 않습니다. `example` 템플릿은 작업하면서 업데이트합니다.
- **Redis/Celery 확인**: Docker로 Redis를 띄운 뒤 `uv run python scripts/chk_etl.py`(작성 예정)를 실행하면 Celery 브로커 연결과 ETL 태스크 모의 호출 여부를 검증할 수 있습니다.

## 저장소 구조
```text
.
├─ README.md              # 프로젝트 개요 및 협업·보안 규칙 요약
├─ AGENTS.md              # 역할 분담, 문서 편집 규칙, 운영 절차 상세 가이드
├─ pyproject.toml         # uv 기반 Python 환경 정의 (Django, Celery, Redis, pandas 등)
├─ .venv/                 # uv sync 실행 시 자동 생성되는 가상환경 폴더 (Git 추적 제외)
├─ src/                   # Django 설정, Celery 태스크, ETL 로직이 들어갈 루트 패키지
│   └─ xai_capstone/      # 초기화 시 생성된 패키지; 프로젝트 코드가 확장될 위치
├─ mdfiles/               # 정책·회의·피드백 문서 모음
│   ├─ AIfeedback.md      # Celery/Redis/ETL/LLM 진행 상황 및 계획 정리
│   ├─ WebFeedback.md     # Django·프런트·인프라 변경 기록
│   ├─ Meeting.md         # 주간 회의록 (담당자만 수정)
│   ├─ WhatcanIdo.md      # 전체 기능 모듈과 책임 관계(Mermaid 다이어그램 포함)
│   ├─ server*.md         # 서버 사양·비용·피드백(확정안/제안안 분리)
│   └─ open-trading-api.md # 로컬 전용 민감 정보 메모 (Git 추적 금지)
├─ open-trading-api/      # 한국투자증권 Open API 샘플 및 래퍼 코드
└─ 활동일지/              # 비공개 활동 보고서 아카이브 (커밋 제외)
```

- 위 트리는 주요 디렉터리 구조와 책임 범위를 요약한 것입니다. 실제 구성은 개발 진행에 따라 `docker-compose.yml`, `scripts/`, `config/` 등이 추가될 수 있습니다.
- `open-trading-api/`는 별도 패키지 구조를 가지고 있으므로, ETL 태스크에서 모듈 임포트 시 경로를 명확히 지정하고 변경 사항은 해당 디렉터리 내 문서에 기록합니다.
- `mdfiles/open-trading-api.md`는 민감 정보를 다루므로 `.gitignore`에 포함되어 있으며, 운영 절차와 환경 변수 명칭만 정리합니다.

## 협업 워크플로
- **문서 업데이트**: 모든 정책·피드백 문서는 `mdfiles/`에서만 수정합니다. 회의록은 `mdfiles/Meeting.md`에 팀원이 직접 기록합니다.
- **운영 지침**: 역할, 문서 편집 규칙, 보안 정책은 `AGENTS.md`를 기준으로 유지하고, 세부 근거는 각 `mdfiles/*.md`에 기록합니다.
- **코딩 컨벤션**: `open-trading-api/docs/convention.md` 명세(추가 예정)에 따라 4 space indentation, 타입 힌트, snake_case를 적용합니다.
- **작업 분리**: 웹 팀은 `mdfiles/WebFeedback.md`, AI 팀은 `mdfiles/AIfeedback.md`, 서버/예산 이슈는 `mdfiles/server.md`(확정안)와 `mdfiles/serverfeedback.md`(제안/피드백)를 나눠 갱신합니다.
- **개발 환경**: Python 패키지는 `uv sync`, Node 기반 자산은 선택된 프레임워크 빌드 도구를 사용합니다. 서비스별 Dockerfile/Compose 정의는 `mdfiles/docker-compose.md`(필요 시 생성)에 정리합니다.
- **테스트 & 검증**: 주요 컴포넌트마다 `chk_*.py` 스크립트를 추가하고 CI에서 `uv run python`으로 실행합니다.

## 비밀 정보 관리
- API App Key/App Secret 등 민감 정보는 `.env` 또는 `kis_devlp.yaml`에만 저장하고 Git 저장소에 올리지 않습니다.
- 로컬 참고용 `mdfiles/open-trading-api.md`는 `.gitignore`에 포함되어 있으며, 실제 키 값 대신 관리 절차와 환경 변수 명을 기록합니다.
- 팀 간 공유는 비밀 관리 솔루션(예: 1Password, Bitwarden)이나 암호화된 채널을 사용하고, 커밋/PR에는 절대 포함하지 않습니다.

## 보안 및 운영 정책
- 기본 모드는 데모/모의투자 환경이며, 실거래 호출은 별도 플래그와 승인 절차를 거칩니다.
- Docker 컨테이너는 비루트 사용자·읽기 전용 루트를 채택하고 Trivy 등으로 이미지를 정기 스캔합니다.
- 로그·백업은 개인정보를 필터링하여 저장하며, 외부 LLM 프롬프트와 응답은 민감 정보 익명화 후 보관합니다.
- 장애 대비 폴백 응답, 토큰 사용량 모니터링, 주기적 백업 절차를 유지합니다.
- 서버 사양·예산, 복구 절차 등 운영 메모는 `mdfiles/serverinit.md`, `mdfiles/server.md`, `mdfiles/serverfeedback.md`를 통해 최신 상태로 관리하며 제안/확정안을 구분합니다.

## 인프라 현황 (2025-11-03)
- **Database:** Cloud DB for MySQL (vCPU 2, RAM 8GB, 200GB CB2 + 50GB 백업)은 시나리오/위험 지표/주문 로그와 LLM 토큰 사용량 테이블을 단일 소스 오브 트루스로 유지하며, 주간 스냅샷을 통한 복구 계획을 뒷받침합니다.
- **Compute:** G3 Standard 서버 (vCPU 4, RAM 16GB, 512GB SSD, Ubuntu 24.04)는 Docker Compose 묶음(api-gateway, web-frontend, Celery 워커/비트, MinIO, 모니터링)을 수용하여 DRF API와 ETL/AI 태스크를 동시에 운영합니다.
- **Networking:** 단일 공인 IP + Private Subnet 구성은 HTTPS 게이트웨이를 외부에 공개하면서 DB/Redis/MinIO를 내부망으로 격리하고, 월 200GB 할당량으로 모의투자 API, 대시보드, LLM 콜백 트래픽을 감당합니다.
- **Budget:** 세 리소스의 월 총비용은 약 462,014원으로 Demo 환경 예산(월 50만 원 이내)에 부합합니다. 세부 로그는 `mdfiles/serverfeedback.md`에 기록합니다.

## 참고 문서
- `mdfiles/WhatcanIdo.md`: 전체 아키텍처와 기능 모듈 관계를 Mermaid로 정리
- `mdfiles/WebFeedback.md`: 프런트엔드/인프라 작업 우선순위와 Compose 운영 가이드
- `mdfiles/AIfeedback.md`: 데이터 파이프라인, 모델 워크플로, LLM 활용 전략
- `mdfiles/serverinit.md`: 네이버 클라우드 서버 구성 및 비용 산정
- `mdfiles/server.md`: 확정된 서버 구성과 예산
- `mdfiles/serverfeedback.md`: 서버 구성 피드백, 비용 절감 제안, 운영 체크포인트
- `AGENTS.md`: 문서 역할, 개발 규칙, 보안 정책 세부 지침

## 단기 우선순위
1. 서비스 경계와 볼륨·네트워크 정책을 반영한 `docker-compose.yml` 초안 마련
2. Django+DRF API 스켈레톤과 인증, OpenAPI 문서화 흐름 구현
3. Celery 워커에서 한국투자증권 API 데이터 적재 및 기본 추천 로직 검증
4. 웹 대시보드 MVP 구성(로그인, 시나리오 편집기, 기본 리포트)
5. LLM 호출 로깅/폴백 시나리오 확립 및 보안 점검 리스트 유지
