# PLAN — kil9/docs (GitHub Pages 퍼블리싱 저장소)

`/publish-pages` 로 넘어온 정적 페이지를 GitHub Pages 로 퍼블리시하는 저장소. 이 문서 하나로 현재 상태와 다음 할 일을 파악할 수 있게 유지한다. 커밋마다 갱신한다.

## 개요

- 목적: 자체 완결형 HTML 페이지를 디렉터리 단위로 호스팅하고, 루트 갤러리에서 모아 보여준다.
- 호스팅: GitHub Pages, `kil9/docs`(public), `main` 루트에서 직접 서빙.
- 라이브: <https://kil9.github.io/docs/>
- 퍼블리시 절차: [AGENTS.md](AGENTS.md) 의 "퍼블리시 런북" 을 정본으로 한다.

## 현재 상태

페이지 3건 퍼블리시됨. 루트 갤러리는 `data-date` 기반 최신순 정렬(T-10), nuc14 에 일 1회 AI요약 잡 가동 중(T-12, cron 09:00 KST). 남은 태스크는 T-11(이번달 외 카드 축약 + 아카이브)이며, 그 외에는 새 `/publish-pages` 요청이 오면 AGENTS.md 런북대로 페이지를 추가한다.

## 태스크

### 완료

- **T-1 문서 골격 작성** — README.md / AGENTS.md / PLAN.md / CLAUDE.md(심볼릭 링크). AGENTS.md 에 퍼블리시 런북 문서화.
- **T-2 첫 페이지 퍼블리시 준비** — claude.ai artifact `6090be57...` 를 자체 완결형 HTML 로 재조립해 `2026-matsuri-wuwa/index.html` 로 저장(프레임 런타임 제거). 제목: 夏色まつり ✕ 鳴潮 — 마츠리의 명조 방송 전기록.
- **T-3 루트 갤러리** — `index.html` 에 갤러리 랜딩 + 첫 페이지 카드 등록. README 표에도 반영.
- **T-4 git 초기화 및 첫 커밋** — `git init -b main`, 초기 커밋(`d92bcc1`). 커밋 이메일은 `61569+kil9@users.noreply.github.com`(public 저장소 프라이버시).
- **T-5 GitHub 저장소 생성 + push** — `gh repo create kil9/docs --public --source . --push`. remote `origin` 연결.
- **T-6 GitHub Pages 활성화** — source = branch `main`, path = `/`(root). `html_url = https://kil9.github.io/docs/`.

- **T-7 배포 검증** — 루트/첫 페이지 모두 HTTP 200 확인(첫 빌드 약 30초). 프레임 런타임 미유출, 갤러리 링크 정상.
- **T-8 히메모리 루나 명조 페이지 추가** — 로컬 아티팩트를 자체 완결형 HTML 로 재조립해 `2026-luna-wuwa/index.html` 로 저장. 방송 23편 타임라인 + 애정도 근거 기반 추정. 루트 갤러리·README 표 함께 갱신.
- **T-12 nuc14 일 1회 AI 트렌딩 요약 섹션** — nuc14 `~/jobs/docs-ai-summary/`(run.sh + extract.py + inject.py + state/pages.list)로 구현, cron `0 9 * * *`(KST). slug 목록 diff 로 신규 판정해 **신규 없으면 claude 호출 전에 조기 종료**, 신규 있으면 haiku 요약을 루트 `index.html` 의 `<!-- AI-SUMMARY:START/END -->` 마커 사이에 주입 후 `[auto]` 커밋·push, push 성공 후에만 상태 갱신. 요약 섹션은 기존 CSS 변수 재사용(라이트/다크·자체 완결 유지). 첫 실행(신규 3건 요약·push `4609899`)과 재실행(조기 종료) 모두 검증 완료.
- **T-13 (조사만) tumblr 퍼블리시 여부 조사** — 결과: **tumblr 연동 없음.** repo 파일 내 tumblr 언급 없음(PLAN 태스크 문구 제외), remote 는 `origin`(github.com/kil9/docs) 하나뿐, GitHub Actions 워크플로·CNAME 없음, Pages 설정은 `main`/root legacy 빌드에 custom domain 없음(`cname: null`), repo webhook 0건, 로스터 `/publish-pages` 스킬 정의에도 tumblr 언급 없음(해당 스킬은 Naver Pages 용이며 이 repo 런북과 별개).
- **T-10 인덱스 최신순 정렬(클라이언트 JS)** — 루트 `index.html` 카드에 `data-date` 부여, 로드 시 날짜 내림차순(동일 날짜는 원래 순서 유지)으로 카드를 재배치하는 인라인 스크립트 추가. 빌드 없음 유지.
- **T-9 두 세션 플랜 파이프라인 페이지 추가** — Claude Code 를 생산자·소비자 두 세션으로 나눠 쓰는 작업 방식(한쪽은 `/add-plan`, 다른 쪽은 `/follow-plan`·`/parallel-plan`)과 각 플랜 스킬의 용도를 인라인 SVG 다이어그램으로 설명한 자체 완결형 페이지를 `2026-07-plan-pipeline/index.html` 로 저장. 루트 갤러리·README 표 함께 갱신.

### 진행 중 / 다음

- **T-11 이번달 외 카드 축약 + 연/월 아카이브 목록** — 방문 시점의 현재 달(클라이언트 JS `data-date` 비교)이 아닌 카드는 **제목 + 날짜만** 남기고 설명(`p`)·경로를 숨겨 컴팩트하게 표시한다. 더해 과거 항목을 연/월 단위로 묶은 아카이브 목록을 만든다 — 항목이 적으면 연 단위, 많아지면 월 단위로 그룹핑한다(임계 기준은 구현 시 정한다). T-10 의 `data-date`·정렬 로직 위에 얹는다. (지금은 이번달 콘텐츠뿐이라 당장 시각적 변화는 없을 수 있음.)

- 위 태스크 외 다음 `/publish-pages` 요청 대기 중. 새 페이지는 [AGENTS.md](AGENTS.md) "퍼블리시 런북" 을 따른다.

## 아이디어 (보류)

- **I-1 저장소 전용 publish 커맨드** — 기존 `/publish-pages`(Naver Pages 배포)와 별개로, 이 저장소의 GitHub Pages 런북을 자동화하는 전용 슬래시 커맨드/워크플로 제작. 지금은 AGENTS.md 런북을 수동으로 따른다.
- **I-2 갤러리 태그/필터** — 페이지가 많아지면 루트 갤러리에 태그 필터·검색·연도 구분 추가.
- **I-3 OG 메타/썸네일** — 각 페이지에 Open Graph 메타태그와 미리보기 이미지 추가(SNS 공유 대응).

## 참고

- 첫 페이지 원본: `https://claude.ai/code/artifact/6090be57-74eb-4ba3-8f49-938684820a72`
- 퍼블리시 계정: github.com `kil9` (gh CLI 인증됨, `repo` scope)
