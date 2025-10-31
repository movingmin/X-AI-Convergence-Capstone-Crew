# 웹 플랫폼 아키텍처 및 도구 피드백

## Docker 및 Kubernetes 패키징
- **서비스 분리**: `web-frontend`(정적/SSR UI), `api-gateway`(REST/GraphQL), `ai-orchestrator`(모델 추론·시나리오 시뮬레이션), `mysql`(거래 데이터), 선택형 `redis`/`rabbitmq`(캐시·작업 큐)처럼 컨테이너를 기능별로 나눕니다. 별도 `etl-worker` 이미지는 한국투자증권 Open API 데이터를 주기적으로 수집합니다.
- **로컬 구성**: 배포 전까지는 `docker compose`로 명명된 네트워크, 공유 `.env`, 인증서 바인드 마운트를 설정해 실서비스 토폴로지를 미리 재현합니다.
- **Kubernetes 배치**: `capstone-trading` 네임스페이스를 만들고 각 서비스를 독립적인 `Deployment`+`Service`(ClusterIP)로 배치합니다. UI/API는 TLS 종단을 담당하는 `Ingress`(NGINX/Traefik)로 노출하고, 일반 설정은 `ConfigMap`, 비밀 정보는 `Secret`, MySQL 데이터는 `PersistentVolumeClaim`으로 연결합니다. API·AI 파드는 `HorizontalPodAutoscaler`로 확장하고, 야간 재학습이나 데이터 갱신은 `CronJob`으로 예약합니다. 로그는 사이드카 또는 DaemonSet(예: Fluent Bit → Elasticsearch/OpenSearch)으로 중앙 수집합니다.

## 기능 구조 제안
- **프레젠테이션 레이어**: 공개 페이지, 인증 대시보드, 시나리오 편집기, 리포트 뷰어로 구성합니다. SPA(React/Vue) 또는 Django 템플릿 기반 SSR을 선택하고, Django 인증과 연계해 접근 제어를 구현합니다.
- **애플리케이션 레이어**: Django와 Django REST Framework(DRF)를 중심으로 사용자·세션 관리, 포트폴리오 시뮬레이션 API, 위험 시나리오 CRUD를 제공합니다. Celery/RQ 백그라운드 작업과 연동해 장시간 최적화 작업을 비동기로 처리하고, Django Channels를 통해 WebSocket 알림을 구현할 수 있습니다.
- **데이터·분석 레이어**: MySQL은 사용자·시뮬레이션·로그를 저장하고, MinIO/S3 등 오브젝트 스토리지는 모델 아티팩트와 대용량 데이터를 보관합니다. 시나리오 템플릿 메타데이터 테이블을 별도로 두고, ETL 워커가 Open API 피드를 정규화하며 AI 오케스트레이터는 예측·위험 점수를 게시합니다.
- **가시성·보안**: Prometheus+Grafana로 모니터링을 중앙화하고, RBAC를 적용한 Kubernetes 클러스터와 네트워크 정책으로 DB 계층을 격리합니다. CI 단계에서 Trivy 등으로 이미지 스캔을 수행합니다.

## 프레임워크 및 도구 가이드
- **Django 확정**: Django는 기본 ORM, 인증/권한, 폼, 템플릿, 관리자(admin) 화면을 제공해 빠르게 MVP를 구축할 수 있습니다. Django REST Framework를 통해 REST/JSON API를 쉽게 노출하고, Django Channels로 WebSocket 기반 실시간 알림을 확장할 수 있습니다.
- **보완 라이브러리**:
  1. **Celery + Redis**: 백그라운드 최적화 작업, 리포트 생성, ETL 트리거를 담당합니다.
  2. **Django Allauth** 또는 **Social Auth**: 외부 로그인·이중 인증 등 인증 요구사항을 간편히 구현합니다.
  3. **DRF Spectacular/Swagger**: OpenAPI 문서를 자동 생성해 웹/모바일/에이전트 클라이언트와의 연동을 돕습니다.
- **프런트엔드 선택지**:
  - Django 템플릿: 서버 렌더 기반 관리 화면이나 초기 프로토타입에 적합합니다.
  - React+Vite 또는 Next.js: 풍부한 인터랙션과 대시보드를 원할 때 별도 프런트엔드 컨테이너에서 SPA/SSR을 제공합니다.
- **DevOps 권장 스택**: Poetry 또는 `uv`로 의존성 관리, Docker Compose로 개발 환경 구성, GitHub Actions CI(테스트·린트·컨테이너 빌드), ArgoCD/Kustomize로 Kubernetes 매니페스트를 선언적으로 관리합니다.

## 다음 단계
1. 서비스 경계를 확정하고 실서비스 토폴로지를 반영한 `docker-compose.yml` 초안을 작성합니다.
2. Django+DRF API 스켈레톤을 컨테이너화해 Open API 데이터 수집과 기본 인증 흐름이 동작하는지 검증합니다.
3. Kubernetes 매니페스트(베이스+오버레이)를 정의하고 스테이징 네임스페이스를 구성해 리허설 배포를 진행합니다.
4. 프런트엔드 스택(React/Next.js 또는 Django 템플릿)을 결정하고 인증·대시보드 뼈대를 구현한 뒤 AI 모듈과 연동합니다.
