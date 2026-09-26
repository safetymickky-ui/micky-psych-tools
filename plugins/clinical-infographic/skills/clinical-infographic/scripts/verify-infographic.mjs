#!/usr/bin/env node
// Fidelity check for a rendered clinical infographic (Step 2.6 of the clinical-infographic skill).
//
//   node verify-infographic.mjs --source report.md --html infographic.html [--render] [--pages N] [--json out.json]
//
// Static checks (always, no dependencies):
//   number       every number in the visible text appears in the source report (exempt: ISO
//                dates such as the render date, chart axis ticks marked data-axis on the <text>
//                or its <g>, and step numbers marked data-ordinal)
//   unit         a number with a unit on the page appears with that unit in the source (mcg = µg)
//   design-label a design word (RCT, meta-analysis, Cochrane, crossover…) is not on the page more
//                often than in the source
//   leak         no template residue ({{ }}, -->, TODO, lorem) in the visible text
//   unverified   a number the source only states inside an [unverified] sentence is not shown
//                without a gap marker
// Render checks (--render; needs Playwright, skipped with a note when it is not installed):
//   case         CSS text-transform does not change text that holds a number or a unit
//   print        A4 print page count (and <= --pages N when given); columns not stacked in print
//   external     the page makes no network request
//
// Exit 0 = no errors, 1 = errors found, 2 = bad usage. Numbers alone never prove fidelity: the
// claim ledger (qualifiers, populations, arms) is still owed after this script passes.
// Tests (run by hand; health.sh runs Python tests only): node --test <this directory>/*.test.mjs

import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';

const ENTITIES = {
  nbsp: ' ', amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", mdash: '—', ndash: '–',
  minus: '−', micro: 'µ', mu: 'μ', le: '≤', ge: '≥', times: '×', middot: '·', plusmn: '±',
  rarr: '→', larr: '←', uarr: '↑', darr: '↓', deg: '°', alpha: 'α', beta: 'β', hellip: '…',
  thinsp: ' ', ensp: ' ', emsp: ' ', lsquo: '‘', rsquo: '’', ldquo: '“', rdquo: '”', asymp: '≈',
};

export function decodeEntities(s) {
  return s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] === '#') {
      const cp = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(cp) ? String.fromCodePoint(cp) : m;
    }
    return ENTITIES[e.toLowerCase()] ?? m;
  });
}

