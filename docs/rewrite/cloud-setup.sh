#!/bin/bash
# Cloud environment setup script for sessions that clone micky-psych-tools and learn-hub.
# Canonical copy: micky-psych-tools/docs/rewrite/cloud-setup.sh (spec S11, interface I16).
# Paste this whole file into the environment's "Setup script" field, then add a
# delivery-log row (variable setup-script) with the SETUP_VERSION below.
#
# Rules for this file:
# - VM tooling only. It may run before the repos are cloned, so nothing here reads
#   or writes /home/user/<repo>.
# - Every step is non-fatal: a non-zero exit stops the session from starting.
# - Output goes to /var/log/cloud-setup.log (kept in the environment cache).
SETUP_VERSION=1
LOG=/var/log/cloud-setup.log
exec >>"$LOG" 2>&1
echo "== cloud-setup start $(date -u +%Y-%m-%dT%H:%M:%SZ) setup_version=$SETUP_VERSION user=$(id -un)"
echo "-- /home/user at setup time (W0 check h: are the repos cloned yet?)"
ls -la /home/user || true
echo "-- tools: python3=$(command -v python3 || echo none) npm=$(command -v npm || echo none)"

# 1. PDF libraries for the python3 that learn-hub's scripts call.
python3 -m pip install --quiet --no-input pymupdf pypdf pdfplumber \
  || python3 -m pip install --quiet --no-input --break-system-packages pymupdf pypdf pdfplumber \
  || echo "WARN step 1 failed: pip install pymupdf pypdf pdfplumber"

# 2. poppler-utils: pdftoppm, pdftotext, pdfinfo.
apt-get install -y -qq poppler-utils \
  || { apt-get update -qq && apt-get install -y -qq poppler-utils; } \
  || echo "WARN step 2 failed: apt-get install -y poppler-utils"

# 3. Firecrawl CLI, pinned (OD12-a). Change the pin only together with a delivery-log row.
NPM="$(command -v npm || true)"
if [ -z "$NPM" ] && [ -x /opt/node22/bin/npm ]; then NPM=/opt/node22/bin/npm; fi
if [ -n "$NPM" ]; then
  "$NPM" install -g --no-audit --no-fund firecrawl-cli@1.24.4 \
    || echo "WARN step 3 failed: npm install -g firecrawl-cli@1.24.4"
else
  echo "WARN step 3 skipped: npm not found"
fi

# 4. Sandbox backend for eval runs that grant Bash: without bubblewrap and socat,
#    claude plugin eval refuses each Bash-granted run (eval-format.md:195; critique C2-02).
apt-get install -y -qq bubblewrap socat \
  || { apt-get update -qq && apt-get install -y -qq bubblewrap socat; } \
  || echo "WARN step 4 failed: apt-get install -y bubblewrap socat"

# --- W0 probe block (checks b and U7). Delete this block at W0 exit (set SETUP_VERSION=2). ---
P=/opt/w0-probe/hookprobe
mkdir -p "$P/.claude-plugin" "$P/hooks"
cat >"$P/.claude-plugin/plugin.json" <<'EOF'
{"name":"w0-hookprobe","version":"0.0.1","description":"W0 probe: records whether plugin SessionStart and PreToolUse(Bash) hooks fire and whether a userConfig default reaches the hook.","author":{"name":"W0 probe"},"keywords":["probe"],"userConfig":{"probe_dir":{"type":"directory","title":"Probe directory","description":"W0 check U7: is a userConfig default visible to an env-var-loaded plugin?","default":"/tmp"}}}
EOF
cat >"$P/hooks/hooks.json" <<'EOF'
{"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"bash","args":["${CLAUDE_PLUGIN_ROOT}/hooks/mark.sh"],"timeout":10}]}],"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"bash","args":["${CLAUDE_PLUGIN_ROOT}/hooks/pre.sh"],"timeout":10}]}]}}
EOF
cat >"$P/hooks/mark.sh" <<'EOF'
#!/bin/bash
echo "SessionStart $(date -u +%FT%TZ) root=${CLAUDE_PLUGIN_ROOT:-unset} project=${CLAUDE_PROJECT_DIR:-unset} pwd=$PWD env_file=${CLAUDE_ENV_FILE:-unset} remote=${CLAUDE_CODE_REMOTE:-unset} option_probe_dir=${CLAUDE_PLUGIN_OPTION_PROBE_DIR:-unset}" >>/tmp/w0-hookprobe.log
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then echo "export W0_PROBE_ENV=1" >>"$CLAUDE_ENV_FILE"; fi
exit 0
EOF
cat >"$P/hooks/pre.sh" <<'EOF'
#!/bin/bash
echo "PreToolUse $(date -u +%FT%TZ)" >>/tmp/w0-hookprobe.log
exit 0
EOF
# --- end of W0 probe block ---

echo "-- versions"
python3 -c "import importlib.metadata as m; print({p: m.version(p) for p in ('pymupdf', 'pypdf', 'pdfplumber')})" || true
pdftoppm -v 2>&1 | head -n 1 || true
command -v bwrap socat || true
"$(dirname "${NPM:-/opt/node22/bin/npm}")/firecrawl" --version || true
echo "== cloud-setup end $(date -u +%Y-%m-%dT%H:%M:%SZ) setup_version=$SETUP_VERSION"
exit 0
