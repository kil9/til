---
id: TASK-15
title: 리브 아바타 아이콘 표정 6종 제작 및 운용 규칙 문서화
status: Done
assignee: []
created_date: '2026-07-16 20:35'
updated_date: '2026-07-16 21:32'
labels:
  - solo
dependencies: []
priority: medium
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
현재 아이콘 버전 리브는 시큰둥한 기본 표정 한 종(`backlog/assets/liv/avatar-chibi.webp`, 256px)뿐이라, 페이지에 리브 코멘트가 서너 개 붙으면 같은 얼굴이 반복된다. 코멘트 톤(실수 고백·일 끝낸 직후·뜻밖의 발견)에 맞는 표정을 골라 쓸 수 있게 아이콘 세트를 만든다.

접근: 기존 설정화 시트 8컷은 헤어핀이 없는 구 판본이라 크롭으로는 현재 아바타와 어긋난다. 확정 기준본 `liv-final-chibi.webp`(헤어핀 판본)를 참고 이미지로 넣어 얼굴 클로즈업 컷을 신규 생성한다(doc-3 §4-2~§4-4 의 확정 프롬프트·일관성 규칙 준수 — 특히 `codex exec -i ref.png -- "프롬프트"` 의 `--`, 표정 지시의 부정형, 결과 md5 대조로 재탕 검출, 동시 5건 이하). 시트 8컷 일괄 재생성(doc-3 §4 의 미룬 숙제)은 이 태스크의 범위가 아니다.

적용은 T-4 원칙대로 신규 페이지부터. 기존 .liv 페이지 4개(moshi-voice-ai, voice-prompting-cost, kb16-bootloop-usb-power, 2026-07-agent-workflow)와 루트 index.html 의 a.keeper(기본 표정 유지)는 건드리지 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 표정 6종(기본 시큰둥 / 하품 / 계면쩍음 / 곤란·난감 / 살짝 만족 / 살짝 흥미) 256px 원본이 헤어핀 판본으로 생성돼 backlog/assets/liv/ 아래에 보존된다
- [x] #2 각 컷은 liv-final-chibi.webp 를 참고 이미지로 넣어 생성하고, 동일 인물·플랫 마스코트 화풍·헤어핀(그릴 슬릿 + 청록 LED)이 유지된다. 결과물 md5 를 서로/입력과 대조해 재탕·중복이 없음을 확인한다
- [x] #3 .liv 임베드용 72x72 WebP q85(컷당 약 2KB) 파생본이 6종 모두 만들어진다
- [x] #4 28px(.liv) 및 48px(a.keeper) 축소 상태에서 6종이 서로 구분되는지 육안 확인한다 — 구분이 안 되는 컷은 표정을 더 눌러 재생성한다
- [x] #5 doc-3(backlog/docs/doc-3 - 리브-투데이-캐릭터-설정.md)에 표정 아이콘 6종 표(파일명·표정·쓰임새)와 확정 프롬프트가 추가된다
- [x] #6 표정 선택 운용 규칙(코멘트 톤에 맞춰 고르고, 한 페이지 안에서 같은 표정을 반복하지 않으며, 애매하면 기본 시큰둥)이 doc-3 와 AGENTS.md 퍼블리시 런북 §2-2 의 .liv 마크업 항목에 반영된다
- [x] #7 기존 .liv 페이지 4개와 루트 index.html 의 a.keeper 아바타는 변경되지 않는다(git diff 로 확인)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
헤어핀 판본 기준 이미지(liv-final-chibi.webp)를 참고해 표정 6종을 생성하고, 256px 원본과 72px WebP q85 파생본을 보존했다. 72px 시트 육안 검토, WebP 헤더·해상도 검사, md5 상호/입력 대조, 기존 .liv 페이지와 index.html 무변경 diff를 확인했다. doc-3·AGENTS.md에 파일표·확정 프롬프트·선택 규칙을 기록했다.

사용자 피드백: 하품 외 표정의 28px 구분감이 약하다. 계면쩍음·난감·만족·흥미 컷에 작은 크기에서도 남는 만화적 시각 신호를 더해 재생성한다.

사용자 피드백에 따라 계면쩍음·난감·만족·흥미 4종을 재생성했다. 28px에서도 남는 만화적 신호(홍조·땀방울, 모인 눈썹·물결 입, 감긴 눈·미소, 별 하이라이트·둥근 입)를 추가했고, 설정화 시트의 인라인 72px 이미지가 파생 WebP 6종과 바이트 단위로 일치함을 확인했다. 모든 원본·파생본 WebP 헤더와 해상도, git diff --check를 다시 검증했다.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
표정 6종 중 구분감이 약했던 4종을 작은 크기용 만화적 시각 신호로 재생성해 설정화 시트와 자산을 갱신했다.
<!-- SECTION:FINAL_SUMMARY:END -->
