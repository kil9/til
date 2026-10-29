---
id: TASK-58
title: 스티커 스펙·포즈 20종 확정 (doc-3 편입)
status: Done
assignee: []
created_date: '2026-07-19 06:23'
updated_date: '2026-07-19 07:22'
labels: []
milestone: m-6
dependencies: []
priority: medium
ordinal: 58000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
스티커 세트의 진실원본 스펙을 만든다. 포즈 후보 약 20종(동작·상황 축 리액션 — 예: 엄지척·갸웃·박스 끌어안기·찻잔·손사래 등)을 리브 캐릭터성(최소 동선·시큰둥·호더)에 맞춰 목록화하고 사용자 확인을 받는다. 아바타 표정 6종(정서 축)과 역할이 겹치지 않게 한다. 규격: 투명 배경 WebP(알파) + 흰 다이컷 테두리, 원본/소형 판본 크기·품질·용량 목표, base64 임베드 전제. 확정 내용은 doc-3(리브 캐릭터 설정)에 스티커 절로 편입한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 포즈 20종 내외 목록이 사용자 확인을 거쳐 확정된다
- [x] #2 크기·품질·테두리·용량 규격이 수치로 확정된다
- [x] #3 doc-3 에 스티커 스펙 절이 추가된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
포즈 18종 확정(사용자 승인 2026-07-19): advisor(Fable) 검토로 초안 20종 중 아바타 표정과 겹치는 3종(반짝 기쁨→satisfied, 엎드림→yawn, 딴청→awkward)과 목록 내부 중복 2종(손사래→X, 노트북→태블릿), 실사용 없는 2종(빼꼼·기지개)을 삭제하고, til 반복 문맥에 대응하는 4종(느낌표 팻말·저울질·구겨진 종이 버리기·턱 괴고 대기)과 도장 찍기를 추가했다. 규격은 원본 512px q80(약 15KB)·소형 256px q85(약 7KB), 흰 다이컷 링 10px, 표시 상한 128px, 다크모드 filter: brightness(0.9). 임베드는 전부 소형 판본. 최대 리스크였던 투명화·다이컷 후처리는 PIL 만으로 구현해 기존 SD 컷으로 실증했고(backlog/assets/liv/stickers/diecut.py) 라이트/다크 렌더링을 육안 확인했다. 전부 doc-3 §4-6 에 편입.
<!-- SECTION:NOTES:END -->
