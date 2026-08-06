---
id: DRAFT-4
title: 브리핑 잡 코드를 저장소로 이관하고 배포 배관을 만든다
status: Draft
assignee: []
created_date: '2026-08-06 06:15'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-backlog 자동 추가(2026-08-06, m-13 작업 중 발견).

nuc14 ~/jobs/liv-briefing/ 의 잡 코드(collect·select·compose·render·recap 등 1,700여 줄)가 머신 로컬 비버전이라, 브리핑을 고치는 태스크의 실질 산출물 대부분이 커밋되지 않는다. task-106·task-117·task-118 이 모두 같은 사정이었다. 검증과 재현이 repo 밖에 있고, 다른 머신에서 손댈 수 없으며, 코드 리뷰가 불가능하다.

m-13 착수 시점에 최소 조치로 그 디렉터리에 로컬 git 을 초기화해 롤백 기준점을 만들어 두었다(state/·repo*/ 는 ignore). 이 항목은 그다음 단계다.

완료 조건 후보:
- 잡 코드가 버전 관리되는 저장소에 있고 nuc14 가 그것을 당겨 쓴다. til 저장소는 public 이므로 시크릿 취급을 먼저 정해야 한다(현재 시크릿은 ~/.hermes 쪽이라 잡 디렉터리에 섞이지 않는다).
- 배포가 수동 복사가 아니다(체크아웃 + cron 이 그 경로를 보게 하거나, 배포 스크립트).
- 어느 머신에서든 코드를 고치고 nuc14 에 반영하는 경로가 문서화된다.

착수 전에 정할 것: 별도 private repo 인가, til 저장소 안(public, 시크릿 없음 확인 후)인가. 이 선택이 나머지를 다 바꾸므로 사용자 결정이 필요하다.
<!-- SECTION:DESCRIPTION:END -->
