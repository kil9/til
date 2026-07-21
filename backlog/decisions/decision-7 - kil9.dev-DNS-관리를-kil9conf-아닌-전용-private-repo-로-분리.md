---
id: decision-7
title: kil9.dev DNS 관리를 kil9conf 아닌 전용 private repo 로 분리
date: '2026-07-21 02:52'
status: accepted
---
## Context

task-71 원안은 dnscontrol 구성을 kil9conf 에 두는 것이었다(nuc14 기준 리모트가 github.com
하나뿐인 private repo 라 안전해 보였다). 그러나 kil9conf 는 회사 머신 클론에 사내 GHE 리모트가
있고 `/sync` 가 모든 리모트에 push 하는 구조라, dnsconfig.js(개인 도메인 kil9.dev 의 전체 구성)가
사내로 흘러간다. 이후 태스크(터널 서브도메인·메일 MX/SPF/DKIM)까지 같은 파일에 쌓이므로 노출
면적은 계속 커지고, 한 번 push 되면 히스토리에서 지우기 어렵다. 대안으로 (a) 전용 private repo
신설, (b) kil9conf 유지 + 사내 리모트 push 제외(운영 실수에 취약), (c) nuc14 로컬 git 만(백업
없음)을 검토했다.

## Decision

github.com/kil9/kil9dev-infra (private) 를 신설해 dnscontrol 구성(dns/)과 설치 스크립트
(bootstrap/)를 그곳에서 관리한다. dnscontrol 설치 스크립트도 kil9conf 에 두지 않아 kil9conf
에는 개인 도메인 관련 흔적을 남기지 않는다. creds.json 은 env 참조($CLOUDFLARE_APITOKEN)만
담아 시크릿 없이 커밋하고, 토큰은 머신 로컬 ~/.config/cloudflare/token(600)에만 둔다.

## Consequences

- 레코드 변경 = 커밋+push 흐름은 유지되면서 회사 리모트와 물리적으로 분리된다.
- 이후 m-7 태스크의 인프라 산출물(터널 구성 문서·메일 레코드·런북)도 kil9dev-infra 에 모은다.
- 진행 상황(backlog)은 계속 til repo 가 진실원본이다 — kil9dev-infra 에는 backlog 를 두지 않는다.
- 트레이드오프: repo 가 하나 늘고, kil9conf 부트스트랩 체계(머신 자동 전파)의 혜택을 받지
  못한다. 새 머신에서 DNS 를 만지려면 kil9dev-infra 클론 + 토큰 수동 배치가 필요하다.
