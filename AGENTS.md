# 작업 지침 요약

## 프로젝트 개요
- 미션: AI 기반 보안 투자 최적화 시뮬레이터 구축
- 핵심 축: 한국투자증권 `open-trading-api` 데이터 → Django/DRF API → 대시보드 UI → AI 추천·위협 대응 엔진
- 전체 흐름: `mdfiles/WhatcanIdo.md`의 Mermaid 다이어그램과 단계별 로드맵을 기준으로 진행

## 문서 및 기록 관리
- `README.md`: 공개용 프로젝트 개요, 협업 규칙, 핵심 보안 정책 요약
- `AGENTS.md`: 본 문서. 에이전트/팀원의 역할, 문서 편집 규범, 운영 절차 정리
- `mdfiles/Meeting.md`: 주간 회의 기록. 에이전트는 열람만, 수정 금지
- `mdfiles/WebFeedback.md`: 웹/인프라 변경사항, Compose 운영 메모
- `mdfiles/AIfeedback.md`: AI 파이프라인, LLM 운용, 데이터 품질 피드백
- `mdfiles/WhatcanIdo.md`: 기능 구조와 책임 구역 한눈에 보기
- `mdfiles/serverinit.md`: 네이버 클라우드 서버 스펙·비용 산정 원본
- `mdfiles/server.md`: 확정된 서버 구성 및 현재 운영 예산
- `mdfiles/serverfeedback.md`: 서버 구성 제안·비용 절감 피드백 기록
- `mdfiles/docker-compose.md`, `mdfiles/feedback.md`: 필요 시 생성해 Compose 설계 또는 일반 피드백 기록
- 로컬 비밀 문서: `mdfiles/open-trading-api.md`는 `.gitignore`에 포함되어 있으며, API 키·시크릿은 여기에 기록하지 말고 `.env` 혹은 `kis_devlp.yaml`에서 환경 변수로 관리

## 문서 편집 규칙
- 정책·피드백 문서는 반드시 `mdfiles/` 하위에서만 수정하고, 회의 메모는 담당자만 갱신
- 서비스 구조 변경 시 `mdfiles/WhatcanIdo.md`와 `mdfiles/docker-compose.md`(존재 시)를 함께 업데이트
- 웹/인프라 변경은 `mdfiles/WebFeedback.md`, AI/데이터 변경은 `mdfiles/AIfeedback.md`에 기록 후 공유
- README/AGENTS는 외부 공지 및 공통 운영 기준을 압축한 버전으로 유지하며, 상세한 근거는 `mdfiles/` 문서에 남긴다

## 역할별 책임 정리
- **웹 & 인프라 팀** (`mdfiles/WebFeedback.md` 참고)
  - Django 5 + DRF API 게이트웨이, 인증/RBAC, 시나리오 CRUD 유지
  - Django 템플릿 기반 MVP → 필요 시 Vite+React 분리, API 스키마는 DRF Spectacular로 자동화
  - Compose 서비스( `api-gateway`, `web-frontend`, `static-nginx`, `monitoring` ) 정의 및 릴리스/모니터링 파이프라인 구축
  - 테스트 스크립트 `chk_api.py`, `chk_front.py` 유지, 보안 설정(CSRF, HTTPS, `SECURE_*`) 검증
- **AI & 데이터 팀** (`mdfiles/AIfeedback.md` 참고)
  - Celery 워커/비트, Redis, ETL 파이프라인(`open-trading-api` 래핑) 설계
  - 위험 점수·추천 모델, LLM 호출, MinIO 버킷 구조(`reports`, `models`, `prompts`) 운영
  - `chk_ai.py`, `chk_etl.py`, `chk_llm.py` 테스트 지표 유지 및 주간 품질 리포트 작성
  - 토큰 사용량·오류 모니터링, 실패 재시도/폴백 전략, 모델 버전 관리 문서화
