#!/usr/bin/env node
/**
 * 렌더 기반 발행 점검(TASK-116). 페이지를 실제 브라우저에 띄워 파일만 봐서는 알 수 없는 것을
 * 확인한다 — 목차 레일이 본문을 침범하는지, 좁은 화면에서 목차가 사라지는지, 현재 절
 * 하이라이트가 도는지, 레일이 뷰포트를 넘치는지.
 *
 * site-check.py 와 역할이 다르다. 그쪽은 파일을 읽어 canonical·링크·용량을 보고 발행 경로에서
 * 매번 돈다(1초). 이쪽은 브라우저를 띄우므로 느리고(페이지당 수 초), UI 를 건드린 커밋에서만
 * 돌린다. impeccable 의 URL 스캔이 같은 일을 하지만 이 머신에서는 puppeteer 가 기본 샌드박스로
 * 죽어 못 쓴다 — 그래서 여기서는 --no-sandbox 로 직접 띄운다.
 *
 * puppeteer 를 찾지 못하면 skip 을 찍고 0 으로 끝난다. 발행을 막는 게이트가 아니다.
 *
 * 사용법:
 *   python3 -m http.server 8321 --bind 127.0.0.1 &
 *   node backlog/assets/render-check.mjs http://localhost:8321/2026/<slug>/ [...URL]
 */

import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';

const URLS = process.argv.slice(2).filter((a) => !a.startsWith('-'));
if (!URLS.length) {
  console.error('사용법: node backlog/assets/render-check.mjs <url> [url...]');
  process.exit(2);
}

// npx 캐시 경로에 해시가 박혀 있어 하드코딩하면 impeccable 이 갱신될 때마다 깨진다. 설치된
// 곳을 찾아 쓰고, 없으면 조용히 건너뛴다.
function findPuppeteer() {
  const require = createRequire(import.meta.url);
  const roots = [];
  try {
    const npx = execFileSync('bash', ['-c', 'ls -d ~/.npm/_npx/*/node_modules 2>/dev/null'], {
      encoding: 'utf-8',
    });
    roots.push(...npx.trim().split('\n').filter(Boolean));
  } catch {
    /* npx 캐시가 없을 수 있다 */
  }
  for (const root of [...roots, process.cwd()]) {
    try {
      return require.resolve('puppeteer', { paths: [root] });
    } catch {
      /* 다음 후보 */
    }
  }
  return null;
}

const entry = findPuppeteer();
if (!entry) {
  console.log('skip: puppeteer 를 찾지 못했다 — 렌더 점검을 건너뛴다');
  process.exit(0);
}
const { default: puppeteer } = await import(entry);

// 폭은 레일 분기(1200px)의 양쪽을, 높이는 짧은 창에서 레일이 넘치는지를 본다.
const VIEWS = [
  { w: 1440, h: 900, rail: true, label: '1440x900' },
  { w: 1440, h: 600, rail: true, label: '1440x600(짧은 창)' },
  { w: 1280, h: 900, rail: true, label: '1280x900(분기 바로 위)' },
  { w: 1199, h: 900, rail: false, label: '1199x900(분기 바로 아래)' },
  { w: 700, h: 900, rail: false, label: '700x900(모바일)' },
];

const problems = [];
const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});

for (const url of URLS) {
  for (const v of VIEWS) {
    const page = await browser.newPage();
    await page.setViewport({ width: v.w, height: v.h });
    await page.goto(url, { waitUntil: 'networkidle0' });
    // 절반쯤 내려가야 현재 절 하이라이트가 첫 절에서 벗어난다.
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.5));
    await new Promise((r) => setTimeout(r, 350));

    const m = await page.evaluate(() => {
      const toc = document.querySelector('.pagetoc');
      if (!toc) return { hasToc: false };
      const railToc = document.querySelector('main > .pagetoc');
      const main = document.querySelector('main');
      const cs = getComputedStyle(toc);
      const t = toc.getBoundingClientRect();
      const out = {
        hasToc: true,
        visible: t.width > 0 && t.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden',
        position: cs.position,
        current: !!document.querySelector('.pagetoc a.current'),
        railEligible: !!(railToc && main),
      };
      if (railToc && main && cs.position === 'absolute') {
        const mr = main.getBoundingClientRect();
        const inner = railToc.querySelector('.pagetoc-inner');
        const ir = inner.getBoundingClientRect();
        out.overlapsMain = t.right > mr.left + 1;
        out.offscreen = t.left < 0;
        out.railBottom = Math.round(ir.bottom);
        out.railOverflow = ir.bottom > window.innerHeight;
      }
      return out;
    });
    await page.close();

    const where = `${url} @${v.label}`;
    if (!m.hasToc) continue; // 목차 없는 글은 점검 대상이 아니다
    if (!m.visible) problems.push(`${where}: 목차가 보이지 않는다`);

    // <main> 이 없는 자체 스타일 페이지는 넓은 화면에서도 인라인이 정상이고, 하이라이트
    // 스크립트도 `main > .pagetoc` 을 못 찾아 돌지 않는다. 그쪽을 위반으로 세면 안 된다.
    const wantRail = v.rail && m.railEligible;
    if (m.railEligible && !m.current) {
      problems.push(`${where}: 현재 절 하이라이트가 붙지 않았다`);
    }
    if (wantRail && m.position !== 'absolute') {
      problems.push(`${where}: 레일로 전환되지 않았다(position=${m.position})`);
    }
    if (!v.rail && m.position !== 'static') {
      problems.push(`${where}: 인라인 폴백이 아니다(position=${m.position})`);
    }
    if (m.overlapsMain) problems.push(`${where}: 레일이 본문을 침범한다`);
    if (m.offscreen) problems.push(`${where}: 레일이 화면 왼쪽 밖으로 나갔다`);
    if (m.railOverflow) {
      problems.push(`${where}: 레일이 뷰포트를 넘친다(bottom=${m.railBottom} > ${v.h})`);
    }
  }
}

await browser.close();

console.log(`렌더 점검 ${URLS.length}페이지 x ${VIEWS.length}조건`);
if (problems.length) {
  console.error(`\n위반 ${problems.length}건:`);
  for (const p of problems) console.error(`  ✗ ${p}`);
  process.exit(1);
}
console.log('위반 없음');
