#!/usr/bin/env node
// verify.mjs — drive a concept-lab page headless and fail on any contract breach.
// Usage: node verify.mjs ./lab.html [--out DIR]
// Exit 0 = every check held at phone and desktop size, with motion on and reduced.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const file = args.find(a => !a.startsWith('--'));
if (!file) { console.error('usage: node verify.mjs ./lab.html [--out DIR]'); process.exit(2); }
const outIdx = args.indexOf('--out');
const outDir = path.resolve(outIdx >= 0 ? args[outIdx + 1] : path.join(path.dirname(file), 'verify-shots'));
fs.mkdirSync(outDir, { recursive: true });
const abs = path.resolve(file);
const html = fs.readFileSync(abs, 'utf8');

// Playwright may be installed locally or only globally; a bare ESM import misses the global one.
function loadPlaywright() {
  const roots = [process.cwd(), path.dirname(abs)];
  try { roots.push(execSync('npm root -g', { encoding: 'utf8' }).trim()); } catch {}
  roots.push('/opt/npm-tools/node_modules');
  for (const r of roots) {
    try { return createRequire(path.join(r, 'x.js'))('playwright'); } catch {}
    try { return createRequire(path.join(r, 'x.js'))(path.join(r, 'playwright')); } catch {}
  }
  console.error('verify: playwright not found (looked in cwd, the page folder and the global npm root)');
  process.exit(2);
}
const { chromium } = loadPlaywright();

async function launch() {
  try { return await chromium.launch(); } catch (e) {
    const base = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
    const dirs = fs.existsSync(base) ? fs.readdirSync(base).filter(d => /^chromium-\d+$/.test(d)).sort() : [];
    for (const d of dirs.reverse()) {
      for (const rel of ['chrome-linux/chrome', 'chrome-linux64/chrome', 'chrome-win/chrome.exe']) {
        const exe = path.join(base, d, rel);
        if (fs.existsSync(exe)) return chromium.launch({ executablePath: exe });
      }
    }
    throw e;
  }
}

const failures = [];
const fail = (where, msg) => { failures.push(`[${where}] ${msg}`); };

