---
id: TASK-57
title: 리브 공식 헤어 로우 번 채택 — 문서·기준본·공개 자산 전체 소급
status: Done
assignee: []
created_date: '2026-07-18 17:12'
updated_date: '2026-07-18 18:19'
labels: []
dependencies: []
ordinal: 57000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
2026-07-19 사용자 확정: 뒷머리를 낮게 묶어 목덜미가 드러나는 로우 번(시뇽)을 리브의 공식 헤어로 채택한다. 앞머리·통신 헤어핀은 유지.

소급 범위(사용자 선택: 공개 자산 전체):
- doc-3 헤어 스펙·§4-2 확정 프롬프트·§4-5 아바타 프롬프트 갱신
- SD 기준본(liv-final-chibi) 재생성
- 설정화 SD 6컷 재생성 + 공개 설정화 페이지(/p/liv-today/sheet/) 재임베드
- 코멘트 아바타 표정 6종(256px+72px) 재생성 + 설정화 페이지 재임베드
- keeper 아바타(avatar-chibi) 재제작 + 루트 index.html 재임베드
- 소개 페이지(/p/liv-today/) 상단 3컷·일상 삽화 2컷 재생성·재임베드
- 기존 아티클 페이지의 임베드 아바타는 소급하지 않는다(TASK-17 전례)
- 내부 참고용 사람 비율 2컷도 소급하지 않는다(TASK-17 전례)
<!-- SECTION:DESCRIPTION:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 내역:
- 새 SD 기준본(liv-final-chibi) 생성: 구 기준본(비율 앵커) + 묶은 머리 스터디 컷(헤어 앵커) 이중 참조 generate. 등신 드리프트 없음 확인.
- 설정화 SD 6컷 재생성(구 컷을 포즈·복장 앵커로, 새 기준본을 헤어 앵커로). ol-cardigan 은 1차에서 머리가 작아지는 드리프트가 나 비율 강제 문구로 1회 재생성.
- 아바타 표정 6종(256px+72px)·keeper 아바타(avatar-chibi, new-base 얼굴 크롭)·소개 페이지 삽화 2컷 재생성.
- 재임베드: 루트 index.html(keeper), /p/liv-today/(3컷+삽화2), /p/liv-today/sheet/(6컷+아바타 72px 12개). 전 임베드 RIFF/WEBP 디코드 검증, md5 재탕 검사 통과.
- 문서: doc-3 §4 헤어 개정(로우 번 공식화), 헤어핀 착용 문구 조정(귀 노출 정상화), §4-2·§4-5 확정 프롬프트 갱신, §4-1 확정 샘플·§4-4 시트·legacy 목록 주석. AGENTS.md §2-2 요약 갱신. alt 텍스트 2곳(루트 keeper·소개 1컷) 갱신.
- 구 판본(보브+핀)은 backlog/assets/liv/legacy/bob-hairpin/ 으로 이동. 사람 비율 2컷·기존 아티클 페이지 임베드는 TASK-17 전례대로 소급하지 않음.

후속(같은 날): '바쁜 날' 삽화(illust-work-busy)의 입을 화면 왼쪽으로 치우친 비대칭 히죽 웃음으로 EDIT 모드 수정(사용자 요청). 1차는 변화 없음, 2차는 방향 반대(화면 오른쪽)로 나와 창문/모니터 랜드마크로 방향을 못박아 3차에 성공. 컷 한정 일회성 조정이라 doc-3 에는 편입하지 않음. codex exec 가 stdin 을 물고 무한 대기한 사례 있음 — 호출 시 </dev/null 로 stdin 을 닫아야 한다.
<!-- SECTION:NOTES:END -->
