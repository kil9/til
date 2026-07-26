---
id: TASK-110
title: 발행된 글의 죽은 외부 링크 정리
status: Done
assignee: []
created_date: '2026-07-26 16:13'
updated_date: '2026-07-26 16:19'
labels: []
dependencies: []
priority: low
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-backlog 자동 추가: TASK-109 의 site-check.py --external 을 처음 돌려 보니 외부 링크 232개 중 8건이 404·타임아웃·연결 끊김이었다(2026-07-27 실측). 발행 당시에는 살아 있던 링크가 죽은 것이라 본문 근거가 확인 불가 상태로 남아 있다. 각각 확인해 대체 URL·web.archive.org 스냅샷으로 바꾸거나, 대체가 없으면 링크를 풀고 출처만 텍스트로 남긴다. 대상: docker/community DockerCon EU 2015(p/til-archive), lasvegassun 링봇맵 기사(lingbot-map-local), moshi.chat(moshi-voice-ai), sad.psychiatry.ubc.ca 광치료 절차(sad-light-therapy), aitimes 기사(citrini-2028-gic), softwarecollections.org devtoolset-8(p/til-archive), visitusers.org CMake(p/til-archive), washingtonpost citrini 칼럼(citrini-2028-gic). 후자 셋은 봇 차단·일시 장애일 수 있으니 브라우저로 재확인부터 한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 8건을 각각 브라우저로 재확인해 진짜 죽은 것과 봇 차단·일시 장애를 가른다
- [x] #2 죽은 링크는 대체 URL 또는 web.archive.org 스냅샷으로 교체하고, 대체가 없으면 링크를 풀고 출처 표기만 남긴다
- [x] #3 수정 후 site-check.py --external 재실행 결과를 태스크 노트에 남긴다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료(2026-07-27):
- 8건을 브라우저 UA + GET 으로 재확인해 3종으로 갈렸다.
  · 오탐 2건(HEAD 에만 404/에러): aitimes 기사, UBC 광치료 절차 — 둘 다 GET 200. 원문 유지.
  · 봇 차단 1건: washingtonpost 칼럼 — HEAD·GET·HTTP1.1 모두 타임아웃이고 기사 자체는 살아 있는 유료 칼럼이라 원문 유지.
  · 진짜 사망 5건: docker/community DockerCon EU 2015(404, 스냅샷 없음), lasvegassun 기사(404, 스냅샷 없음), moshi.chat(인증서 2026-07-07 만료), softwarecollections.org(인증서가 CN=localhost 자체서명으로 바뀜 = 도메인 방치), visitusers.org(TLS/HTTP 프로토콜 오류).
- 조치: 스냅샷 있는 3건(moshi.chat 2026-04, softwarecollections 2025-06, visitusers 2023-02)은 web.archive.org 링크로 교체하고 무엇의 스냅샷인지 괄호로 밝혔다. 스냅샷 없는 2건은 링크를 풀고 출처 표기만 텍스트로 남겼다. moshi 는 '데모를 바로 써 볼 수 있다'는 서술이 사실과 달라져 문장도 고쳤다.
- site-check.py 보강: HEAD 가 실패하면 GET 으로 한 번 더 본다(HEAD 를 제대로 처리 못 하는 서버가 흔하다 — 실측 오탐 2건이 그것). 브라우저 UA 를 쓰고, 405 는 사유 목록에서 뺐다(GET 폴백이 대신한다). 다른 페이지 앵커 검사에도 '#top' 예외를 맞췄다.
- 재실행 결과: 외부 링크 230개 확인 · 응답 없음 1건(washingtonpost 봇 차단). 8건 → 1건.
<!-- SECTION:NOTES:END -->