// ---- static checks on the file ----
if (!/^\s*<!doctype html>/i.test(html)) fail('file', 'does not start with <!DOCTYPE html>');
if (!/<meta[^>]+name=["']viewport["']/i.test(html)) fail('file', 'no viewport meta tag');
const external = html.match(/<(script|img|iframe|video|audio|source)[^>]+src=["'](?:https?:)?\/\/[^"']+|<link[^>]+href=["'](?:https?:)?\/\/[^"']+|@import\s|url\(\s*["']?(?:https?:)?\/\//gi);
if (external) fail('file', `loads from outside the file: ${external.slice(0, 3).join(' | ')}`);
if (/Math\.random\s*\(/.test(html)) fail('file', 'uses Math.random() — route randomness through the seeded generator');

const SIZES = [
  { name: 'phone', width: 390, height: 700, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
  { name: 'desktop', width: 1280, height: 800, isMobile: false, hasTouch: false, deviceScaleFactor: 1 },
];
const BAD_TEXT = /\b(NaN|Infinity|undefined)\b/;
const MAX_STRONG_TEXT = 10;

// Runs in the page: everything the script needs to know about the current step.
function probe() {
  const vis = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
  const strength = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity || '1'); return o; };
  const view = document.querySelector('.view');
  const vr = view ? view.getBoundingClientRect() : null;
  const texts = view ? [...view.querySelectorAll('text')].filter(t => t.textContent.trim() && vis(t) && strength(t) > 0.05) : [];
  const boxes = texts.map(t => { const r = t.getBoundingClientRect(); return { s: t.textContent.trim().slice(0, 24), l: r.left, t: r.top, r: r.right, b: r.bottom, o: strength(t), el: t }; });
  const overlaps = [];
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    if (Math.min(a.r, b.r) - Math.max(a.l, b.l) > 2 && Math.min(a.b, b.b) - Math.max(a.t, b.t) > 2) overlaps.push(`"${a.s}" and "${b.s}"`);
  }
  const outside = vr ? boxes.filter(b => b.l < vr.left - 1 || b.r > vr.right + 1 || b.t < vr.top - 1 || b.b > vr.bottom + 1).map(b => b.s) : [];
  const covered = boxes.filter(b => { const top = document.elementFromPoint((b.l + b.r) / 2, (b.t + b.b) / 2); return top && top !== b.el && !b.el.contains(top) && view.contains(top); }).map(b => b.s);
  const controls = [...document.querySelectorAll('button, input:not([type=hidden]), select')].filter(vis);
  const hit = (el) => (el.matches('input[type=checkbox], input[type=radio]') ? (el.closest('label') || el) : el).getBoundingClientRect();
  const small = controls.map(el => ({ n: el.id || el.dataset.preset || el.textContent.trim().slice(0, 20), r: hit(el) })).filter(c => c.r.height < 43.5 || c.r.width < 43.5).map(c => `${c.n} ${Math.round(c.r.width)}×${Math.round(c.r.height)}`);
  const offscreen = controls.filter(el => { const r = el.getBoundingClientRect(); return r.bottom > innerHeight + 1 || r.top < -1; }).map(el => el.id || el.dataset.preset || el.textContent.trim().slice(0, 20));
  const status = document.querySelector('#status');
  return {
    at: window.__lab && typeof window.__lab.at === 'function' ? window.__lab.at() : null,
    card: status ? status.innerText.trim() : '',
    body: document.body.innerText,
    overlaps, outside, covered, small, offscreen,
    strong: boxes.filter(b => b.o > 0.85).length,
    viewH: vr ? vr.height : 0,
    sideways: document.documentElement.scrollWidth > innerWidth + 1,
    tall: document.documentElement.scrollHeight - innerHeight,
    presets: [...document.querySelectorAll('[data-preset]')].filter(vis).map(b => b.dataset.preset),
  };
}

const browser = await launch();
for (const size of SIZES) {
  for (const motion of ['no-preference', 'reduce']) {
    const where = `${size.name}/${motion === 'reduce' ? 'reduced' : 'motion'}`;
    const tag = `${size.name}${motion === 'reduce' ? '-reduced' : ''}`;
    const ctx = await browser.newContext({
      viewport: { width: size.width, height: size.height }, isMobile: size.isMobile,
      hasTouch: size.hasTouch, deviceScaleFactor: size.deviceScaleFactor, reducedMotion: motion,
    });
    const page = await ctx.newPage();
    page.on('console', m => m.type() === 'error' && fail(where, `console error: ${m.text()}`));
    page.on('pageerror', e => fail(where, `page error: ${e}`));
    page.on('request', r => { if (!/^(file|data|blob|about):/.test(r.url())) fail(where, `network request: ${r.url()}`); });
    await page.goto('file://' + abs);
    await page.waitForTimeout(300);

    // ---- structure ----
    const T = await page.evaluate(() => ({
      h1: document.querySelectorAll('h1').length,
      view: !!document.querySelector('.view'),
      status: !!document.querySelector('#status[aria-live]'),
      prev: !!document.querySelector('#prev'), next: !!document.querySelector('#next'),
      play: !!document.querySelector('#play'),
      inputs: [...document.querySelectorAll('input:not([type=hidden]), select, textarea')].length,
      nPresets: document.querySelectorAll('[data-preset]').length,
      lab: window.__lab ? { mode: window.__lab.mode, steps: window.__lab.steps, at: typeof window.__lab.at, checks: typeof window.__lab.checks } : null,
    }));
    if (T.h1 !== 1) fail(where, `expected one <h1>, found ${T.h1}`);
    if (!T.view) fail(where, 'no .view element (the main view)');
    if (!T.status) fail(where, 'no #status element with aria-live (the step card)');
    if (!T.lab || T.lab.checks !== 'function') fail(where, 'window.__lab.checks() is missing');
    const mode = T.lab && T.lab.mode;
    if (T.lab && !['computed', 'authored', 'mixed', 'watch'].includes(mode)) fail(where, `__lab.mode is "${mode}"`);
    const watch = mode === 'watch';
    const walk = T.prev && T.next;                       // guided walkthrough or watch page
    if (T.inputs > 2) fail(where, `${T.inputs} inputs/sliders (limit 2, and none for a beginner page)`);
    if (T.nPresets > 4) fail(where, `${T.nPresets} "what if" cases (limit 4)`);
    if (T.play && !watch && walk) fail(where, 'a walkthrough has a Play button (the reader sets the pace with Back/Next)');
    if (walk) {
      if (!(T.lab && T.lab.steps >= 5 && T.lab.steps <= 14) && !(watch && T.lab && T.lab.steps >= 3 && T.lab.steps <= 8)) fail(where, `__lab.steps is ${T.lab && T.lab.steps} (walkthrough 5–14, watch 3–8)`);
      if (T.lab && T.lab.at !== 'function') fail(where, 'window.__lab.at() is missing (it returns the current step, from 0)');
    } else if (!watch) {
      if (!T.inputs) fail(where, 'no #prev/#next and no input: the page is neither a walkthrough nor a free-play lab');
    }
    const steps = (T.lab && T.lab.steps) || 0;

    // ---- one step's checks ----
    const seen = new Set();
    const checkStep = async (label, shot) => {
      const P = await page.evaluate(probe);
      const say = (m) => { const k = `${label}: ${m}`; if (!seen.has(k)) { seen.add(k); fail(where, k); } };
      if (!P.card) say('the step card is empty');
      const bad = P.body.match(BAD_TEXT); if (bad) say(`"${bad[0]}" on screen`);
      if (P.viewH < 120) say(`main view is only ${Math.round(P.viewH)} px tall`);
      if (P.sideways) say('page scrolls sideways');
      for (const o of P.overlaps) say(`labels overlap: ${o}`);
      for (const o of P.outside) say(`label outside the view: "${o}"`);
      for (const o of P.covered) say(`label covered by a shape: "${o}"`);
      if (P.strong > MAX_STRONG_TEXT) say(`${P.strong} pieces of full-strength text in the view (limit ${MAX_STRONG_TEXT}) — dim or hide what this step does not need`);
      for (const c of P.small) say(`touch target under 44 px: ${c}`);
      if (size.name === 'phone') {
        if (P.tall > 1) say(`page is ${Math.round(P.tall)} px taller than the phone screen (no-scroll rule)`);
        for (const c of P.offscreen) say(`control off screen: ${c}`);
      }
      if (shot) await page.screenshot({ path: path.join(outDir, `shot-${tag}-${shot}.png`) });
      return P;
    };
    const settle = () => page.waitForTimeout(motion === 'reduce' ? 80 : 350);
    const walkToEnd = async (label, shootEach) => {
      for (let guard = 0; guard < 40; guard++) {
        const P = await checkStep(`${label} step ${((await page.evaluate(() => window.__lab.at())) + 1)}`, shootEach ? `${label === 'base' ? '' : label + '-'}step${String((await page.evaluate(() => window.__lab.at())) + 1).padStart(2, '0')}` : null);
        if (P.at >= steps - 1) return P;
        await page.click('#next'); await settle();
        const now = await page.evaluate(() => window.__lab.at());
        if (now !== P.at + 1) { fail(where, `${label}: Next went from step ${P.at + 1} to step ${now + 1}`); return P; }
      }
    };
    const runChecks = async (label) => {
      const checks = await page.evaluate(() => window.__lab.checks());
      if (!Array.isArray(checks) || !checks.length) fail(where, `${label}: __lab.checks() returned no checks`);
      else for (const c of checks) if (c.pass !== true) fail(where, `${label}: check failed: ${c.name}${c.detail ? ' — ' + c.detail : ''}`);
    };

    if (walk && T.lab && T.lab.at === 'function' && steps) {
      const first = await page.evaluate(probe);
      if (first.at !== 0) fail(where, `page opens on step ${first.at + 1}, not step 1`);
      if (first.presets.length && !watch) fail(where, '"what if" cases are visible on step 1 (show them on the last step)');
      await walkToEnd('base', true);
      await runChecks('base');
      // Back returns to the first state
      for (let i = 0; i < steps - 1; i++) { await page.click('#prev'); }
      await settle();
      const back = await page.evaluate(probe);
      if (back.at !== 0) fail(where, `Back ${steps - 1} times ends on step ${back.at + 1}`);
      else if (back.card !== first.card) fail(where, 'after going Back to step 1 the card differs from the first load');
      for (let i = 0; i < steps - 1; i++) { await page.click('#next'); }
      await settle();
      // every "what if" case, walked to its end
      const names = (await page.evaluate(probe)).presets;
      if (T.nPresets && !names.length) fail(where, 'no "what if" case is visible on the last step');
      for (const name of names) {
        await page.click(`[data-preset="${name}"]`); await settle();
        const end = await walkToEnd(name, false);
        await runChecks(`case "${name}"`);
        await page.screenshot({ path: path.join(outDir, `shot-${tag}-case-${name}.png`) });
        if (end && end.at < steps - 1) break;
      }
      if (watch && T.play) { await page.click('#restart').catch(() => {}); await page.click('#play'); await page.waitForTimeout(600); await page.click('#play'); await checkStep('play/pause', null); }
    } else {
      // ---- free-play lab: presets, every input to both ends, transport ----
      await checkStep('load', 'load');
      for (const b of await page.$$('[data-preset]')) {
        const name = await b.getAttribute('data-preset');
        await b.click(); await page.waitForTimeout(motion === 'reduce' ? 200 : 3000);
        await checkStep(`case "${name}"`, `case-${name}`);
        if (T.lab) await runChecks(`case "${name}"`);
      }
      for (const r of await page.$$('input[type=range]')) {
        for (const end of ['min', 'max']) {
          const v = await r.getAttribute(end);
          await r.evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }, v);
          if (T.play) { await page.click('#play'); await page.waitForTimeout(500); }
          await checkStep(`${(await r.getAttribute('id')) || 'range'} at ${end}`, null);
        }
      }
      for (const c of await page.$$('input[type=checkbox]')) for (let i = 0; i < 2; i++) { await c.evaluate(el => el.click()); await page.waitForTimeout(150); await checkStep('checkbox', null); }
      if (T.lab) await runChecks('after controls');
    }
    await ctx.close();
  }
}
await browser.close();

if (failures.length) {
  const uniq = [...new Set(failures)];
  console.error(`verify: FAIL (${uniq.length})`);
  for (const f of uniq) console.error('  ' + f);
  process.exit(1);
}
console.log(`verify: OK — phone and desktop, motion on and reduced. Screenshots in ${outDir}`);
console.log('Now look at the phone screenshots, step by step: is it clear where to look, does the card say what the highlight shows, is anything cramped?');
