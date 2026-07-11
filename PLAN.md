# PLAN — kil9/docs (GitHub Pages 퍼블리싱 저장소)

`/publish-pages` 로 넘어온 정적 페이지를 GitHub Pages 로 퍼블리시하는 저장소. 이 문서 하나로 현재 상태와 다음 할 일을 파악할 수 있게 유지한다. 커밋마다 갱신한다.

## 개요

- 목적: 자체 완결형 HTML 페이지를 디렉터리 단위로 호스팅하고, 루트 갤러리에서 모아 보여준다.
- 호스팅: GitHub Pages, `kil9/docs`(public), `main` 루트에서 직접 서빙.
- 라이브: <https://kil9.github.io/docs/>
- 퍼블리시 절차: [AGENTS.md](AGENTS.md) 의 "퍼블리시 런북" 을 정본으로 한다.

## 현재 상태

페이지 3건 퍼블리시됨. 루트 갤러리는 `data-date` 최신순 정렬(T-10) + 이번달 외 카드 축약·연/월 아카이브(T-11) 적용, nuc14 에 일 1회 AI요약 잡 가동 중(T-12, cron 09:00 KST). 주제 필터 칩(T-14)도 적용. 남은 태스크는 T-15\~T-17·T-19 이며(T-18 은 T-17 만 남기고 선행 해소됨), 그 외에는 새 `/publish-pages` 요청이 오면 AGENTS.md 런북대로 페이지를 추가한다.

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
- **T-14 인덱스 주제별 분류(필터 칩)** — 카드에 `data-topic` 부여(hololive / claude-code, kebab-case·느슨한 taxonomy), AI요약 아래에 필터 칩(`전체`+주제별)을 클라이언트 JS 로 자동 생성. 칩 라벨은 `.tag` 의 "·" 앞 세그먼트 재활용, 주제 2개 미만이면 칩 미표시. 필터는 T-11 아카이브 그룹과 연동(빈 그룹·빈 아카이브 숨김), `?topic=<key>` 딥링크 지원. 표시 방식은 그룹 헤딩 대신 **필터 칩**으로 사용자 확정(날짜 정렬·아카이브 그룹핑과 직교). AGENTS.md 런북에 신규 카드 `data-date`/`data-topic` 필수 명시. 헤드리스 Chrome 으로 칩 생성·필터·아카이브 연동·폴백 검증.
- **T-11 이번달 외 카드 축약 + 연/월 아카이브** — 방문 시점 현재 달(클라이언트 로컬 `YYYY-MM`)과 `data-date` 접두사가 다른 카드는 `.compact`(설명·경로 숨김, 제목+날짜+태그만)로 축약해 하단 `#archive` 섹션으로 이동. 그룹핑은 연 단위 기본, 한 해 12건 초과 시 그 해만 월 단위 분할. `?now=YYYY-MM` URL 파라미터로 현재 달 오버라이드 가능(검증용). 헤드리스 Chrome DOM 덤프로 기본(아카이브 숨김)·과거 달 축약·월 분할 경로 모두 검증.
- **T-9 두 세션 플랜 파이프라인 페이지 추가** — Claude Code 를 생산자·소비자 두 세션으로 나눠 쓰는 작업 방식(한쪽은 `/add-plan`, 다른 쪽은 `/follow-plan`·`/parallel-plan`)과 각 플랜 스킬의 용도를 인라인 SVG 다이어그램으로 설명한 자체 완결형 페이지를 `2026-07-plan-pipeline/index.html` 로 저장. 루트 갤러리·README 표 함께 갱신.

### 진행 중 / 다음

- **T-15 방문 지표 — Cloudflare Web Analytics** — 정적 공개 사이트라 서버 로그가 없으므로 클라이언트 비콘으로 **익명 집계**(페이지뷰·리퍼러·지역·디바이스·시각)를 수집한다. Cloudflare Web Analytics 를 도입한다: CF 계정에 사이트 등록 → beacon 토큰 발급 → JS beacon 스크립트(`static.cloudflareinsights.com/beacon.min.js`, cookieless)를 루트 `index.html` 과 모든 `<slug>/index.html` 에 삽입. GitHub Pages 호스팅이라 CF 프록시 없이 beacon 방식으로 동작한다. beacon 토큰은 클라이언트 임베드용 공개 값이라 public repo 커밋 무방하나 확인 후 넣는다. 지표는 **CF 기본 대시보드**로 확인하고 사이트 내 커스텀 대시보드는 만들지 않는다. **신규 페이지에도 자동 반영되도록** beacon 삽입을 퍼블리시 런북([AGENTS.md](AGENTS.md))과 `publish-gh-pages` 스킬·페이지 템플릿에 넣는다. 완료 조건: 전 페이지에 beacon 존재 + CF 대시보드에 방문 데이터 집계 확인.
- **T-16 (리서치/결정) 블로그 프레임워크 도입 검토** — 현행 "artifact 당 자체 완결형 HTML 디렉터리" 방식을 유지할지, 블로그/정적 사이트 생성기(Jekyll — GitHub Pages 네이티브 지원 / Astro / Hugo / Eleventy 등)로 전환할지 비교·결정한다. 평가 축: 현재 퍼블리시 워크플로(claude.ai artifact 를 그대로 옮기는 흐름)와의 적합성, 마이그레이션 비용(기존 페이지 보존·URL 유지), 빌드 도입에 따른 운영 부담, 태그/주제 분류·아카이브(T-11/T-14)·OG 메타(I-3)·분석(T-15) 통합 이득. **결과물은 권고안(도입/유지 + 근거)까지이며 실제 마이그레이션은 하지 않는다**(도입으로 결정되면 후속 태스크로 분리).

