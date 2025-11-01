# 웹 팀 전용 프레임워크 & 운영 가이드

## 우리가 맡을 서비스 경계
- **api-gateway**: Django 5 + DRF로 인증, 사용자·시나리오 CRUD, 투자 시뮬레이션 API를 제공합니다. REST 기본을 지키고 `/api/v1/` 접두사를 고정하세요.
- **web-frontend**: 초기엔 Django 템플릿으로 빠르게 붙이고, 대시보드가 복잡해지면 Vite+React 컨테이너로 분리합니다. 어떤 방식을 쓰든 인증은 Django 세션을 재활용합니다.
- **static-assets / nginx**: 정적 파일과 미디어를 서빙하는 얇은 Nginx 컨테이너입니다. `/static`은 빌드 결과물, `/media`는 사용자 업로드로 나눠 마운트하세요.
- **monitoring**: Node Exporter + Prometheus(경량) + Grafana 또는 Dozzle을 붙여 API/프런트 상태를 우리 쪽에서 즉시 확인할 수 있게 합니다.

## 필수 프레임워크 & 라이브러리
- **Django + DRF**: ORM, 인증, throttling, OpenAPI 문서(Swagger/Redoc)까지 기본 제공하므로 백엔드 핵심입니다.
- **Django Allauth**: 이메일 인증, 2FA(확장), 소셜 로그인까지 빠르게 붙을 수 있습니다.
- **DRF Spectacular**: API 스키마 자동화. 프런트와 모바일이 의존하므로 PR마다 `schema.yml`이 생성되는지 확인하세요.
- **Django Channels (선택)**: 실시간 알림이나 진행 상황 표시가 필요하면 WebSocket 단을 Channels로 두고 Redis를 브로커로 씁니다.
- **요청/응답 검증**: `pydantic`의 `BaseModel`을 적용하거나 DRF Serializer를 적극 사용해 프런트가 기대하는 스펙을 고정합니다.

## 프런트엔드 작업 흐름
1. **템플릿 빠른 뼈대**: Django 템플릿으로 로그인/대시보드 기본 화면을 만들고, Chart.js 또는 ECharts로 그래프를 붙여 MVP를 완성합니다.
2. **React 전환 기준**: 시나리오 편집기가 드래그·드롭 등 인터랙션을 요구하면 `web-frontend` 컨테이너를 생성하고 Vite+React+TypeScript로 마이그레이션합니다.
3. **디자인 시스템**: Chakra UI 혹은 Ant Design을 선택해 컴포넌트를 재사용합니다. 선택한 라이브러리는 `README`에 명시하고, 공용 색상·폰트 토큰은 `src/theme.ts`로 고정합니다.
4. **API 클라이언트**: `openapi-typescript`로 DRF 스키마에서 타입을 생성하고, React Query로 데이터 요청 캐시를 관리합니다.

## 배포 & Docker Compose 포인트
- `api-gateway`, `web-frontend`, `static-nginx`, `monitoring`, `redis`는 우리가 책임지는 Compose 서비스입니다. `mysql`, `minio`, `celery`는 AI팀과 협업하지만 설정 변경 시 반드시 공지합니다.
- 컨테이너별 `.env`를 나누되 공통 시크릿은 `.env` 루트 파일에서 읽습니다. 배포 전 `uv sync`로 종속성을 맞추고, `collectstatic` → `migrate` 순서로 배포 스크립트를 고정하세요.
- 리소스 제한: `api-gateway`는 `cpus: "2"` `mem_limit: 4g`, `web-frontend`는 `cpus: "1"` `mem_limit: 1g` 정도로 시작해 모니터링 결과에 따라 조정합니다.
- 네트워크: `frontend_net`과 `backend_net` 두 개를 만들어 외부 노출은 Nginx만 허용하고, DB/MinIO는 내부 네트워크로만 통신합니다.

## 품질 & 보안 체크리스트
- **테스트**: `chk_api.py`, `chk_front.py` 같은 유닛/통합 테스트를 `uv run python`으로 실행합니다. 최소한 인증, 시나리오 CRUD, 권한 제어 테스트를 유지하세요.
- **CI 파이프라인**: GitHub Actions에서 `ruff`, `pytest`, `npm test`(React 전환 시), Docker 이미지 빌드까지 자동화합니다.
- **로그**: API는 구조화 로그(JSON)를 남겨 Loki나 CloudWatch에 쌓기 쉽게 합니다. UI 에러는 Sentry 브라우저 SDK로 전송합니다.
- **보안 기본**: 모든 외부 요청은 CSRF/세션 만료를 설정하고, HTTPS 종속 Cookie(`Secure`, `HttpOnly`)를 적용합니다. Django `SECURE_*` 설정은 운영 모드에서 필수입니다.
- **릴리스 노트**: 프런트/백 사양 변경 시 `mdfiles/WebFeedback.md`를 최신화하고, AI 팀이 알아야 하는 변경(API 경로, 응답 필드)을 명시합니다.

## 웹 팀 작업 우선순위 (이 순서만 따라도 완주 가능)
1. Django 프로젝트 골격 구성 → 기본 모델/Serializer/뷰셋 작성.
2. 인증 흐름, RBAC, 감사 로그 구현.
3. 시나리오 편집기 API + 템플릿 UI 작성, 기본 차트 시각화.
4. Compose 서비스(`api-gateway`, `web-frontend`, `static-nginx`, `monitoring`) 정의 및 자동 배포 스크립트 작성.
5. React 전환 여부 결정 → 필요 시 타입 생성, 디자인 시스템 정착.
6. 모니터링·알람, 장애 대응 플레이북, 주간 릴리스 루틴 확립.
