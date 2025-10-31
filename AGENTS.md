# 작업 개요 및 안내

## 프로젝트 전반
- 주제: AI 기반 보안 투자 최적화 시뮬레이터.
- 핵심 구성은 `open-trading-api` 샘플을 활용한 데이터 수집·시뮬레이션, 웹 대시보드, 위협 대응 전략 모듈입니다.
- 전체 기능 구조와 흐름은 `WhatcanIdo.md`의 Mermaid 그래프를 참고하세요.

## 문서 역할
- `Meeting.md`: 팀 회의 메모. 사용자가 직접 관리하므로 수정하지 않습니다. 사용자의 추가적인 요구가 있어도 이 메모에 작성, 참고.
- `Web_app/WebFeedback.md`: 웹 제작 관련 인프라·프레임워크 피드백과 다음 단계.
- `AIfeedback.md`: AI API 활용 방안, 데이터 파이프라인, 모델 관련 피드백.
- `docker-compose.md`: 서비스 경계, 컨테이너 구성, Compose 초안.
- `feedback.md`: 회의 기록에 대한 일반 피드백.
- `WhatcanIdo.md`: 전체 서비스 기능 목록 및 상호 연계 그래프.

## 문서 업데이트 규칙
- 웹 제작 피드백은 항상 `Web_app/WebFeedback.md`에 정리합니다.
- AI API 및 모델 활용 논의는 `AIfeedback.md`에 기록합니다.
- 회의 내용은 `Meeting.md`에만 사용자가 직접 메모합니다.
- 공통 구조나 계획이 바뀌면 `WhatcanIdo.md`, `docker-compose.md`를 함께 갱신합니다.

## 개발 스택 & 규칙
- 백엔드: Django + Django REST Framework, Celery+Redis 비동기 작업, MinIO 객체 저장소.
- 데이터베이스: MySQL 8.4 (컨테이너로 운영), 필요 시 Redis/RabbitMQ 큐 추가.
- 프런트엔드: Django 템플릿 혹은 React/Next.js 기반 UI(추후 선택).
- 환경 구성: Python 3.13, `uv sync`로 종속성 정렬, Docker Compose로 로컬 테스트 후 Kubernetes로 이관.
- 코딩 컨벤션: `docs/convention.md` 준수(4 space indentation, type hints, snake_case 명명, 모듈별 docstring).
- 테스트: 각 실행 샘플에 `chk_*.py` 배치, `uv run python path/to/chk_example.py`로 검증.

## 작업 흐름 제안
1. `docker-compose.md` 설계를 따라 서비스별 Dockerfile 정리 및 Compose 환경 구축.
2. Django+DRF API 스켈레톤 컨테이너에서 인증·Open API 연동을 검증.
3. AI 팀은 `AIfeedback.md`의 가이드를 반영해 ETL 워커·모델 추론 흐름을 준비.
4. 웹 팀은 `Web_app/WebFeedback.md`를 참고해 네이버 클라우드 환경, Kubernetes 배포 전략, UI 뼈대를 설계.
5. 공용 보안 정보는 `.env` 또는 `kis_devlp.yaml`(로컬 전용)에 보관하고 레포지토리에 커밋하지 않습니다.

## 보안 및 운영 포인트
- App Key/App Secret은 `kis_devlp.yaml`에만 저장하고 Git 추적에서 제외.
- Demo 환경 우선 사용, Real 트레이딩 호출은 명시적 플래그로 제한.
- 캐시·응답 데이터는 공유 전 정리하고, Config는 환경 변수 또는 Helper를 통해 로드.
- Kubernetes 전환 시 Namespace 분리, RBAC, NetworkPolicy, 이미지 스캔(Trivy) 적용.
