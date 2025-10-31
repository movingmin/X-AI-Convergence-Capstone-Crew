# 웹 플랫폼 아키텍처 및 도구 피드백

## Docker 패키징 전략
- **서비스 분리**: `web-frontend`(정적/SSR UI), `api-gateway`(REST/GraphQL), `ai-orchestrator`(모델 추론·시나리오 시뮬레이션), `mysql`(거래 데이터 저장), 선택형 `redis`(캐시·작업 큐)처럼 컨테이너를 기능별로 나눕니다. `etl-worker` 이미지는 한국투자증권 Open API 데이터를 주기적으로 수집합니다.
- **로컬·운영 공통 구성**: Docker Compose 프로필을 사용해 개발/운영 환경을 동일하게 재현합니다. 명명된 네트워크, `.env` 공유, TLS 인증서 바인드 마운트, 볼륨(데이터·로그)을 정의해 단일 서버에서도 서비스 간 연결을 명확히 합니다.
- **확장 여지**: 부하가 증가하면 `docker compose scale` 또는 Systemd 서비스로 컨테이너 수를 늘리고, 장기적으로 필요할 때만 Kubernetes로 이전합니다. 현재 계획에서는 Compose만으로 운영합니다.

## 서버 스펙 검토 (네이버 클라우드 High Memory 8vCPU/64GB/1TB SSD 단일 노드)
- **적합성**: Django API, Celery 워커, MySQL, Redis, MinIO를 한 서버에서 Docker Compose로 돌리기에는 충분한 여유가 있습니다. 8 vCPU와 64GB RAM이면 동시 사용자 수가 수백 명 수준이어도 CPU·메모리 병목이 거의 없으며, ETL/모델 추론 작업도 워커 수를 조절해 안정적으로 처리할 수 있습니다.
- **과도한 부분**: 64GB 메모리와 1TB SSD는 현재 계획된 데이터 규모(거래 내역·시뮬레이션 로그 중심)를 고려하면 다소 넉넉합니다. 월 요금(약 60만 원)이 부담된다면 4 vCPU / 16~32GB RAM, 200~300GB SSD 구성을 검토해도 무방합니다. GPU가 없는 사양이므로 대규모 딥러닝 재학습은 불가능하며, 필요 시 외부 GPU 인스턴스를 임시로 사용하는 방안을 준비해야 합니다.
- **부족한 부분**: 단일 서버 구성이라 가용성(HA)과 확장성이 제한됩니다. 장애 시 전체 서비스가 중단되므로, 정기 백업/스냅샷 정책과 빠른 복구 시나리오를 마련해야 합니다. 또한 MySQL과 MinIO에 대한 I/O를 집중적으로 사용한다면 SSD를 두 개의 볼륨으로 분리(운영체제용+데이터용)해 IOPS를 확보하는 방안도 고려할 수 있습니다.

## 외부 LLM 연동 전략
- **ChatGPT API 활용**: 투자 시나리오 요약, 위협 분석 보고서 작성, 사용자 질의 응답은 ChatGPT 등 외부 LLM API로 처리합니다. 모든 연산은 LLM 제공사의 GPU 인프라에서 수행되므로 우리 서버에는 GPU가 필요 없습니다.
- **API 호출 패턴**: Django 백엔드에서 비동기 호출(Celery)로 LLM 응답을 받아오고, 민감 데이터는 익명화/축약 후 전송합니다. 응답은 MySQL 또는 MinIO에 저장해 재사용합니다.
- **장래 확장**: 자체 모델 미세 조정이 필요해지면 GPU 인스턴스를 임대하거나 외부 파트너 서비스를 연결합니다. 현재 인프라에서는 CPU 기반 전처리·후처리만 수행합니다.

## 기능 구조 제안
- **프레젠테이션 레이어**: 공개 페이지, 인증 대시보드, 시나리오 편집기, 리포트 뷰어로 구성합니다. SPA(React/Vue) 또는 Django 템플릿 기반 SSR을 선택하고, Django 인증과 연계해 접근 제어를 구현합니다.
- **애플리케이션 레이어**: Django와 Django REST Framework(DRF)를 중심으로 사용자·세션 관리, 포트폴리오 시뮬레이션 API, 위험 시나리오 CRUD를 제공합니다. Celery 워커와 연동해 장시간 최적화 작업을 비동기로 처리하고, Django Channels를 통해 WebSocket 알림을 구현할 수 있습니다.
- **데이터·분석 레이어**: MySQL은 사용자·시뮬레이션·로그를 저장하고, MinIO/S3 등 오브젝트 스토리지는 모델 아티팩트와 대용량 데이터를 보관합니다. 시나리오 템플릿 메타데이터 테이블을 별도로 두고, ETL 워커가 Open API 피드를 정규화하며 AI 오케스트레이터는 예측·위험 점수를 게시합니다.
- **가시성·보안**: Prometheus+Grafana 또는 lightweight-exporter로 Compose 환경에서도 메트릭을 수집하고, Fail2ban/iptables 등으로 최소한의 네트워크 보호를 적용합니다. CI 단계에서 Trivy 등으로 이미지 스캔을 수행합니다.

## 프레임워크 및 도구 가이드
- **Django 확정**: Django는 기본 ORM, 인증/권한, 폼, 템플릿, 관리자(admin) 화면을 제공해 빠르게 MVP를 구축할 수 있습니다. Django REST Framework를 통해 REST/JSON API를 쉽게 노출하고, Django Channels로 WebSocket 기반 실시간 알림을 확장할 수 있습니다.
- **보완 라이브러리**:
  1. **Celery + Redis**: 백그라운드 최적화 작업, 리포트 생성, ETL 트리거, 외부 LLM 호출 비동기 처리를 담당합니다.
  2. **Django Allauth** 또는 **Social Auth**: 외부 로그인·이중 인증 등 인증 요구사항을 간편히 구현합니다.
  3. **DRF Spectacular/Swagger**: OpenAPI 문서를 자동 생성해 웹/모바일/에이전트 클라이언트와의 연동을 돕습니다.
- **프런트엔드 선택지**:
  - Django 템플릿: 서버 렌더 기반 관리 화면이나 초기 프로토타입에 적합합니다.
  - React+Vite 또는 Next.js: 풍부한 인터랙션과 대시보드를 원할 때 별도 프런트엔드 컨테이너에서 SPA/SSR을 제공합니다.
- **DevOps 권장 스택**: Poetry 또는 `uv`로 의존성 관리, Docker Compose로 개발/운영 환경을 구성, GitHub Actions CI(테스트·린트·컨테이너 빌드). 장기적으로 Kubernetes 이전을 고려한다면 Kustomize/ArgoCD를 병행할 수 있습니다.

## 다음 단계
1. Compose 기반 서비스 경계를 확정하고 `mdfiles/docker-compose.md` 초안을 작성합니다.
2. Django+DRF API 스켈레톤을 컨테이너화해 Open Trading API 데이터 수집과 기본 인증 흐름을 검증합니다.
3. 외부 LLM(ChatGPT) 호출 워크플로를 Celery 작업으로 구현하고, API 키·로그 필터링 정책을 문서화합니다.
4. 프런트엔드 스택(React/Next.js 또는 Django 템플릿)을 결정하고 인증·대시보드 뼈대를 구현한 뒤 AI 모듈과 연동합니다.
