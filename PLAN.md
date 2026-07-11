# PLAN — kil9/til (GitHub Pages 퍼블리싱 저장소)

`/publish-pages` 로 넘어온 정적 페이지를 GitHub Pages 로 퍼블리시하는 저장소. 이 문서 하나로 현재 상태와 다음 할 일을 파악할 수 있게 유지한다. 커밋마다 갱신한다.

## 개요

- 목적: 자체 완결형 HTML 페이지를 디렉터리 단위로 호스팅하고, 루트 갤러리에서 모아 보여준다.
- 호스팅: GitHub Pages, `kil9/til`(public, 2026-07-11 `kil9/docs` 에서 리네임), `main` 루트에서 직접 서빙.
- 라이브: <https://kil9.github.io/til/>
- 퍼블리시 절차: [AGENTS.md](AGENTS.md) 의 "퍼블리시 런북" 을 정본으로 한다.

## 현재 상태

페이지 3건 퍼블리시됨. 루트 갤러리는 `data-date`(날짜+시각, `YYYY-MM-DDTHH:MM`) 최신순 정렬(T-10, 카드에 시각까지 표시) + 이번달 외 카드 축약·연/월 아카이브(T-11, `/til-archive/` 는 구 til repo 마지막 업데이트 `2026-04-02` 기준으로 아카이브 하단 배치) + 주제 필터 칩(T-14) 적용, AI요약은 히어로(구 lede 자리)에 작은 라벨 + 안내 톤 요약문으로 표시(T-17, 페이지 목록은 제거하고 아래 갤러리 카드로 대체), nuc14 에 일 1회 AI요약 잡 가동 중(T-12, cron 09:00 KST, 모델 sonnet — `inject.py` 템플릿은 index.html 히어로의 AI-SUMMARY 블록과 반드시 일치시켜야 다음 cron 이 되돌리지 않는다). 사이트 구조는 SSG 미도입·현행 자체 완결형 HTML 방식 유지로 결정(T-16). 사이트 디자인 방향 검토(T-19)는 제안 전부 폐기·현행 룩 유지로 종결(검토 내역은 I-5). 저장소는 2026-07-11 `kil9/docs` 에서 `kil9/til` 로 리네임 완료(T-20 권고 → T-21 실행: 기존 til 노트는 `/til-archive/` 로 흡수, 원 저장소 삭제, 라이브 URL 은 `https://kil9.github.io/til/` 로 변경). 남은 태스크는 T-15·T-18 이며, 그 외에는 새 `/publish-pages` 요청이 오면 AGENTS.md 런북대로 페이지를 추가한다.

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
- **T-16 (리서치/결정) 블로그 프레임워크 도입 검토** — 결과: **현행 "artifact 당 자체 완결형 HTML 디렉터리" 방식 유지(SSG 미도입)**. 근거: ① claude.ai artifact 는 이미 완성된 standalone HTML 이라 SSG(본문+템플릿→HTML 생성 모델)에 넣으려면 프론트매터+콘텐츠로 역분해가 필요해 워크플로가 오히려 한 단계 늘어남 ② 정렬·아카이브·필터 칩 등 동적 기능은 T-10/T-11/T-14 클라이언트 JS 로 이미 구현돼 빌드 타임 렌더링 이점이 상쇄됨 ③ Jekyll 외 SSG(Astro/Hugo/Eleventy)는 GitHub Actions 빌드 필수(새 CI 실패 지점)이고, 어떤 SSG 든 루트 index.html 이 빌드 산출물이 되어 nuc14 AI요약 직접 주입(T-12)과 소스/산출물 이중화 충돌 발생 ④ 남은 "전 페이지 공통 삽입" 수요(OG 메타 I-3·분석 beacon T-15)는 SSG 없이 런북 템플릿 강화로 충분. 재평가 트리거: 페이지가 수십 건 이상으로 늘고 공통 룩 변경이 수동 유지보수 병목이 되면 Jekyll(유일한 무빌드·네이티브 서빙 SSG)에 한해 재검토. 소급 공통 삽입용 경량 후처리 스크립트는 I-4 로 보류.
- **T-17 AI 요약 표시를 서브헤딩 스타일로** — 루트 `index.html` 의 AI요약 섹션을 카드(배경·테두리·그림자)에서 eyebrow 라벨(`AI 요약` + 날짜) + 요약 문단 + 불릿 없는 링크 리스트의 가벼운 텍스트 블록으로 변경. nuc14 `~/jobs/docs-ai-summary/inject.py` 의 주입 템플릿도 동일 마크업으로 갱신하고 스크래치 복사본에 실제 주입을 실행해 검증. Firefox 헤드리스 스크린샷으로 라이트/다크 렌더링 모두 확인. 요약 파이프라인 로직은 변경 없음.
- **T-19 사이트 전체 디자인 방향 제안** — 1차 3안(A 플레인로그 / B 열람실 / C 온에어) 비교 아티팩트와 2차 A안 세부 3안(A-1 레저 / A-2 TTY / A-3 관제실) 비교 아티팩트를 제작해 제안. 결과: **제안 전부 폐기, 현행 룩 유지**(사용자 결정, 2026-07-11). 검토 내역과 아티팩트 링크는 [I-5](#아이디어-보류) 로 보류 이관.
- **T-9 두 세션 플랜 파이프라인 페이지 추가** — Claude Code 를 생산자·소비자 두 세션으로 나눠 쓰는 작업 방식(한쪽은 `/add-plan`, 다른 쪽은 `/follow-plan`·`/parallel-plan`)과 각 플랜 스킬의 용도를 인라인 SVG 다이어그램으로 설명한 자체 완결형 페이지를 `2026-07-plan-pipeline/index.html` 로 저장. 루트 갤러리·README 표 함께 갱신.
- **T-20 (제안까지) 저장소 kil9/til 리네임 + 기존 til 흡수 방안 권고** — 권고안 제시 완료(2026-07-11). **실행은 하지 않았다** — 사용자 승인 후 후속 태스크로 분리한다. 조사 근거: 기존 `kil9/til` 은 파일 26개(토픽 노트 22개·12개 토픽 + README/AGENTS/CLAUDE/.vimrc 메타 4개, 총 약 26KB)·29커밋(2016\~2026)·스타/포크/이슈 0·Pages 미사용·브랜치 main 단일; 이 repo 의 `kil9/docs` 문자열은 README 6곳·AGENTS 5곳·루트 index.html 1곳(footer)·PLAN 다수이며 개별 `<slug>/index.html` 에는 자기참조 없음; nuc14 AI요약 잡은 clone 의 origin URL 만 걸려 있고 run.sh/extract.py/inject.py 에 하드코딩 없음; 현재 gh 토큰 scope 에 `delete_repo` 없음. **권고 실행 계획(5단계)**:
  - **P0 백업** — 삭제는 영구 조치이므로 실행 전 `git clone --mirror https://github.com/kil9/til` 후 `git bundle create til-YYYYMMDD.bundle --all` 로 전체 히스토리 번들을 로컬 보관(공개 repo 에는 커밋하지 않음). GitHub 지원의 90일 복구는 rename 으로 이름이 즉시 재사용되면 막히므로 번들이 실질적 안전장치다.
  - **P1 흡수** — **정적 렌더 단일 아카이브 페이지** `til-archive/index.html` 채택(택1 중 정적 렌더). 근거: ① 사이트 컨벤션(자체 완결형 HTML 디렉터리)과 일치 ② Pages legacy 빌드는 front matter 없는 `.md` 를 raw 텍스트로 서빙해 "원본 md + 인덱스" 안은 열람성이 나쁨 ③ 총 26KB·동결 콘텐츠라 1회 변환으로 끝나고 재생성 파이프라인 불필요. 26개 노트를 토픽별 섹션 + 페이지 내 목차로 렌더. 슬러그는 rename 후 `kil9.github.io/til/til/` 중복을 피해 `til-archive` 로. 히스토리는 **subtree 병합 비권고, 단순 복사(렌더) 채택** — 29커밋이 퍼블리시 repo 히스토리에 섞이는 노이즈 대비 노트 중요도가 낮고, 히스토리 보존은 P0 번들이 담당. 갤러리 카드 추가(`data-topic="til"` 신규 키) — AI요약 잡이 다음 실행에서 신규 slug 로 1회 요약에 포함하는 것은 무해하므로 수용. 검증: 원본 26개 파일 대 페이지 섹션 전수 대조 + 로컬 http.server 렌더 확인 + push 후 라이브 200.
  - **P2 기존 til 삭제** — 게이트: P0 번들 존재 + P1 라이브 200·전수 대조 통과 후에만. `gh auth refresh -h github.com -s delete_repo`(현 토큰에 없음) → `gh repo delete kil9/til --yes`. 삭제 즉시 이름이 해제된다.
  - **P3 리네임** — `gh repo rename til -R kil9/docs --yes`. github.com 쪽(웹·git 원격)은 `kil9/docs` → `kil9/til` 자동 리다이렉트가 생기지만 **Pages URL 은 리다이렉트 없이 404**(수용 확정). Pages 설정은 유지된 채 `https://kil9.github.io/til/` 로 재빌드 — `gh api repos/kil9/til/pages` 로 확인. 주의: 이후 `kil9/docs` 이름의 repo 를 새로 만들면 리다이렉트가 끊긴다.
  - **P4 문자열·로컬 정합** — rename 직후 1커밋으로: README 6곳·AGENTS 5곳·루트 index.html footer 1곳 갱신, PLAN 은 살아있는 참조(제목·개요·현재 상태)만 갱신하고 완료 태스크의 과거 사실 서술(T-5·T-6·T-13 등)은 그대로 둔다. 개별 페이지는 갱신 불필요. 로컬: 이 클론과 nuc14 잡 클론(`~/jobs/docs-ai-summary/repo`) 모두 `git remote set-url origin https://github.com/kil9/til.git`(리다이렉트로 당장은 동작하나 명시 갱신), crontab 코멘트 문구 갱신. 작업 디렉터리 `~/work/kil9/docs` → `~/work/kil9/til` 이동은 선택 — Claude Code 프로젝트 설정·auto-memory 가 경로 키라 이동 시 memory 디렉터리 이관 필요함을 유의.
- **T-21 til 리네임·흡수 실행 (T-20 권고안 승인, 2026-07-11 완료)** — P0 백업: `~/backup/til-20260711.bundle`(전체 히스토리, verify 통과). P1 흡수: `til-archive/index.html` 에 22개 노트(12개 토픽)+부록 `.vimrc` 정적 렌더, 22/22 전수 대조·태그 정합·앵커 검사·헤드리스 Firefox 라이트/다크 렌더 확인, 갤러리 카드(`data-topic="til"`)·README 표 갱신, `zsh/ctrl-r.md` 의 사내 서버 절대경로는 `~/` 로 일반화, til 의 AGENTS/CLAUDE/README 메타 문서는 페이지 구성으로 대체. P2 삭제: 사용자가 `delete_repo` scope 인증 후 `gh repo delete kil9/til`. P3 리네임: `gh repo rename til -R kil9/docs` → Pages `https://kil9.github.io/til/` 재빌드 확인. P4 정합: README·AGENTS(구조도 포함)·루트 index.html(title/h1/footer)·til-archive footer·PLAN 살아있는 참조 갱신, 두 클론 `git remote set-url`, crontab 코멘트 갱신. 작업 디렉터리 이동(`~/work/kil9/docs` → `til`)도 사용자 지시로 완료: `~/.claude/projects/-home-kil9-work-kil9-docs` 를 `-til` 로 이관(구 키는 당시 진행 중이던 세션의 전사 기록용 심볼릭 링크로 유지 — 세션 종료 후 `rm ~/.claude/projects/-home-kil9-work-kil9-docs` 로 제거 가능), `~/.claude.json` 의 projects 키 갱신, `~/work/kil9/docs` 호환 링크는 검증 후 제거.

### 진행 중 / 다음

- **T-15 방문 지표 — Cloudflare Web Analytics** — 정적 공개 사이트라 서버 로그가 없으므로 클라이언트 비콘으로 **익명 집계**(페이지뷰·리퍼러·지역·디바이스·시각)를 수집한다. Cloudflare Web Analytics 를 도입한다: CF 계정에 사이트 등록 → beacon 토큰 발급 → JS beacon 스크립트(`static.cloudflareinsights.com/beacon.min.js`, cookieless)를 루트 `index.html` 과 모든 `<slug>/index.html` 에 삽입. GitHub Pages 호스팅이라 CF 프록시 없이 beacon 방식으로 동작한다. beacon 토큰은 클라이언트 임베드용 공개 값이라 public repo 커밋 무방하나 확인 후 넣는다. 지표는 **CF 기본 대시보드**로 확인하고 사이트 내 커스텀 대시보드는 만들지 않는다. **신규 페이지에도 자동 반영되도록** beacon 삽입을 퍼블리시 런북([AGENTS.md](AGENTS.md))과 `publish-gh-pages` 스킬·페이지 템플릿에 넣는다. 완료 조건: 전 페이지에 beacon 존재 + CF 대시보드에 방문 데이터 집계 확인.
- **T-18 갤러리 다단 칼럼 레이아웃** — 현재 갤러리는 1단(`index.html` 의 `.grid { grid-template-columns: 1fr }`)이라 정보 밀도가 낮다. 반응형 다단 칼럼(예: 넓은 화면에서 2\~3열)으로 나눠 밀도를 높인다. 선행(T-11·T-14·T-17) 모두 완료되어 2026-07-11 블록 해제. T-19 는 현행 룩 유지로 종결됐으므로, 현재 카드 레이아웃 위에서 칼럼 분할 여부·형태를 판단한다.

- 위 태스크 외 다음 `/publish-pages` 요청 대기 중. 새 페이지는 [AGENTS.md](AGENTS.md) "퍼블리시 런북" 을 따른다.

### 블록됨 (blocked)

- (현재 없음 — T-18 은 T-17 완료로 블록 해제되어 "진행 중 / 다음" 으로 이동.)

## 아이디어 (보류)

- **I-1 저장소 전용 publish 커맨드** — 기존 `/publish-pages`(Naver Pages 배포)와 별개로, 이 저장소의 GitHub Pages 런북을 자동화하는 전용 슬래시 커맨드/워크플로 제작. 지금은 AGENTS.md 런북을 수동으로 따른다.
- **I-2 갤러리 검색** — 페이지가 많아지면 루트 갤러리에 검색 추가. (태그 필터는 T-14, 연도 구분은 T-11 로 구현됨.)
- **I-3 OG 메타/썸네일** — 각 페이지에 Open Graph 메타태그와 미리보기 이미지 추가(SNS 공유 대응).
- **I-4 공통 요소 소급 후처리 스크립트** — 기존 전 페이지(`*/index.html`)에 OG 메타·분석 beacon 등 공통 헤드 요소의 누락을 검사·삽입하는 경량 스크립트(빌드 시스템 없이). T-16 권고의 선택 보완안 — 페이지 10건 이상으로 늘 때 착수를 검토한다.
- **I-5 사이트 리디자인 (T-19 검토 내역 보관)** — 2026-07-11 T-19 에서 디자인 방향을 검토했으나 제안 전부 폐기, 현행 룩(웜 크림+오렌지 카드 갤러리, 페이지별 주제 팔레트) 유지로 결정. 검토했던 안: 1차 3안 — A 「플레인로그」(터미널 모노 인덱스·앰버 액센트·행 단위 밀도), B 「열람실」(서고 카드 카탈로그 — 명조 표제·점선 목차·낙관 「九」), C 「온에어」(주제색 듀오 포스터 벽·다단 카드 그리드); 2차 A안 세부 3안 — A-1 「레저」(인쇄물·man page 표제), A-2 「TTY」(프롬프트+블록 커서·앰버 인광), A-3 「관제실」(TUI 패널·ANSI 토픽 컬러·키보드 내비). 아티팩트: [1차 비교](https://claude.ai/code/artifact/d06f3b11-6d72-4e62-877d-9ee3154165e6) · [2차 A안 세부](https://claude.ai/code/artifact/5a8e39e2-a822-419e-ac8f-b5c740b44008). 추후 리디자인을 착수하게 되면 이 검토를 출발점으로 재활용한다.

## 참고

- 첫 페이지 원본: `https://claude.ai/code/artifact/6090be57-74eb-4ba3-8f49-938684820a72`
- 퍼블리시 계정: github.com `kil9` (gh CLI 인증됨, `repo` scope)
