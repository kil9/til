# PLAN — kil9/docs (GitHub Pages 퍼블리싱 저장소)

`/publish-pages` 로 넘어온 정적 페이지를 GitHub Pages 로 퍼블리시하는 저장소. 이 문서 하나로 현재 상태와 다음 할 일을 파악할 수 있게 유지한다. 커밋마다 갱신한다.

## 개요

- 목적: 자체 완결형 HTML 페이지를 디렉터리 단위로 호스팅하고, 루트 갤러리에서 모아 보여준다.
- 호스팅: GitHub Pages, `kil9/docs`(public), `main` 루트에서 직접 서빙.
- 라이브: <https://kil9.github.io/docs/>
- 퍼블리시 절차: [AGENTS.md](AGENTS.md) 의 "퍼블리시 런북" 을 정본으로 한다.

## 현재 상태

페이지 3건 퍼블리시됨. 루트 갤러리는 `data-date` 최신순 정렬(T-10) + 이번달 외 카드 축약·연/월 아카이브(T-11) + 주제 필터 칩(T-14) 적용, AI요약은 카드가 아닌 서브헤딩 스타일 텍스트 블록으로 표시(T-17), nuc14 에 일 1회 AI요약 잡 가동 중(T-12, cron 09:00 KST). 사이트 구조는 SSG 미도입·현행 자체 완결형 HTML 방식 유지로 결정(T-16). 사이트 디자인 방향 3안 비교 아티팩트 제작 완료(T-19, B안 「열람실」 권고 — 사용자 방향 선택 대기). 남은 태스크는 T-15·T-18·T-20 이며, 그 외에는 새 `/publish-pages` 요청이 오면 AGENTS.md 런북대로 페이지를 추가한다.

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
- **T-19 사이트 전체 디자인 방향 제안** — 3안 비교 아티팩트 1장 제작(방향 선택용, 사이트 적용 없음): A안 「플레인로그」(터미널 모노 인덱스·앰버 단일 액센트·행 단위 최고 밀도, T-18 불필요화·til 흡수 궁합 최상), B안 「열람실」(서고 카드 카탈로그 — 한지색+잉크 네이비+인주 레드, 명조 표제·점선 목차·낙관 「九」, 아카이브 정체성 정합), C안 「온에어」(주제색 듀오(핑크/시안) 포스터 벽·2-3열 카드 그리드로 T-18 자체 해소). 각 안에 무드 타일·라이트/다크 팔레트·타이포 페어링(시스템 폰트 스택 한정)·루트 갤러리 목업·개별 페이지 공통 헤더 목업(목업별 라이트/다크 토글)·태스크 궁합·리스크 수록, 말미에 비교표 + 권고. **권고: B안 「열람실」** (근거: 아카이브 정체성(T-11·T-12·T-20 와 정합), 웹폰트 불가 제약에서 유일하게 시스템 폰트만으로 차별화되는 명조 활용, kil9→낙관 「九」 인장). 아티팩트: <https://claude.ai/code/artifact/d06f3b11-6d72-4e62-877d-9ee3154165e6> — 방향 확정은 사용자 결정 대기, 확정 시 루트 갤러리 → 런북 템플릿 → 기존 페이지 소급(I-4) 순으로 적용 태스크 분리.
- **T-9 두 세션 플랜 파이프라인 페이지 추가** — Claude Code 를 생산자·소비자 두 세션으로 나눠 쓰는 작업 방식(한쪽은 `/add-plan`, 다른 쪽은 `/follow-plan`·`/parallel-plan`)과 각 플랜 스킬의 용도를 인라인 SVG 다이어그램으로 설명한 자체 완결형 페이지를 `2026-07-plan-pipeline/index.html` 로 저장. 루트 갤러리·README 표 함께 갱신.

### 진행 중 / 다음

- **T-15 방문 지표 — Cloudflare Web Analytics** — 정적 공개 사이트라 서버 로그가 없으므로 클라이언트 비콘으로 **익명 집계**(페이지뷰·리퍼러·지역·디바이스·시각)를 수집한다. Cloudflare Web Analytics 를 도입한다: CF 계정에 사이트 등록 → beacon 토큰 발급 → JS beacon 스크립트(`static.cloudflareinsights.com/beacon.min.js`, cookieless)를 루트 `index.html` 과 모든 `<slug>/index.html` 에 삽입. GitHub Pages 호스팅이라 CF 프록시 없이 beacon 방식으로 동작한다. beacon 토큰은 클라이언트 임베드용 공개 값이라 public repo 커밋 무방하나 확인 후 넣는다. 지표는 **CF 기본 대시보드**로 확인하고 사이트 내 커스텀 대시보드는 만들지 않는다. **신규 페이지에도 자동 반영되도록** beacon 삽입을 퍼블리시 런북([AGENTS.md](AGENTS.md))과 `publish-gh-pages` 스킬·페이지 템플릿에 넣는다. 완료 조건: 전 페이지에 beacon 존재 + CF 대시보드에 방문 데이터 집계 확인.
- **T-18 갤러리 다단 칼럼 레이아웃** — 현재 갤러리는 1단(`index.html` 의 `.grid { grid-template-columns: 1fr }`)이라 정보 밀도가 낮다. 반응형 다단 칼럼(예: 넓은 화면에서 2\~3열)으로 나눠 밀도를 높인다. 선행(T-11·T-14·T-17) 모두 완료되어 2026-07-11 블록 해제. T-19 디자인 방향 제안이 완료됐으므로(3안 비교, B안 권고) **사용자가 확정한 방향에 맞춰** 칼럼 분할 여부·형태를 판단한다 — A안이면 다단 불필요(행 인덱스), B안이면 1단 목차 유지(필요시 2단), C안이면 2\~3열 카드 그리드로 이 태스크 자체가 흡수된다.