// Visible text of an HTML file, one entry per block-ish chunk: text nodes, SVG <text>/<title>/<desc>,
// and aria-label / alt values. Comments, <style>, <script> and <head> metadata are dropped.
export function visibleChunks(html) {
  let s = html.replace(/<!--[\s\S]*?-->/g, ' ')
    // chart axis ticks are scale, not claims: mark them (or their <g>) with data-axis
    .replace(/<g\b[^>]*\bdata-axis\b[^>]*>[\s\S]*?<\/g>/gi, ' ')
    .replace(/<(text|span|div)\b[^>]*\bdata-(?:axis|ordinal)\b[^>]*>[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<(style|script|noscript)\b[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<head\b[\s\S]*?<\/head>/i, (h) => (h.match(/<title\b[^>]*>[\s\S]*?<\/title>/i) || [''])[0]);
  const labels = [];
  s = s.replace(/<[a-z][^>]*>/gi, (tag) => {
    for (const m of tag.matchAll(/\b(?:aria-label|alt)\s*=\s*("([^"]*)"|'([^']*)')/gi)) labels.push(m[2] ?? m[3]);
    return /^<(?:br|p|div|li|tr|td|th|h[1-6]|section|article|header|footer|summary|details|text|tspan|title|desc|figcaption|dt|dd)\b/i.test(tag) ? '\n' : ' ';
  }).replace(/<\/[a-z][^>]*>/gi, (tag) => (/^<\/(?:p|div|li|tr|td|th|h[1-6]|section|text|title|desc|summary|dt|dd)\b/i.test(tag) ? '\n' : ' '));
  return [...s.split('\n'), ...labels].map((c) => normalize(decodeEntities(c))).filter((c) => c.trim());
}

// Unicode minus / dashes between digits -> '-', exotic spaces -> ' ', thousands commas dropped,
// µg / μg -> mcg so a label written either way matches.
export function normalize(s) {
  return s.replace(/[\u00a0\u2007\u2009\u200a\u202f]/g, ' ')
    .replace(/(\d)\s*[\u2212\u2013\u2014]\s*(?=\d)/g, '$1-')
    .replace(/[\u2212]/g, '-')
    .replace(/(\d),(?=\d{3}(?:\D|$))/g, '$1')
    .replace(/[µμ]g\b/g, 'mcg')
    .replace(/[ \t]+/g, ' ');
}

const UNIT = String.raw`(?:mcg|mg|g|kg|ng|mL|ml|L|dL|mmol|µmol|mEq|IU|units?|mmHg|bpm|h|hr|hours?|min|days?|d|weeks?|wk|months?|years?|y|%)(?:\/(?:kg|day|d|h|min|L|dL|mL|m2|m²|dose|week|wk))*`;
const NUM_RE = new RegExp(String.raw`(?<![\w.])(\d+(?:\.\d+)?)(?:\s?(${UNIT})(?![A-Za-z]))?`, 'g');
const ISO_DATE = /\b\d{4}-\d{2}-\d{2}\b/g;

function numberSet(text) {
  const nums = new Set(), pairs = new Set(), unitsByNum = new Map();
  for (const m of text.replace(ISO_DATE, ' ').matchAll(NUM_RE)) {
    const n = canonNum(m[1]);
    nums.add(n);
    if (m[2]) {
      const u = canonUnit(m[2]);
      pairs.add(`${n} ${u}`);
      if (!unitsByNum.has(n)) unitsByNum.set(n, new Set());
      unitsByNum.get(n).add(u);
    }
  }
  return { nums, pairs, unitsByNum };
}
const canonNum = (n) => String(Number(n));
const UNIT_SYNONYMS = [[/^(hours?|hr)$/, 'h'], [/^(days?)$/, 'd'], [/^(weeks?|wk)$/, 'week'], [/^(months?)$/, 'month'],
  [/^(years?|y)$/, 'year'], [/^ml$/, 'mL'], [/^units?$/, 'unit'], [/^m²$/, 'm2']];
const canonUnit = (u) => u.split('/').map((part) => UNIT_SYNONYMS.reduce((x, [re, to]) => x.replace(re, to), part)).join('/');

const DESIGN_LABELS = [
  ['RCT', /\bRCTs?\b/g], ['randomised/randomized', /\brandomi[sz]ed\b/gi], ['meta-analysis', /\bmeta-?analys[ie]s\b/gi],
  ['systematic review', /\bsystematic reviews?\b/gi], ['Cochrane', /\bCochrane\b/g], ['crossover', /\bcross-?over\b/gi],
  ['cohort', /\bcohorts?\b/gi], ['double-blind', /\bdouble-?blind(?:ed)?\b/gi], ['placebo-controlled', /\bplacebo-controlled\b/gi],
  ['case-control', /\bcase-control\b/gi], ['guideline', /\bguidelines?\b/gi], ['Mendelian randomisation', /\bMendelian\b/gi],
];
const count = (re, s) => (s.match(new RegExp(re.source, re.flags)) || []).length;

export function staticCheck(sourceMd, html) {
  const findings = [];
  const add = (level, check, detail) => findings.push({ level, check, detail });
  const src = normalize(sourceMd);
  const chunks = visibleChunks(html);
  const page = chunks.join('\n');
  const S = numberSet(src);

  // number + unit
  for (const chunk of chunks) {
    for (const m of chunk.replace(ISO_DATE, ' ').matchAll(NUM_RE)) {
      const n = canonNum(m[1]);
      if (!S.nums.has(n)) { add('error', 'number', `"${m[0]}" is not in the source — in: "${clip(chunk)}"`); continue; }
      if (m[2]) {
        const u = canonUnit(m[2]);
        const srcUnits = S.unitsByNum.get(n);
        if (!S.pairs.has(`${n} ${u}`) && srcUnits && srcUnits.size) {
          add('error', 'unit', `"${m[0]}" — the source gives ${n} only as ${[...srcUnits].map((x) => `${n} ${x}`).join(', ')} — in: "${clip(chunk)}"`);
        }
      }
    }
  }

  // design labels
  for (const [name, re] of DESIGN_LABELS) {
    const p = count(re, page), s = count(re, src);
    if (p > 0 && s === 0) add('error', 'design-label', `"${name}" appears ${p}× on the page and never in the source`);
    else if (p > s) add('warn', 'design-label', `"${name}" appears ${p}× on the page but ${s}× in the source — check each use belongs to a study the source labels that way`);
  }

  // template leaks
  for (const [name, re] of [['{{ }}', /\{\{|\}\}/], ['-->', /-->|<!--/], ['TODO', /\bTODO\b|\bFIXME\b/], ['lorem', /\blorem ipsum\b/i]]) {
    const hit = chunks.find((c) => re.test(c));
    if (hit) add('error', 'leak', `template residue ${name} in visible text: "${clip(hit)}"`);
  }

  // [unverified] numbers
  const srcLines = src.split(/\n|(?<=[.!?])\s+/);
  const unverifiedOnly = new Set();
  for (const n of S.nums) {
    const re = new RegExp(String.raw`(?<![\w.])${n.replace('.', '\\.')}(?![\d])`);
    const lines = srcLines.filter((l) => re.test(l));
    if (lines.length && lines.every((l) => /\[unverified\]/i.test(l))) unverifiedOnly.add(n);
  }
  for (const chunk of chunks) {
    for (const m of chunk.replace(ISO_DATE, ' ').matchAll(NUM_RE)) {
      if (unverifiedOnly.has(canonNum(m[1])) && !/unverified|not verified|unconfirmed/i.test(chunk)) {
        add('error', 'unverified', `"${m[0]}" is [unverified] in the source but shown without a gap marker: "${clip(chunk)}"`);
      }
    }
  }
  return findings;
}

const clip = (s, n = 90) => (s.length > n ? `${s.slice(0, n - 1)}…` : s).trim();

async function loadPlaywright() {
  const tries = [() => import('playwright'), () => import('@playwright/test')];
  const roots = [...(process.env.NODE_PATH || '').split(/[:;]/).filter(Boolean)];
  try { roots.push(execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim()); } catch {}
  for (const root of roots) {
    tries.push(() => import(pathToFileURL(createRequire(resolve(root, 'noop.js')).resolve('playwright')).href));
  }
  for (const t of tries) { try { const m = await t(); return m.chromium ? m : m.default; } catch {} }
  return null;
}

export async function renderCheck(htmlPath, { pages } = {}) {
  const findings = [];
  const add = (level, check, detail) => findings.push({ level, check, detail });
  const pw = await loadPlaywright();
  if (!pw) { add('note', 'render', 'Playwright not found — render checks skipped; screenshot and print by hand'); return findings; }
  const browser = await pw.chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const external = [];
    await page.route('**/*', (route) => {
      const u = route.request().url();
      if (/^(file|data|about|blob):/.test(u)) return route.continue();
      external.push(u); return route.abort();
    });
    await page.goto(pathToFileURL(resolve(htmlPath)).href, { waitUntil: 'load' });
    for (const u of external) add('error', 'external', `network request: ${u}`);

    const transformed = await page.evaluate(() => {
      const out = [];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        const t = n.textContent.trim();
        if (!t || !/\d|[µμ]|\b(?:mcg|mg|mL|mmHg|mmol|mEq|IU|kg|bpm)\b/.test(t)) continue;
        const tt = getComputedStyle(n.parentElement).textTransform;
        if (tt && tt !== 'none') out.push(`${tt}: "${t.slice(0, 80)}"`);
      }
      return out;
    });
    for (const t of transformed) add('error', 'case', `CSS text-transform changes text holding a number or unit — ${t}`);

    const screenCols = await page.evaluate(() => {
      const c = document.querySelector('.columns');
      return c ? getComputedStyle(c).gridTemplateColumns.split(' ').filter(Boolean).length : 0;
    });
    await page.emulateMedia({ media: 'print' });
    await page.setViewportSize({ width: 794, height: 1123 });
    const printCols = await page.evaluate(() => {
      const c = document.querySelector('.columns');
      return c ? getComputedStyle(c).gridTemplateColumns.split(' ').filter(Boolean).length : 0;
    });
    if (screenCols > 1 && printCols === 1) add('error', 'print', `columns stack into one in print (${screenCols} on screen) — scope breakpoints to @media screen`);
    const pdf = await page.pdf({ format: 'A4', printBackground: true, preferCSSPageSize: true });
    const n = (pdf.toString('latin1').match(/\/Type\s*\/Page(?!s)/g) || []).length;
    if (pages && n > pages) add('error', 'print', `prints on ${n} A4 pages; the chosen format allows ${pages}`);
    else add('note', 'print', `prints on ${n} A4 page${n === 1 ? '' : 's'}`);
  } finally {
    await browser.close();
  }
  return findings;
}

function parseArgs(argv) {
  const a = { render: false };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === '--source') a.source = argv[++i];
    else if (k === '--html') a.html = argv[++i];
    else if (k === '--render') a.render = true;
    else if (k === '--pages') a.pages = Number(argv[++i]);
    else if (k === '--json') a.json = argv[++i];
    else return null;
  }
  return a.source && a.html ? a : null;
}

async function main() {
  const a = parseArgs(process.argv.slice(2));
  if (!a) {
    console.error('usage: verify-infographic.mjs --source <report.md> --html <infographic.html> [--render] [--pages N] [--json out.json]');
    process.exit(2);
  }
  const findings = staticCheck(readFileSync(a.source, 'utf8'), readFileSync(a.html, 'utf8'));
  if (a.render) findings.push(...await renderCheck(a.html, { pages: a.pages }));
  for (const f of findings) console.log(`${f.level.toUpperCase().padEnd(5)} ${f.check.padEnd(12)} ${f.detail}`);
  const errors = findings.filter((f) => f.level === 'error').length;
  const warns = findings.filter((f) => f.level === 'warn').length;
  console.log(`verify-infographic: ${errors} error(s), ${warns} warning(s)${a.render ? '' : ' (static only — add --render for case, print and network checks)'}`);
  if (a.json) writeFileSync(a.json, JSON.stringify({ errors, warns, findings }, null, 2));
  process.exit(errors ? 1 : 0);
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) main();
