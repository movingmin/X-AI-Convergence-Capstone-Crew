# X-AI Convergence Capstone Crew

AI 기반 보안 투자 최적화 시뮬레이터를 설계하는 프로젝트입니다. 한국투자증권 Open API 데이터를 토대로 투자·위협 시나리오를 시뮬레이션하고, 웹 대시보드와 AI 분석 엔진을 결합해 의사결정을 돕는 것이 목표입니다.

## Mission Snapshot
- 보안 위협 수준과 예산 제약을 반영한 투자 시뮬레이션 환경 구축
- Django REST API + 웹 대시보드를 통한 운영자 워크플로 제공
- Celery 기반 AI 추천·위협 대응 엔진과 외부 LLM 보조 설명 결합
- Docker Compose로 단일 서버(네이버 클라우드) 배포 체계 마련

## Core Systems
- **데이터 수집·저장**: 한국투자증권 Open API 스크립트를 활용해 MySQL·MinIO에 시세, 주문, 리포트 데이터를 적재합니다.
- **AI 추천 & 위협 엔진**: Celery 워커가 위험 점수 계산, 종목 추천, 대응 전략 수립을 담당하며 필요 시 ChatGPT API로 설명을 보조합니다.
- **웹 애플리케이션**: Django+DRF가 인증, 시나리오 CRUD, 리포트 API를 제공하고, 웹 포털/모바일 에이전트가 이를 소비합니다.
- **모니터링 & 운영**: Compose 환경에 Redis, 모니터링 스택을 포함하고, Fail-safe·비밀 관리 정책을 문서화합니다.

## Tech Stack Baseline
- **Backend**: Python 3.13, Django 5, Django REST Framework, Celery, Redis
- **Data**: MySQL 8.4, MinIO (S3 호환), pandas/scikit-learn 기반 분석
- **Infra**: Docker Compose, 네이버 클라우드 Ubuntu 24.04 단일 서버, `uv sync`로 의존성 정렬
- **AI & LLM**: ChatGPT API(비동기 호출, 토큰 로깅), 내부 추천 모델(위험 점수·대응 전략)
- **Testing**: `chk_*.py` 실행 스크립트를 `uv run python <path>` 패턴으로 유지

## Development Environment
- **Python 버전**: `.python-version`은 3.13으로 고정되어 있습니다. `uv python install 3.13`으로 로컬 런타임을 준비하세요.
- **초기 동기화**: 루트에서 `uv sync --no-cache`를 실행하면 `.venv/`가 생성되고 기본 패키지( Django, Celery, Redis, pandas, scikit-learn, MinIO, OpenAI SDK 등)가 설치됩니다.
- **옵션 구성**: MySQL 네이티브 드라이버가 필요하면 시스템 라이브러리 설치 후 `uv sync --extra db`로 `mysqlclient`를 추가하세요. 기본 커넥터는 `pymysql`입니다.
- **작업 예시**:
  - 서버 실행: `uv run python manage.py runserver`
  - 워커 실행: `uv run celery -A config worker -l info`
  - 테스트: `uv run --extra tests pytest`
  - 린트: `uv run --extra lint ruff check .`
- **로컬 비밀**: `.env`나 `kis_devlp.yaml`에서 `REDIS_URL`, DB 접속 정보, OpenAI Key 등을 관리하고 Git에 추가하지 않습니다. `.env.example`은 추후 업데이트 예정입니다.

## Repository Layout
```text
.
├─ AGENTS.md                # 운영 지침 및 상세 역할 정의
├─ README.md                # 공개용 개요, 협업 규칙, 보안 지침 요약
├─ LICENSE
├─ mdfiles/                 # 정책·설계 레퍼런스
│  ├─ AIfeedback.md         # AI/데이터 파이프라인 피드백
│  ├─ Meeting.md            # 회의 메모(사용자 편집 전용)
│  ├─ WebFeedback.md        # 웹/인프라 피드백과 다음 단계
│  ├─ WhatcanIdo.md         # 전체 기능 구조와 Mermaid 그래프
│  ├─ server.md             # 확정된 서버 구성 및 예산
│  ├─ serverfeedback.md     # 서버 구성/비용 최적화 제안 및 논의
│  └─ serverinit.md         # 네이버 클라우드 서버 사양·견적
├─ open-trading-api/        # 한국투자증권 Open API 연동 실험(샘플 코드 위치)
└─ 활동일지/                # 비공개 활동 보고서 아카이브
```

> 참고: `mdfiles/open-trading-api.md`는 로컬 환경에서만 유지되는 민감 정보 메모로 Git 추적 대상이 아닙니다. 템플릿이나 가이드는 `open-trading-api/` 디렉터리 내 문서로 제공합니다.