- **T-20 (단독, 제안까지) 저장소 kil9/til 리네임 + 기존 til 흡수 방안 권고** — 이 저장소(`kil9/docs`)를 `kil9/til` 로 리네임하고, 기존 `kil9/til`(토픽별 마크다운 노트 저장소: docker/·git/·go/·vim/ 등, 약 22KB·29커밋, 최근 푸시 2026-04-02)의 내용을 이 저장소로 흡수하는 **단계별 실행 계획을 권고안(근거 포함)으로 제시**한다. **결과물은 권고안까지이며 실제 리네임·흡수·삭제·push 는 하지 않는다**(승인 후 후속 태스크로 분리). 권고안이 다뤄야 할 결정 사항(사용자 확정):
  - **이름 충돌 해소 순서** — `kil9/til` 이 이미 존재하므로 곧바로 rename 불가. 확정 방침: **기존 til 콘텐츠를 이 repo 로 먼저 흡수 → 기존 `kil9/til` 삭제 → `kil9/docs` 를 `kil9/til` 로 rename**. 각 단계의 GitHub 조작(`gh repo rename`/`gh repo delete`)과 순서 안전성(삭제 전 흡수 검증)을 명시한다.
  - **TIL 콘텐츠 흡수 형태** — 기존 til 노트의 중요성은 낮음. **아카이브 페이지 하나로** 만들어 기존 토픽별 마크다운을 열람만 가능하면 충분(갤러리·AI요약·아카이브 등 기존 기능과 깊게 통합할 필요 없음). 원본 `.md` 를 어떤 형태로 담을지(원본 md 보존 + 간단한 인덱스 페이지 / 정적 렌더 중 택1)를 권고한다. 히스토리 병합 여부(subtree 병합 vs 단순 파일 복사)도 근거와 함께 제안.
  - **리네임에 따른 URL 변경** — Pages 경로가 `kil9.github.io/docs/` → `kil9.github.io/til/` 로 바뀌고 기존 퍼블리시 페이지 URL 이 깨지는 것을 **수용**함(리다이렉트·custom domain 유지는 요구하지 않음). 다만 저장소 내 문서(README/AGENTS/PLAN·루트 index.html 등)의 `kil9/docs`·`kil9.github.io/docs` 문자열을 어디까지 갱신해야 하는지 범위를 정리한다.
  - **git remote / 로컬 정합** — rename 후 로컬 `origin` URL 갱신(`git remote set-url`), GitHub 자동 repo 리다이렉트로 인한 영향 등을 점검 항목으로 포함한다.
  - **(단독 진행 — 에이전트 팀/parallel-plan 으로 나누지 않고 단일 세션에서 처리한다.)**

- 위 태스크 외 다음 `/publish-pages` 요청 대기 중. 새 페이지는 [AGENTS.md](AGENTS.md) "퍼블리시 런북" 을 따른다.

### 블록됨 (blocked)

- (현재 없음 — T-18 은 T-17 완료로 블록 해제되어 "진행 중 / 다음" 으로 이동.)

## 아이디어 (보류)

- **I-1 저장소 전용 publish 커맨드** — 기존 `/publish-pages`(Naver Pages 배포)와 별개로, 이 저장소의 GitHub Pages 런북을 자동화하는 전용 슬래시 커맨드/워크플로 제작. 지금은 AGENTS.md 런북을 수동으로 따른다.
- **I-2 갤러리 검색** — 페이지가 많아지면 루트 갤러리에 검색 추가. (태그 필터는 T-14, 연도 구분은 T-11 로 구현됨.)
- **I-3 OG 메타/썸네일** — 각 페이지에 Open Graph 메타태그와 미리보기 이미지 추가(SNS 공유 대응).
- **I-4 공통 요소 소급 후처리 스크립트** — 기존 전 페이지(`*/index.html`)에 OG 메타·분석 beacon 등 공통 헤드 요소의 누락을 검사·삽입하는 경량 스크립트(빌드 시스템 없이). T-16 권고의 선택 보완안 — 페이지 10건 이상으로 늘 때 착수를 검토한다.

## 참고

- 첫 페이지 원본: `https://claude.ai/code/artifact/6090be57-74eb-4ba3-8f49-938684820a72`
- 퍼블리시 계정: github.com `kil9` (gh CLI 인증됨, `repo` scope)
