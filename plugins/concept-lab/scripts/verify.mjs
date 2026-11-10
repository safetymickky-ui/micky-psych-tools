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
  { name: 'phone', width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
  { name: 'desktop', width: 1280, height: 800, isMobile: false, hasTouch: false, deviceScaleFactor: 1 },
];
const BAD_TEXT = /\b(NaN|Infinity|undefined)\b/;

const browser = await launch();
for (const size of SIZES) {
  for (const motion of ['no-preference', 'reduce']) {
    const where = `${size.name}/${motion === 'reduce' ? 'reduced' : 'motion'}`;
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

    const badText = async (after) => {
      const t = await page.evaluate(() => document.body.innerText);
      const m = t.match(BAD_TEXT);
      if (m) fail(where, `"${m[0]}" on screen after ${after}`);
    };

    // ---- structure and layout ----
    const L = await page.evaluate(() => {
      const box = (el) => { const r = el.getBoundingClientRect(); return { w: r.width, h: r.height, top: r.top + scrollY, bottom: r.bottom + scrollY }; };
      const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; };
      const view = document.querySelector('.view');
      const params = [...document.querySelectorAll('input:not([type=hidden]), select, textarea')].filter(vis);
      const presets = [...document.querySelectorAll('[data-preset]')].filter(vis);
      const buttons = [...document.querySelectorAll('button')].filter(vis);
      const firstControl = [...document.querySelectorAll('button, input, select')].filter(vis)[0];
      const hit = (el) => {                       // a checkbox or radio is judged by its label
        const t = el.matches('input[type=checkbox], input[type=radio]') ? (el.closest('label') || el) : el;
        return box(t);
      };
      const small = [...buttons, ...params].map(el => ({ el: el.id || el.dataset.preset || el.textContent.trim().slice(0, 20) || el.tagName, ...hit(el) }))
        .filter(b => b.h < 43.5 || b.w < 43.5);
      return {
        h1: document.querySelectorAll('h1').length,
        hasView: !!view, view: view && box(view),
        firstControl: firstControl && box(firstControl),
        nParams: params.length, nPresets: presets.length, small,
        hasStatus: !!document.querySelector('#status[aria-live]'),
        hasLab: !!(window.__lab && typeof window.__lab.checks === 'function'),
        sideways: document.documentElement.scrollWidth > innerWidth + 1,
        innerH: innerHeight,
      };
    });
    if (L.h1 !== 1) fail(where, `expected one <h1>, found ${L.h1}`);
    if (!L.hasView) fail(where, 'no .view element (the main view)');
    else if (L.view.h < 120) fail(where, `main view is only ${Math.round(L.view.h)} px tall (collapsed)`);
    if (!L.hasStatus) fail(where, 'no #status element with aria-live');
    if (!L.hasLab) fail(where, 'window.__lab.checks() is missing');
    const lab = L.hasLab ? await page.evaluate(() => ({ mode: window.__lab.mode, scenes: window.__lab.scenes })) : {};
    const watch = lab.mode === 'watch';
    if (L.hasLab && !['computed', 'authored', 'mixed', 'watch'].includes(lab.mode)) fail(where, `__lab.mode is "${lab.mode}" (computed | authored | mixed | watch)`);
    if (watch) {
      if (L.nParams > 0) fail(where, `watch mode has ${L.nParams} parameter controls (a page with controls is computed or authored mode)`);
      if (L.nPresets > 0) fail(where, 'watch mode has presets');
      for (const id of ['play', 'prev', 'next', 'restart']) if (!(await page.$('#' + id))) fail(where, `watch mode needs a #${id} button`);
      if (!(lab.scenes >= 3 && lab.scenes <= 8)) fail(where, `__lab.scenes is ${lab.scenes} (need 3–8)`);
    } else {
      if (L.nParams > 3) fail(where, `${L.nParams} parameter controls (limit 3)`);
      if (L.nPresets < 2 || L.nPresets > 4) fail(where, `${L.nPresets} presets (need 2–4)`);
    }
    if (L.sideways) fail(where, 'page scrolls sideways');
    for (const s of L.small) fail(where, `touch target "${s.el}" is ${Math.round(s.w)}×${Math.round(s.h)} px (minimum 44×44)`);
    if (size.name === 'phone') {
      if (L.view && L.view.bottom > L.innerH) fail(where, `main view ends at ${Math.round(L.view.bottom)} px, below the first screen (${L.innerH} px)`);
      if (L.firstControl && L.firstControl.bottom > L.innerH) fail(where, `first control ends at ${Math.round(L.firstControl.bottom)} px, below the first screen`);
    }
    await badText('load');

    // ---- presets ----
    for (const b of await page.$$('[data-preset]')) {
      const name = await b.getAttribute('data-preset');
      await b.click(); await page.waitForTimeout(motion === 'reduce' ? 200 : 3000);
      await page.screenshot({ path: path.join(outDir, `shot-${size.name}${motion === 'reduce' ? '-reduced' : ''}-${name}.png`) });
      await badText(`preset "${name}"`);
    }

    // ---- every control to both ends ----
    for (const r of await page.$$('input[type=range]')) {
      const id = (await r.getAttribute('id')) || 'range';
      for (const end of ['min', 'max']) {
        const v = await r.getAttribute(end);
        await r.evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }, v);
        if (await page.$('#play')) { await page.click('#play'); await page.waitForTimeout(500); }
        await badText(`${id} at ${end}`);
      }
    }
    for (const c of await page.$$('input[type=checkbox]')) {
      for (let i = 0; i < 2; i++) { await c.evaluate(el => el.click()); await page.waitForTimeout(150); await badText('checkbox toggle'); }
    }
    for (const s of await page.$$('select')) {
      const values = await s.evaluate(el => [...el.options].map(o => o.value));
      for (const v of values) { await s.selectOption(v); await page.waitForTimeout(150); await badText(`select ${v}`); }
    }

    // ---- watch mode: walk every scene, shoot its hold, then play it through ----
    if (watch && await page.$('#next')) {
      await page.click('#restart'); await page.waitForTimeout(200);
      for (let i = 1; i <= (lab.scenes || 0); i++) {
        await page.waitForTimeout(motion === 'reduce' ? 200 : 2500);
        const cap = (await page.textContent('#status') || '').trim();
        if (!cap) fail(where, `scene ${i} has an empty caption`);
        await page.screenshot({ path: path.join(outDir, `shot-${size.name}${motion === 'reduce' ? '-reduced' : ''}-scene${i}.png`) });
        await badText(`scene ${i}`);
        if (i < lab.scenes) await page.click('#next');
      }
      await page.click('#prev'); await page.click('#restart');
      await page.click('#play'); await page.waitForTimeout(600); await page.click('#play'); await badText('play/pause');
    }

    // ---- transport, when the lab has it ----
    if (await page.$('#reset')) {
      await page.click('#reset');
      if (await page.$('#step')) { await page.click('#step'); await page.click('#step'); await badText('step'); }
      if (await page.$('#play')) { await page.click('#play'); await page.waitForTimeout(400); await page.click('#play'); await badText('play/pause'); }
      await page.click('#reset'); await badText('reset');
    }

    // ---- the lab's own checks, on the values actually running ----
    if (L.hasLab) {
      const firstPreset = await page.$('[data-preset]');
      if (firstPreset) { await firstPreset.click(); await page.waitForTimeout(300); }
      const checks = await page.evaluate(() => window.__lab.checks());
      if (!Array.isArray(checks) || checks.length === 0) fail(where, '__lab.checks() returned no checks');
      else for (const c of checks) if (c.pass !== true) fail(where, `check failed: ${c.name}${c.detail ? ' — ' + c.detail : ''}`);
    }
    await ctx.close();
  }
}
await browser.close();

if (failures.length) {
  console.error(`verify: FAIL (${failures.length})`);
  for (const f of [...new Set(failures)]) console.error('  ' + f);
  process.exit(1);
}
console.log(`verify: OK — phone and desktop, motion on and reduced. Screenshots in ${outDir}`);
console.log('Now look at the phone screenshots: does each preset (or scene) show what its name (or caption) says?');
