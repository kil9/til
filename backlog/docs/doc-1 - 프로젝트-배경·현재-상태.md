---
id: doc-1
title: 프로젝트 배경·현재 상태
type: other
created_date: '2026-07-13 14:08'
updated_date: '2026-07-13 14:08'
---
## 목적

`kil9/til` 은 `/publish-pages` 로 넘어온 정적 페이지를 GitHub Pages 로 퍼블리시하는 저장소다. 자체 완결형 HTML 페이지를 디렉터리 단위로 호스팅하고, 루트 갤러리에서 모아 보여준다.

- 호스팅: GitHub Pages, `kil9/til`(public, 2026-07-11 `kil9/docs` 에서 리네임), `main` 루트에서 직접 서빙(빌드 없음).
- 라이브: <https://kil9.github.io/til/>
- 퍼블리시 절차의 정본은 [AGENTS.md](../../AGENTS.md) 의 "퍼블리시 런북". 이 doc 은 배경·상태만 담는다.

## 현재 상태 (2026-07-13 기준)

페이지 9건 퍼블리시됨(matsuri / luna / plan-pipeline / ai-capex-hedge / claude-vs-gpt56-computer-use / citrini-2028-gic / hashimoto-oss-philosophy / ghostty-vs-windows-terminal / backlog-md-vs-plan-md) + `/til-archive/` 아카이브, 갤러리 카드 10장.

루트 갤러리 기능:
- `data-date`(날짜+시각 `YYYY-MM-DDTHH:MM`) 최신순 정렬, 카드에 시각까지 표시.
- 최신 피드 + 사이드바 월별 목차 + `/p/archive/` 전체 목록 페이지(2026-07-21, 구 이번달-축약 연/월 아카이브와 같은 날 시도한 루트 하단 전체-색인을 대체): 기본 뷰는 최근 10건 풀 카드(`?recent=N` 오버라이드), 검색·주제 칩이 걸리면 컷을 풀고 전체 카드에서 매치를 펼친다. 사이드바 목차(월별 건수, `/p/archive/` 앵커 연결)와 전체 목록 페이지(월별 카드 격자, 주제 타일 커버 — 색조+아이콘, `data-thumb` 훅으로 실제 썸네일 대체 가능)는 루트 카드를 진실원본으로 JS 자동 생성(후자는 루트 index.html 을 fetch)이라 퍼블리시 때 따로 갱신하지 않는다.
- 주제 필터 칩 + 검색 입력(`?q=` 딥링크, 칩과 AND 결합).
- AI요약은 히어로에 작은 라벨 + 안내 톤 요약문으로 표시(페이지 목록은 제거, 갤러리 카드로 대체).

AI요약 잡: nuc14 에서 일 1회 가동(cron 09:00 KST, 모델 sonnet). 경로 `~/jobs/docs-ai-summary/`. **주의: `inject.py` 템플릿은 index.html 히어로의 `<!-- AI-SUMMARY:START/END -->` 블록과 반드시 일치시켜야 다음 cron 이 되돌리지 않는다.** 루트 index.html 의 마커·`.ai-summary` 구조를 바꾸는 변경은 inject.py 와 동기화 필수.

디자인: 극한 미니멀(무채색 + 차가운 블루 액센트), 단일 리스트. 상세는 [decision](../decisions/) 참조. 사이트 구조는 SSG 미도입·현행 자체 완결형 HTML 방식 유지.

저장소 리네임: 2026-07-11 `kil9/docs` → `kil9/til` 완료(기존 til 노트는 `/til-archive/` 로 흡수, 원 저장소 삭제, 라이브 URL 은 `https://kil9.github.io/til/`). 방문 지표는 Cloudflare Web Analytics beacon 을 전 페이지에 삽입해 수집 중(CF 대시보드 `kil9.github.io`).

## 다음 할 일

정해진 미완료 태스크는 없다. 새 `/publish-pages` 요청이 오면 AGENTS.md 런북대로 페이지를 추가한다. 보류 아이디어는 draft(`/next-task` 로 조회) 참조.

## 참고

- 첫 페이지 원본: `https://claude.ai/code/artifact/6090be57-74eb-4ba3-8f49-938684820a72`
- 퍼블리시 계정: github.com `kil9`(gh CLI 인증, `repo` scope)
