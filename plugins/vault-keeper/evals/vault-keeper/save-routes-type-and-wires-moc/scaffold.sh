#!/usr/bin/env bash
# Marketplace root with an initialised but empty vault (index.md = the init scaffold), plus
# the evidence report the prompt asks to file. Report facts: Cipriani 2013 BMJ meta-analysis
# (PubMed record fetched 2026-09-24).
set -euo pipefail
mkdir -p .claude-plugin vault/MOCs vault/notes vault/artifacts vault/assets
echo '{"name":"micky-psych-tools","owner":{"name":"fixture"},"plugins":[]}' > .claude-plugin/marketplace.json
touch vault/MOCs/.gitkeep vault/notes/.gitkeep vault/artifacts/.gitkeep vault/assets/.gitkeep
printf '# Vault Index\n\n' > vault/index.md
cat > lithium-suicide-prevention.md <<'EOF'
# Does lithium prevent suicide in mood disorders?
*2026-09-01 · PubMed 1 · trials 0 · books 0*

**Verdict: lithium lowers the risk of suicide in people with mood disorders; keep it in the maintenance plan where suicide risk is part of the picture.** Confidence: moderate — the effect rests on few events pooled across trials, not on a trial powered for suicide.

## What the trials show

An updated systematic review and meta-analysis pooled 48 randomised controlled trials (6674 participants, 15 comparisons) of lithium against placebo or active drugs in long-term treatment of unipolar and bipolar mood disorders. Lithium reduced the number of suicides compared with placebo (odds ratio 0.13, 95% CI 0.03 to 0.66) and deaths from any cause (0.38, 0.15 to 0.95). It showed no clear benefit over placebo for deliberate self-harm (0.60, 0.27 to 1.32). In unipolar depression it was associated with fewer suicides (0.36, 0.13 to 0.98) and fewer total deaths (0.13, 0.02 to 0.76).

## Sources

- Lithium and suicide prevention in mood disorders, meta-analysis of 48 RCTs — [doi:10.1136/bmj.f3646](https://doi.org/10.1136/bmj.f3646)
EOF