- **T-17 AI 요약 표시를 서브헤딩 스타일로** — T-12 가 루트 `index.html` `<!-- AI-SUMMARY:START/END -->` 마커에 주입하는 AI 요약을 **카드 형식이 아니라 최상단 서브헤딩 느낌의 가벼운 텍스트 블록**으로 바꾼다(카드 배경·테두리·그림자 없이 제목 소자막 + 한두 줄 요약 정도). nuc14 `~/jobs/docs-ai-summary/inject.py` 의 요약 마크업 템플릿과 이미 주입돼 있는 index.html 결과물을 함께 손본다. 정확한 룩은 자유 재량(라이트/다크·자체 완결 유지). T-12 산출물의 표시 형식만 조정하며 요약 파이프라인 로직은 건드리지 않는다.

- **T-19 (단독) 사이트 전체 디자인 방향 제안** — 사이트 전체 비주얼 방향(무드·컬러 팔레트·타이포·여백·레이아웃)을 아우르는 디자인 안 몇 가지(자유 재량, 보통 3안)를 제안한다. **결과물은 여러 안을 나란히 비교하는 단일 아티팩트 한 장** — 각 안의 무드보드·컬러·타이포·갤러리 목업 샘플을 한 페이지에서 비교하도록 만든다(실제 사이트 적용은 하지 않음, 방향 선택용). 루트 갤러리 + 개별 페이지 공통 룩을 함께 다룬다. 이 제안이 진행 중 레이아웃 태스크(T-11·T-14·T-17·T-18)의 최종 룩을 가늠하는 기준이 되므로 그 전에 방향을 잡아두면 좋다. **(단독 진행 — 에이전트 팀/parallel-plan 으로 나누지 않고 단일 세션에서 처리한다.)**

- 위 태스크 외 다음 `/publish-pages` 요청 대기 중. 새 페이지는 [AGENTS.md](AGENTS.md) "퍼블리시 런북" 을 따른다.

### 블록됨 (blocked)

- **T-18 (blocked) 갤러리 다단 칼럼 레이아웃** — 현재 갤러리는 1단(`index.html` 의 `.grid { grid-template-columns: 1fr }`)이라 정보 밀도가 낮다. 반응형 다단 칼럼(예: 넓은 화면에서 2\~3열)으로 나눠 밀도를 높인다. **블록 사유:** 카드 축약·아카이브(T-11)·주제 분류(T-14)·AI 요약 서브헤딩(T-17) 이 레이아웃 구조를 바꾸므로, 그 작업들을 먼저 마친 뒤 최종 레이아웃 위에서 칼럼 분할을 다시 판단한다. 선행 중 T-11·T-14 완료, T-17 정리 후 해제.

## 아이디어 (보류)

- **I-1 저장소 전용 publish 커맨드** — 기존 `/publish-pages`(Naver Pages 배포)와 별개로, 이 저장소의 GitHub Pages 런북을 자동화하는 전용 슬래시 커맨드/워크플로 제작. 지금은 AGENTS.md 런북을 수동으로 따른다.
- **I-2 갤러리 검색** — 페이지가 많아지면 루트 갤러리에 검색 추가. (태그 필터는 T-14, 연도 구분은 T-11 로 구현됨.)
- **I-3 OG 메타/썸네일** — 각 페이지에 Open Graph 메타태그와 미리보기 이미지 추가(SNS 공유 대응).

## 참고

- 첫 페이지 원본: `https://claude.ai/code/artifact/6090be57-74eb-4ba3-8f49-938684820a72`
- 퍼블리시 계정: github.com `kil9` (gh CLI 인증됨, `repo` scope)
