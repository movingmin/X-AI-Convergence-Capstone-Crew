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
│  └─ serverinit.md         # 네이버 클라우드 서버 사양·견적
├─ open-trading-api/        # 한국투자증권 Open API 연동 실험(샘플 코드 위치)
└─ 활동일지/                # 비공개 활동 보고서 아카이브
```

## Collaboration Workflow
- **문서 업데이트**: 모든 정책·피드백 문서는 `mdfiles/`에서만 수정합니다. 회의록은 `mdfiles/Meeting.md`에 팀원이 직접 기록합니다.
- **코딩 컨벤션**: `open-trading-api/docs/convention.md` 명세(추가 예정)에 따라 4 space indentation, 타입 힌트, snake_case를 적용합니다.
- **작업 분리**: 웹 팀은 `mdfiles/WebFeedback.md`, AI 팀은 `mdfiles/AIfeedback.md`를 수시로 갱신하여 변경 사항을 공유합니다.
- **개발 환경**: Python 패키지는 `uv sync`, Node 기반 자산은 선택된 프레임워크 빌드 도구를 사용합니다. 서비스별 Dockerfile/Compose 정의는 `mdfiles/docker-compose.md`(필요 시 생성)에 정리합니다.
- **테스트 & 검증**: 주요 컴포넌트마다 `chk_*.py` 스크립트를 추가하고 CI에서 `uv run python`으로 실행합니다.

## Security & Operations
- 비밀 값(App Key/App Secret)은 `.env` 또는 `kis_devlp.yaml`에 저장하고 Git에 커밋하지 않습니다.
- 기본 모드는 데모/모의투자 환경이며, 실거래 호출은 별도 플래그와 승인 절차를 거칩니다.
- Docker 컨테이너는 비루트 사용자·읽기 전용 루트를 채택하고 Trivy 등으로 이미지를 정기 스캔합니다.
- 로그·백업은 개인정보를 필터링하여 저장하며, 외부 LLM 프롬프트와 응답은 민감 정보 익명화 후 보관합니다.
- 장애 대비 폴백 응답, 토큰 사용량 모니터링, 주기적 백업 절차를 유지합니다.

## Reference Documents
- `mdfiles/WhatcanIdo.md`: 전체 아키텍처와 기능 모듈 관계를 Mermaid로 정리
- `mdfiles/WebFeedback.md`: 프런트엔드/인프라 작업 우선순위와 Compose 운영 가이드
- `mdfiles/AIfeedback.md`: 데이터 파이프라인, 모델 워크플로, LLM 활용 전략
- `mdfiles/serverinit.md`: 네이버 클라우드 서버 구성 및 비용 산정
- `AGENTS.md`: 문서 역할, 개발 규칙, 보안 정책 세부 지침

## Near-Term Focus
1. 서비스 경계와 볼륨·네트워크 정책을 반영한 `docker-compose.yml` 초안 마련
2. Django+DRF API 스켈레톤과 인증, OpenAPI 문서화 흐름 구현
3. Celery 워커에서 한국투자증권 API 데이터 적재 및 기본 추천 로직 검증
4. 웹 대시보드 MVP 구성(로그인, 시나리오 편집기, 기본 리포트)
5. LLM 호출 로깅/폴백 시나리오 확립 및 보안 점검 리스트 유지
