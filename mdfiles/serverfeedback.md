# 서버 비용 최적화안 제안 (월 50만 원대 목표)

## 제안 개요
- **대상**: 기존 150만 원대 견적 대비 예산 축소가 필요한 상황
- **목표 예산**: 월 500,000원 이하
- **핵심 아이디어**: 단일 중간 사양 서버로 서비스 통합, Cloud DB 다운스케일, Object Storage 도입, 네트워크 리소스 최소화
- **예상 총액**: **약 492,096원/월** (부가세 제외, 24시간 가동 기준)

| 항목 | 제안 사양 | 월 예상 비용 | 비고 |
|------|-----------|--------------|------|
| 통합 애플리케이션 서버 | Standard G2, vCPU 8 · RAM 32GB, SSD 512GB | 263,232원 | Django API, Celery, 정적 자산, 모니터링 통합 |
| Cloud DB for MySQL | vCPU 2 · RAM 8GB, SSD 200GB, 자동 백업 50GB | 193,600원 | 보존 기간 3개월, 장기 데이터는 Object Storage 이전 |
| Object Storage | Standard 클래스 200GB | 19,200원 | 모델·리포트·LLM 로그 저장 |
| 네트워크 & DNS | 공인 IP 1개, Global DNS 1건 | 8,064원 + 1,430원 | 외부 노출은 Nginx 하나로 일원화 |
| 보안 스캔/기타 | Trivy cron 구동 | 0원 | 오픈소스 사용 |
| **합계** |  | **492,096원** |  |

> 단가 근거: 네이버 클라우드 2024년 Q1 On-Demand 가격표, 720시간 사용 시 산정. 트래픽·부가세·추가 백업은 제외.

---

## 서비스별 운영 전략 제안

### 1. 애플리케이션 서버 통합
- 웹/API, Celery 워커, Redis, Nginx, 모니터링을 Docker Compose로 컨테이너 분리.
- 야간에는 Celery 워커 수를 1대로 줄이고, 필요 시 `docker compose scale`로 수동 확장.
- 주간 장애 대비: 스냅샷 주 1회, 복구 스크립트 자동화.

### 2. Cloud DB 다운스케일
- vCPU 4 → 2, RAM 16GB → 8GB, 스토리지 1TB → 200GB.
- 거래 로그 보존 기간을 3개월로 제한하고, 월말에 Object Storage로 이전.
- 자동 백업 주기를 3일로 줄이고, 중요 시점은 수동 스냅샷을 Object Storage에 저장.

### 3. Object Storage 도입
- `reports`, `models`, `prompts` 버킷을 생성해 장기 보관.
- 6개월 이상 데이터는 Archive 클래스로 이전해 요금 추가 절감.
- MinIO 대신 네이버 Object Storage 사용 시 Outbound 트래픽 비용 검토.

### 4. 네트워크 최적화
- 공인 IP 1개만 유지, Nginx Reverse Proxy로 모든 외부 요청 처리.
- 내부 통신은 VPC Peering(추가 비용 없음)으로 DB와 연결.
- Dozzle, cAdvisor 등 모니터링 UI는 VPN 혹은 Bastion을 통해 제한적 접근.

### 5. 보안·운영 권장사항
- Trivy를 주 1회 cron으로 실행하고 결과를 Slack/Email로 알림.
- Celery 큐 길이, 실패 태스크 수, LLM 호출 오류를 Prometheus 대신 경량 스크립트로 체크.
- 백업: DB는 3일 자동 백업 + 주 1회 덤프(Object Storage), 애플리케이션 컨테이너는 `docker save`로 월 1회 보관.

---

## 추가 절감 아이디어
1. 1년 예약 인스턴스(선납)로 전환 시 약 15~20% 추가 절감 가능.
2. 근무 시간대만 Celery 워커 추가 컨테이너를 올려 CPU 사용량을 제한.
3. LLM 호출 캐시·폴백 비율을 높여 외부 API 비용을 분기별로 조정.
4. 로그 샘플링(50%) 및 30일 이상 로그 압축 보관으로 Object Storage 비용 절감.
5. 모니터링/알림은 Slack Webhook 기반 경량 스크립트로 운영해 추가 SaaS 비용을 제거.

---

## 후속 액션 제안
- 위 제안을 검토 후 채택 여부와 예산 변동 사항을 `mdfiles/server.md`에 명시해 주세요.
- 채택한 항목은 `mdfiles/serverfeedback.md` 하단에 “반영 완료” 메모를 남기고, 미채택 항목은 사유를 기록하면 향후 재검토가 수월합니다.