- **공통 운영** (`mdfiles/serverinit.md`, `mdfiles/server.md`, `mdfiles/serverfeedback.md` 참고)
  - 네이버 클라우드 서버 사양 및 비용 추적, 공인 IP/DNS 관리
  - Docker Compose로 단일 서버 운영, Trivy 스캔·비루트 사용자·읽기 전용 루트 적용
  - 로그·백업 정책 수립, 주간 점검 항목을 `mdfiles/feedback.md` 또는 전용 문서에 기록
  - Database: Cloud DB for MySQL (vCPU 2/8GB, 200GB CB2 + 50GB 백업)을 시나리오/위험 지표·LLM 토큰 사용량 저장소로 운영하고, 주간 스냅샷과 복구 문서(`docs/recovery.md`) 준비를 책임집니다.
  - Compute: G3 Standard 서버 (vCPU 4/16GB, 512GB SSD, Ubuntu 24.04)에서 Compose 묶음(api-gateway, web-frontend, Celery 워커/비트, MinIO, 모니터링)을 상시 가동하며, 로그·모델 캐시 디스크 용량을 관리합니다.
  - Networking: 단일 공인 IP와 Private Subnet을 관리해 HTTPS 게이트웨이를 노출하고 DB/Redis/MinIO를 내부망에 격리하며, 월 200GB 전송량과 보안그룹/TLS 정책을 점검합니다.

## 개발 스택 & 협업 규칙
- Python 3.13 + `uv sync` 고정, Django REST Framework, Celery, Redis, MySQL 8.4, MinIO
- 프런트: Django 템플릿 → 필요 시 Vite+React/TypeScript, Chart.js 혹은 ECharts
- 외부 LLM: ChatGPT API 사용, 프롬프트/응답 로깅은 민감 정보 마스킹 후 MinIO 저장
- 코딩 컨벤션: `open-trading-api/docs/convention.md`(4-space, type hints, snake_case, 모듈 docstring)
- 모든 주요 실행 예시는 `chk_*.py` 형태의 검증 스크립트로 유지, `uv run python path/to/chk_example.py`
- CI 기본: `ruff`, `pytest`, (React 사용 시) `npm test`, Docker 이미지 빌드

## 운영 및 보안 정책
- 기본 실행 모드는 Demo/모의투자. 실거래 호출은 별도 플래그와 승인 절차, Fail-safe 로직(주문 한도/중단 조건) 수립 후 진행
- 비밀 값(App Key/Secret 등)은 `.env` 또는 `kis_devlp.yaml`에만 저장하고 Git 추적 금지. 필요 시 비밀 공유는 암호화된 채널 사용
- 로그·백업·공유 데이터는 민감 정보 필터링 후 저장. LLM 프롬프트/응답은 익명화, 토큰 사용량은 MySQL `llm_usage`에 기록
- Celery 워커/비트 헬스체크, 큐 길이·실패 태스크 모니터링, 주기적 백업·스냅샷 정책 유지
- Docker 컨테이너는 비루트 사용자, 읽기 전용 루트 적용. 이미지 스캔은 Trivy 등으로 정기 수행
- 장애 대비: LLM 실패 폴백, 데이터 복구 절차(`docs/recovery.md` 예정), 모니터링 알림(Slack/Email) 연동
- 서버 사양·예산 및 운영 변경 사항은 `mdfiles/serverinit.md`, `mdfiles/server.md`, `mdfiles/serverfeedback.md`에서 추적하며, 제안과 확정안을 구분해 기록

## 작업 순서 가이드
1. `mdfiles/docker-compose.md` 초안 확정 후 서비스별 Dockerfile 및 배포 스크립트 정리
2. Django+DRF 스켈레톤과 인증, OpenAPI 문서화, Celery/Redis 연동 검증
3. `open-trading-api` ETL 태스크와 MySQL/MinIO 적재 라인 구축, 실패 재시도·알림 연결
4. 대시보드/시각화 MVP 제작, React 전환 여부 결정, 공통 디자인 시스템 확립
5. LLM 호출 로그·폴백 설계, 토큰 사용량 모니터링, 백업·스냅샷·재해 복구 문서화
6. 주간 회의 메모, 웹/AI 피드백 문서 업데이트로 진행 상황 공유
