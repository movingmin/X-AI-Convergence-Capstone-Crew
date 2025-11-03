# 서버 피드백 로그

## 2025-11-03 서버 역할 정리
- **Database:** Cloud DB for MySQL (vCPU 2, RAM 8GB, 200GB CB2 스토리지)는 프로젝트의 단일 트랜잭션 저장소로 사용된다. 시나리오/위험 점수/주문 이력과 LLM 토큰 사용량 테이블을 여기서 일관성 있게 관리하며, 50GB 백업 스토리지는 주간 스냅샷과 장애 복구 계획(`docs/recovery.md` 예정)을 뒷받침한다.
- **Compute:** G3 Standard 서버 (vCPU 4, RAM 16GB, 512GB SSD)는 Docker Compose 묶음(api-gateway, web-frontend, Celery 워커/비트, MinIO, 모니터링)을 수용한다. Ubuntu 24.04 기반으로 DRF API, ETL 태스크, 대시보드 템플릿을 동시 운영하고, SSD 용량은 로그·모델 아카이브·캐시를 분리 마운트하기에 충분하다.
- **Networking:** 단일 공인 IP와 Private Subnet 구성은 외부 사용자에게 HTTPS 게이트웨이를 제공하면서도 DB/Redis/MinIO는 내부망에 고립시킨다. 월 200GB 전송량은 모의투자 API 호출, 대시보드 스트림, LLM 콜백 웹훅을 감안한 현재 사용량 범위 내이며, TLS 종단과 WAF/보안그룹 정책 업데이트가 가능한 구조다.
- **비용 메모:** 세 구성의 합산 월 462,014원은 Demo 환경 기준 예산(월 50만 원 이내)에 부합하며, 향후 실거래 플래그 도입 시에는 Database 슬레이브 증설 또는 Object Storage 증액을 대비해야 한다.
