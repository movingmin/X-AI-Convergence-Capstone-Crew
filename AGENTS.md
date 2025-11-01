# 작업 개요 및 안내

## 프로젝트 전반
- 주제: AI 기반 보안 투자 최적화 시뮬레이터 구축
- 핵심 구성: `open-trading-api` 기반 데이터 수집·시뮬레이션, 웹 대시보드, 위협 대응 전략 모듈
- 전체 기능 구조 및 흐름: `mdfiles/WhatcanIdo.md`의 Mermaid 그래프 참조

## 문서 체계
- `README.md`: 공개용 개요, 협업 규칙, 보안 지침 요약
- `AGENTS.md`: 에이전트/팀원의 상세 업무 기준과 문서 편집 규칙
- `mdfiles/Meeting.md`: 주간 회의 메모 (사용자 직접 관리, 열람만)
- `mdfiles/WebFeedback.md`: 웹/인프라 관련 피드백과 차기 액션
- `mdfiles/AIfeedback.md`: AI API, 데이터 파이프라인, 모델 관련 피드백
- `mdfiles/WhatcanIdo.md`: 전체 기능 목록 및 상호 연계 다이어그램
- `mdfiles/docker-compose.md` (필요 시 생성): 서비스 경계, 컨테이너 구성, Compose 초안
- `mdfiles/feedback.md` (필요 시 생성): 회의 내용 외 일반 피드백
- `mdfiles/serverinit.md`: 네이버 클라우드 서버 사양 및 견적 기록

## 문서 편집 규칙
- 정책·피드백 문서는 반드시 `mdfiles/` 하위에서만 수정합니다.
- 회의 내용은 `mdfiles/Meeting.md`에 팀원이 직접 기록하며, 에이전트는 편집하지 않습니다.
- 웹 관련 변경사항은 `mdfiles/WebFeedback.md`, AI 관련 변경사항은 `mdfiles/AIfeedback.md`에 정리합니다.
- 서비스 경계나 공통 구조가 바뀌면 `mdfiles/WhatcanIdo.md`와 `mdfiles/docker-compose.md`(존재 시)를 함께 갱신합니다.
- README/AGENTS는 공개 가이드와 내부 운영 기준을 요약하는 용도로 유지합니다.

## 개발 스택 & 규칙
- 백엔드: Django 5 + Django REST Framework, 필요 시 Celery 워커와 Redis 메시지 큐 확장
- 데이터/스토리지: MySQL 8.4 컨테이너, 대용량 파일·모델은 MinIO(S3 호환) 또는 객체 스토리지 사용
- 프런트엔드: Django 템플릿 기반 MVP → 필요 시 Vite+React/Next.js로 분리
- 외부 LLM: ChatGPT 등 SaaS LLM API 사용, 프롬프트 구성·비동기 처리 가이드는 `mdfiles/AIfeedback.md` 준수
- 환경 구성: Python 3.13, `uv sync`로 종속성 정렬, Docker Compose 기반 단일 서버(네이버 클라우드 Ubuntu 24.04) 운영
- 코딩 컨벤션: `open-trading-api/docs/convention.md` 명세(4 space indentation, type hints, snake_case, 모듈 docstring) 준수
- 테스트: 각 실행 샘플에 `chk_*.py` 유지, `uv run python path/to/chk_example.py`로 검증

## 권장 작업 흐름
1. `mdfiles/docker-compose.md` 설계를 참고해 서비스별 Dockerfile과 Compose 환경 정의
2. Django+DRF API 스켈레톤을 컨테이너화해 인증·Open API 연동 검증
3. `open-trading-api` 스크립트를 Celery 태스크로 래핑해 데이터 적재 파이프라인 구성
4. 웹 팀은 `mdfiles/WebFeedback.md` 지침에 따라 대시보드/UI 뼈대 설계 및 배포 전략 수립
5. AI 팀은 `mdfiles/AIfeedback.md` 가이드를 기반으로 ETL 워커·모델 추론 흐름 구현
6. 공용 보안 정보는 `.env` 또는 `kis_devlp.yaml`(로컬 전용)에만 저장하고 Git 추적에서 제외
7. 실거래 API 사용은 모의투자 환경에서 충분히 검증한 뒤 주문 한도·Fail-safe 로직을 선행 정의

## 보안 및 운영 정책
- App Key/App Secret 등 비밀 값은 `.env` 또는 `kis_devlp.yaml`에만 저장하며 버전관리에서 제외합니다.
- 기본 실행 모드는 Demo/모의투자이며, Real 트레이딩 호출은 명시적 플래그와 승인 절차를 거칩니다.
- 로그·백업·공유 데이터는 개인정보·민감 정보를 필터링한 뒤 저장·배포합니다.
- Docker 컨테이너는 비루트 사용자와 읽기 전용 루트를 적용하고, 이미지는 Trivy 등으로 정기 스캔합니다.
- Config는 환경 변수 또는 Helper를 통해 로드해 하드코딩을 피합니다.
- 외부 LLM 호출 시 프롬프트·응답을 로깅하되 민감 정보는 익명화하고, 장애 대비 폴백 응답을 준비합니다.
- Celery 워커/비트 헬스체크, 토큰 사용량 모니터링, 주기적 백업·스냅샷 정책을 유지합니다.
