---
id: TASK-119
title: 접수창구를 PWA 로 만들어 안드로이드 공유 시트에 share_target 등록
status: In Progress
assignee: []
created_date: '2026-08-06 12:33'
updated_date: '2026-08-06 14:28'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
2026/web-share-target/ 조사 보고서의 A안(본선)을 구현한다. 안드로이드 크롬·갤러리 등에서 공유 시트로 URL 을 넘기면 접수창구(p/submit-96a2d1c7e19e8a09/)가 항목으로 뜨고, 공유된 내용이 채워진 폼에서 접수까지 이어지게 한다.

접근: 접수창구 디렉터리에 manifest.webmanifest 와 아이콘을 두고 페이지 head 에 link rel=manifest 를 건다. share_target 은 method GET, action 은 절대 경로(안드로이드 캐시·상대경로 함정). 공유로 열려도 같은 오리진이라 localStorage 의 PAT 를 그대로 쓴다. 파일 공유(POST + multipart + 서비스 워커)는 이번 범위 밖.

결정사항:
- 공유 진입 시 기본 동작은 자동 접수가 아니라 프리필 폼이다(오발 방지, 구현 단순).
- 아이콘 192/512 파일은 접수창구 디렉터리 사이드카로 둔다. thumbs/·og/ 와 같은 결의 단일 파일 원칙 의도적 예외이며 AGENTS.md 에 명시한다.
- 안드로이드는 URL 을 url 파라미터로 주지 않는다 — text 에 실려 오므로 text 에서 URL 을 골라내는 처리가 필수.

근거 문서: 2026/web-share-target/index.html 의 '구현 체크리스트 (다음 에이전트용)' 절.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 p/submit-96a2d1c7e19e8a09/manifest.webmanifest 가 있고 name·icons(192/512)·start_url·scope·display:standalone·share_target(method GET, 절대 경로 action, params title/text/url)을 갖춘다
- [x] #2 접수 페이지 head 에 link rel=manifest 가 걸리고, 아이콘 파일이 같은 디렉터리에 사이드카로 존재한다
- [x] #3 공유 진입(?title/?text/?url)이면 그 내용으로 채워진 접수 폼이 뜬다. 자동 접수하지 않는다. text 파라미터에 URL 이 실려 온 경우를 골라내 처리한다
- [x] #4 접수 성공 후 history.replaceState 로 공유 쿼리를 지워, 새로고침해도 같은 내용이 다시 프리필되지 않는다
- [x] #5 접수 본문에 SOURCE: share-sheet 표식이 들어가 워처 쪽에서 유입 경로를 구분할 수 있다
- [x] #6 접수창구·매니페스트·아이콘 모두 비공개 유지: noindex 그대로이고 루트 갤러리·README 표·sitemap.xml·search-index.json·feed.xml 어디에도 노출되지 않는다
- [x] #7 AGENTS.md 에 PWA 아이콘·매니페스트 사이드카가 단일 파일 원칙의 의도적 예외임을 기록한다
- [x] #8 site-check.py 통과
- [ ] #9 관리자 실기 검증: 안드로이드 크롬에서 홈 화면에 추가 → 크롬에서 URL 공유 → 공유 시트에 항목이 뜨고 → 접수 폼이 프리필되고 → til-inbox 에 pending 이슈가 생기는 것까지 확인
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
구현 완료(2026-08-06). AC#9(관리자 실기 검증)만 남았다.

산출물: p/submit-96a2d1c7e19e8a09/ 에 manifest.webmanifest + icon-192.png·icon-512.png·icon-maskable-512.png 사이드카, index.html head 에 link rel=manifest·theme-color·apple-touch-icon, JS 에 prefillFromShare()·SOURCE 분기·성공 후 history.replaceState. AGENTS.md §2 에 사이드카 예외 기록.

파싱 규칙(안드로이드가 URL 을 url 이 아니라 text 로 보내는 것이 본선 경로):
- url 파라미터가 있으면 그것을 쓰고, 없으면 text 에서 URL 을 뽑는다.
- text 안 URL 이 정확히 하나일 때만 떼어낸다. 여럿이면 어느 것이 본체인지 알 수 없어 원문을 그대로 둔다(자동 접수가 아니라 폼에서 고칠 수 있다는 점이 이 위험을 흡수한다).
- title 이 text 에 부분문자열로 들어 있으면 title 을 버린다(삼성 '텍스트 공유'가 제목+URL 을 한 덩어리로 보낸다).
- 결합 순서는 [title, text, url]. URL 을 첫 줄에 두면 이슈 제목이 첫 줄에서 만들어지는 기존 규칙 때문에 접수함이 URL 목록이 된다.

설계 판단:
- 아이콘을 리브 얼굴로 했다. task-111 이 이 페이지 파비콘을 리브에서 📮 로 일부러 바꿨지만(탭에서 본문 페이지와 구분), 그 의도는 브라우저 탭 축이고 런처·공유 시트는 앱 정체성 축이라 축이 다르다. 탭 파비콘은 📮 그대로 두고 런처만 리브 얼굴이다.
- maskable 을 별도 파일로 뺐다. 얼굴이 꽉 찬 판본을 maskable 로 쓰면 안드로이드 adaptive 마스크가 머리 위를 잘라낸다. 512 캔버스에 410px 로 축소해 안전영역을 확보한 판본을 따로 굽고, any 는 크롭이 꽉 찬 판본을 쓴다.
- PAT 미등록 상태로 공유 진입해도 프리필은 유지된다 — 토큰 등록 핸들러가 submit-form 을 reset 하지 않아 별도 상태 저장이 필요 없다. 안내 문구만 patStatus 에 띄운다.
- enctype 은 뺐다(GET 에서는 의미가 없다). manifest id 를 명시해 나중에 start_url 이 바뀌어도 딴 앱으로 취급되지 않게 했다.

검증: 페이지의 prefillFromShare() 원문을 그대로 node 로 돌려 7케이스(크롬 표준·삼성 혼합·title 중복·URL 여럿·괄호 뒤따름·순수 텍스트·일반 방문) 통과. site-check.py 통과. sitemap·feed·search-index·루트 index·README 에 경로 미노출 확인.

Fable 자문에서 받은 지적 중 반영: maskable 분리, manifest id, title 보존, 결합 순서, URL 복수 시 원문 유지, enctype 제거. 반영 안 한 것: robots.txt Disallow 추가(경로를 오히려 광고한다 — 애초에 repo 가 public 이라 경로는 이미 공개이고 실제 게이트는 PAT 다).

AC#9 실기 때 볼 것:
- 크롬 메뉴가 '앱 설치'로 뜨는지. '홈 화면에 추가'만 뜨면 매니페스트 요건 미달 신호이고 그 바로가기는 share target 을 등록하지 않는다.
- 매니페스트를 고친 뒤에는 WebAPK 갱신이 하루 이상 걸릴 수 있으므로 삭제 후 재설치로 확인한다.
- 삼성 공유 시트에서는 항목이 첫 화면에 없고 옆으로 스크롤하거나 더보기 안쪽에 있을 수 있다.
<!-- SECTION:NOTES:END -->