## Collaboration Workflow
- **문서 업데이트**: 모든 정책·피드백 문서는 `mdfiles/`에서만 수정합니다. 회의록은 `mdfiles/Meeting.md`에 팀원이 직접 기록합니다.
- **운영 지침**: 역할, 문서 편집 규칙, 보안 정책은 `AGENTS.md`를 기준으로 유지하고, 세부 근거는 각 `mdfiles/*.md`에 기록합니다.
- **코딩 컨벤션**: `open-trading-api/docs/convention.md` 명세(추가 예정)에 따라 4 space indentation, 타입 힌트, snake_case를 적용합니다.
- **작업 분리**: 웹 팀은 `mdfiles/WebFeedback.md`, AI 팀은 `mdfiles/AIfeedback.md`, 서버/예산 이슈는 `mdfiles/server.md`(확정안)와 `mdfiles/serverfeedback.md`(제안/피드백)를 나눠 갱신합니다.
- **개발 환경**: Python 패키지는 `uv sync`, Node 기반 자산은 선택된 프레임워크 빌드 도구를 사용합니다. 서비스별 Dockerfile/Compose 정의는 `mdfiles/docker-compose.md`(필요 시 생성)에 정리합니다.
- **테스트 & 검증**: 주요 컴포넌트마다 `chk_*.py` 스크립트를 추가하고 CI에서 `uv run python`으로 실행합니다.

## Secrets & Credentials
- API App Key/App Secret 등 민감 정보는 `.env` 또는 `kis_devlp.yaml`에만 저장하고 Git 저장소에 올리지 않습니다.
- 로컬 참고용 `mdfiles/open-trading-api.md`는 `.gitignore`에 포함되어 있으며, 실제 키 값 대신 관리 절차와 환경 변수 명을 기록합니다.
- 팀 간 공유는 비밀 관리 솔루션(예: 1Password, Bitwarden)이나 암호화된 채널을 사용하고, 커밋/PR에는 절대 포함하지 않습니다.

## Security & Operations
- 기본 모드는 데모/모의투자 환경이며, 실거래 호출은 별도 플래그와 승인 절차를 거칩니다.
- Docker 컨테이너는 비루트 사용자·읽기 전용 루트를 채택하고 Trivy 등으로 이미지를 정기 스캔합니다.
- 로그·백업은 개인정보를 필터링하여 저장하며, 외부 LLM 프롬프트와 응답은 민감 정보 익명화 후 보관합니다.
- 장애 대비 폴백 응답, 토큰 사용량 모니터링, 주기적 백업 절차를 유지합니다.
- 서버 사양·예산, 복구 절차 등 운영 메모는 `mdfiles/serverinit.md`, `mdfiles/server.md`, `mdfiles/serverfeedback.md`를 통해 최신 상태로 관리하며 제안/확정안을 구분합니다.

## Infrastructure Snapshot (2025-11-03)
- **Database:** Cloud DB for MySQL (vCPU 2, RAM 8GB, 200GB CB2 + 50GB 백업)은 시나리오/위험 지표/주문 로그와 LLM 토큰 사용량 테이블을 단일 소스 오브 트루스로 유지하며, 주간 스냅샷을 통한 복구 계획을 뒷받침합니다.
- **Compute:** G3 Standard 서버 (vCPU 4, RAM 16GB, 512GB SSD, Ubuntu 24.04)는 Docker Compose 묶음(api-gateway, web-frontend, Celery 워커/비트, MinIO, 모니터링)을 수용하여 DRF API와 ETL/AI 태스크를 동시에 운영합니다.
- **Networking:** 단일 공인 IP + Private Subnet 구성은 HTTPS 게이트웨이를 외부에 공개하면서 DB/Redis/MinIO를 내부망으로 격리하고, 월 200GB 할당량으로 모의투자 API, 대시보드, LLM 콜백 트래픽을 감당합니다.
- **Budget:** 세 리소스의 월 총비용은 약 462,014원으로 Demo 환경 예산(월 50만 원 이내)에 부합합니다. 세부 로그는 `mdfiles/serverfeedback.md`에 기록합니다.

## Reference Documents
- `mdfiles/WhatcanIdo.md`: 전체 아키텍처와 기능 모듈 관계를 Mermaid로 정리
- `mdfiles/WebFeedback.md`: 프런트엔드/인프라 작업 우선순위와 Compose 운영 가이드
- `mdfiles/AIfeedback.md`: 데이터 파이프라인, 모델 워크플로, LLM 활용 전략
- `mdfiles/serverinit.md`: 네이버 클라우드 서버 구성 및 비용 산정
- `mdfiles/server.md`: 확정된 서버 구성과 예산
- `mdfiles/serverfeedback.md`: 서버 구성 피드백, 비용 절감 제안, 운영 체크포인트
- `AGENTS.md`: 문서 역할, 개발 규칙, 보안 정책 세부 지침

## Near-Term Focus
1. 서비스 경계와 볼륨·네트워크 정책을 반영한 `docker-compose.yml` 초안 마련
2. Django+DRF API 스켈레톤과 인증, OpenAPI 문서화 흐름 구현
3. Celery 워커에서 한국투자증권 API 데이터 적재 및 기본 추천 로직 검증
4. 웹 대시보드 MVP 구성(로그인, 시나리오 편집기, 기본 리포트)
5. LLM 호출 로깅/폴백 시나리오 확립 및 보안 점검 리스트 유지
