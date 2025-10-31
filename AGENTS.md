# 작업 개요 및 안내

## 프로젝트 전반
- 주제: AI 기반 보안 투자 최적화 시뮬레이터.
- 핵심 구성은 `open-trading-api` 샘플을 활용한 데이터 수집·시뮬레이션, 웹 대시보드, 위협 대응 전략 모듈입니다.
- 전체 기능 구조와 흐름은 `mdfiles/WhatcanIdo.md`의 Mermaid 그래프를 참고하세요.

## 문서 역할
- `mdfiles/Meeting.md`: 팀 회의 메모. 사용자가 직접 관리하므로 수정하지 않습니다.
- `mdfiles/WebFeedback.md`: 웹 제작 관련 인프라·프레임워크 피드백과 다음 단계 기록.
- `mdfiles/AIfeedback.md`: AI API 활용 방안, 데이터 파이프라인, 모델 관련 피드백.
- `mdfiles/WhatcanIdo.md`: 전체 서비스 기능 목록 및 상호 연계 그래프.
- `mdfiles/docker-compose.md`(필요 시 신규 생성): 서비스 경계, 컨테이너 구성, Compose 초안.
- `mdfiles/feedback.md`(필요 시 신규 생성): 회의 기록에 대한 일반 피드백.
- `mdfiles/serverinit.md`: 네이버 클라우드 서버 사양·견적 기록(변경 시 갱신).
- `README.md`: 폴더 구조·협업 규칙·보안 지침을 요약한 공개용 개요 문서.

## 문서 업데이트 규칙
- 문서 편집은 `mdfiles/` 디렉터리 내 파일을 기준으로 합니다.
- 웹 제작 피드백은 항상 `mdfiles/WebFeedback.md`에 정리합니다.
- AI API 및 모델 활용 논의는 `mdfiles/AIfeedback.md`에 기록합니다.
- 회의 내용은 `mdfiles/Meeting.md`에만 사용자가 직접 메모합니다.
- 공통 구조나 계획이 바뀌면 `mdfiles/WhatcanIdo.md`, `mdfiles/docker-compose.md`(존재 시)를 함께 갱신합니다.

## 개발 스택 & 규칙
- 백엔드: 기본 구성은 Django + Django REST Framework로 REST API를 제공하며, 장기 작업이 생기면 Celery 워커와 Redis 메시지 큐를 붙입니다.
- 스토리지: 기본 데이터베이스는 MySQL 8.4 컨테이너입니다. 대용량 파일·모델을 저장해야 할 때 MinIO(S3 호환) 또는 객체 스토리지 대안을 도입합니다.
- 외부 LLM: ChatGPT 등 SaaS LLM을 API로 호출하며, 프롬프트 구성·비동기 처리 가이드는 `mdfiles/AIfeedback.md`를 따릅니다.
- 프런트엔드: Django 템플릿 혹은 React/Next.js 기반 UI(추후 선택).
- 환경 구성: Python 3.13, `uv sync`로 종속성 정렬, Docker Compose 중심의 단일 서버(네이버 클라우드 Ubuntu 24.04) 배포.
- 코딩 컨벤션: `open-trading-api/docs/convention.md` 준수(4 space indentation, type hints, snake_case 명명, 모듈별 docstring).
- 테스트: 각 실행 샘플에 `chk_*.py` 배치, `uv run python path/to/chk_example.py`로 검증.

## 작업 흐름 제안
1. `mdfiles/docker-compose.md`(존재 시) 설계를 따라 서비스별 Dockerfile 정리 및 Compose 환경 구축.
2. Django+DRF API 스켈레톤 컨테이너에서 인증·Open API 연동을 검증.
3. AI 팀은 `mdfiles/AIfeedback.md`의 가이드를 반영해 ETL 워커·모델 추론 흐름을 준비.
4. 웹 팀은 `mdfiles/WebFeedback.md`를 참고해 네이버 클라우드 단일 서버 기반 Docker Compose 배포 전략과 UI 뼈대를 설계.
5. 공용 보안 정보는 `.env` 또는 `kis_devlp.yaml`(로컬 전용)에 보관하고 레포지토리에 커밋하지 않습니다.
6. 실거래 API는 모의투자로 충분한 검증을 마친 뒤 필요한 경우에만 신청하며, 주문 한도·Fail-safe 로직을 사전에 정의합니다.

## 보안 및 운영 포인트
- App Key/App Secret은 `.env` 또는 `kis_devlp.yaml`에만 저장하고 Git 추적에서 제외합니다.
- Demo 환경을 기본값으로 사용하고 Real 트레이딩 호출은 명시적 플래그와 승인 절차를 거칩니다.
- 로그·백업·공유 데이터는 개인정보와 민감 정보를 필터링한 뒤 보관·배포합니다.
- Docker 컨테이너는 비루트 사용자와 읽기 전용 루트를 적용하고, 이미지는 Trivy 등으로 정기 스캔합니다.
- Config는 환경 변수 또는 Helper를 통해 로드해 하드코딩을 피합니다.
- 외부 LLM 호출 시 프롬프트와 응답을 로깅하되 민감 정보는 익명화하고, 장애 대비 폴백 응답을 준비합니다.
