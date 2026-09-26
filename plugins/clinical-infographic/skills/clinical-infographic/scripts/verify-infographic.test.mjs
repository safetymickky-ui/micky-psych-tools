// node --test plugins/clinical-infographic/skills/clinical-infographic/scripts/*.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { staticCheck, visibleChunks, normalize } from './verify-infographic.mjs';

const SOURCE = `# PPGL preparation
*2026-07-11 · PubMed 15 · trials 4 · books 0*

Doxazosin 2 mg/day, titrated to at most 32 mg/day. Target seated BP <130/80 mmHg.
The PRESCRIPT RCT (n=134) found either agent acceptable.
Prolonged post-operative hypotension occurs in roughly 10% of patients [unverified].
Norepinephrine 5 µg/min.
`;
const page = (body) => `<!doctype html><html><head><title>PPGL</title><style>.k{color:red}</style></head><body>${body}</body></html>`;
const errors = (html) => staticCheck(SOURCE, html).filter((f) => f.level === 'error');

test('a faithful page passes', () => {
  const html = page(`<div class="k">Seated BP, mmHg</div><div class="v">&lt;130/80 mmHg</div>
    <p>Doxazosin 2&nbsp;mg/day → max 32 mg/day. PRESCRIPT RCT, n=134.</p>
    <p>Norepinephrine 5 mcg/min</p><footer>Rendered 2026-09-26</footer>`);
  assert.deepEqual(errors(html), []);
});

test('a number that is not in the source fails', () => {
  assert.equal(errors(page('<p>Doxazosin up to 16 mg/day</p>'))[0].check, 'number');
});

test('a unit that differs from the source fails (mg vs mcg)', () => {
  const e = errors(page('<p>Norepinephrine 5 mg/min</p>'));
  assert.equal(e[0].check, 'unit');
});

test('a design label the source never used fails', () => {
  const e = errors(page('<p>A meta-analysis found either agent acceptable.</p>'));
  assert.ok(e.some((f) => f.check === 'design-label'));
});

test('template residue in visible text fails', () => {
  assert.ok(errors(page('<p>{{TITLE}}</p>')).some((f) => f.check === 'leak'));
});

test('an [unverified] number needs a gap marker', () => {
  assert.ok(errors(page('<p>Hypotension in 10% of patients</p>')).some((f) => f.check === 'unverified'));
  assert.deepEqual(errors(page('<p>Hypotension in ~10% of patients [unverified in source]</p>')), []);
});

test('axis ticks (data-axis) and step numbers (data-ordinal) are exempt; comments are not visible text', () => {
  const html = page('<svg><g data-axis><text>0.25</text><text>0.75</text></g></svg><!-- 999 mg -->'
    + '<div class="tier"><span class="n" data-ordinal>7</span><span>Doxazosin 2 mg/day</span></div>');
  assert.deepEqual(errors(html), []);
  assert.ok(!visibleChunks(html).join(' ').includes('999'));
});

test('normalize maps unicode minus, thin spaces, thousands commas and µg', () => {
  assert.equal(normalize('−0.3 to 0.8'), '-0.3 to 0.8');
  assert.equal(normalize('1,000 µg'), '1000 mcg');
  assert.equal(normalize('7–14 days'), '7-14 days');
});
