#!/usr/bin/env python3
"""Check a session recap and render it as one self-contained HTML page.

    build_recap.py recap.json -o recap.html     check, then render
    build_recap.py recap.json --check           check only

The data shape and every rule are in ../references/recap-contract.md. The page is
rendered from ../assets/recap.template.html. Nothing is written when a rule is broken.

Output: one JSON object on stdout: {"ok", "errors", "warnings", "out"}.
Exit codes: 0 ok (warnings allowed), 1 a rule is broken, 2 usage error or unreadable input.

Stdlib only. `check(data)` and `render(data, template)` are importable.
"""
import argparse
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "recap.template.html")

STATUSES = ("done", "partial", "failed", "skipped", "running")
TYPES = ("change", "answer")
VERIFIED = ("yes", "no", "n/a")
OPEN_KINDS = ("todo", "question", "risk", "blocked")
OWNERS = ("user", "claude", "either")
BY = ("user", "claude", "default")
RESULTS = ("passed", "failed", "not run")
EVIDENCE_KINDS = ("file", "commit", "pr", "artifact", "command", "link", "other")
FILE_CHANGES = ("added", "modified", "deleted", "renamed")
PR_STATES = ("open", "merged", "closed", "draft")
MAX_FILES = 40
OUTCOME_CAP = 400
TITLE_CAP = 48

SECRET_PATTERNS = (
    ("an API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("a GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("an AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("a Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("a private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("a JSON web token", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}")),
    ("a password or key assignment",
     re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token|token)\b\s*[:=]\s*[\"']?(?=\S*\d)[^\s\"']{8,}")),
)
PRAISE = re.compile(
    r"(?i)\b(successfully|seamless(?:ly)?|robust(?:ly)?|perfect(?:ly)?|flawless(?:ly)?|"
    r"excellent|amazing|beautiful(?:ly)?|elegant(?:ly)?|great job)\b")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
SHA = re.compile(r"[0-9a-fA-F]{7,40}")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
CODE = re.compile(r"`([^`\n]+)`")

LABELS = {
    "en": {
        "eyebrow": "Session recap", "open": "Still open", "none_open": "Nothing is left open.",
        "done": "Done", "decisions": "Decisions", "checks": "Checks", "changes": "What changed",
        "asked": "What was asked", "gaps": "What this recap could not establish",
        "status": {"done": "Done", "partial": "Partly done", "failed": "Failed",
                   "skipped": "Skipped", "running": "Still running"},
        "kind": {"todo": "To do", "question": "Your decision", "risk": "Risk", "blocked": "Blocked"},
        "owner": {"user": "For you", "claude": "For Claude", "either": "For either"},
        "by": {"user": "You chose", "claude": "Claude chose", "default": "Default"},
        "result": {"passed": "Passed", "failed": "Failed", "not run": "Not run"},
        "verified_by": "Verified by", "not_verified": "Not verified by a check",
        "from_summary": "From a compacted part of the session",
        "prs": "Pull requests", "artifacts": "Artifacts", "commits": "Commits", "files": "Files",
        "external": "Sent or written outside",
        "change": {"added": "added", "modified": "changed", "deleted": "deleted", "renamed": "renamed"},
        "ev": {"file": "file", "commit": "commit", "pr": "PR", "artifact": "artifact",
               "command": "command", "link": "link", "other": "other"},
        "tally": {"asked": ("request", "requests"), "done": ("done", "done"),
                  "notdone": ("not finished", "not finished"), "open": ("open", "open")},
        "focus": "This page covers only: {focus}. The rest of the session is left out.",
        "compacted": "Part of this session was read from a compacted summary, so its items carry less detail.",
        "foot": "Built from the session record on {date}.",
        "interpreted": "Read as",
    },
    "th": {
        "eyebrow": "สรุป session", "open": "ยังค้างอยู่", "none_open": "ไม่มีงานค้าง",
        "done": "สิ่งที่ทำ", "decisions": "การตัดสินใจ", "checks": "การตรวจสอบ", "changes": "สิ่งที่เปลี่ยน",
        "asked": "สิ่งที่ขอ", "gaps": "สิ่งที่สรุปนี้ยืนยันไม่ได้",
        "status": {"done": "เสร็จ", "partial": "เสร็จบางส่วน", "failed": "ไม่สำเร็จ",
                   "skipped": "ข้าม", "running": "กำลังทำ"},
        "kind": {"todo": "ต้องทำต่อ", "question": "รอคุณตัดสินใจ", "risk": "ความเสี่ยง", "blocked": "ติดขัด"},
        "owner": {"user": "ของคุณ", "claude": "ของ Claude", "either": "ใครทำก็ได้"},
        "by": {"user": "คุณเลือก", "claude": "Claude เลือก", "default": "ค่า default"},
        "result": {"passed": "ผ่าน", "failed": "ไม่ผ่าน", "not run": "ไม่ได้รัน"},
        "verified_by": "ตรวจแล้วด้วย", "not_verified": "ยังไม่มี check ยืนยัน",
        "from_summary": "มาจากส่วนของ session ที่ถูกย่อแล้ว",
        "prs": "Pull requests", "artifacts": "Artifacts", "commits": "Commits", "files": "ไฟล์",
        "external": "สิ่งที่ส่งหรือเขียนออกไปข้างนอก",
        "change": {"added": "เพิ่ม", "modified": "แก้", "deleted": "ลบ", "renamed": "เปลี่ยนชื่อ"},
        "ev": {"file": "ไฟล์", "commit": "commit", "pr": "PR", "artifact": "artifact",
               "command": "คำสั่ง", "link": "ลิงก์", "other": "อื่น ๆ"},
        "tally": {"asked": ("คำขอ", "คำขอ"), "done": ("เสร็จ", "เสร็จ"),
                  "notdone": ("ยังไม่เสร็จ", "ยังไม่เสร็จ"), "open": ("ค้าง", "ค้าง")},
        "focus": "หน้านี้ครอบคลุมเฉพาะ: {focus} ส่วนอื่นของ session ไม่ได้รวมไว้",
        "compacted": "บางส่วนของ session นี้อ่านจากสรุปที่ถูกย่อแล้ว รายการจากส่วนนั้นจึงมีรายละเอียดน้อยกว่า",
        "foot": "สร้างจากบันทึกของ session เมื่อ {date}",
        "interpreted": "ตีความว่า",
    },
}
STATUS_CLASS = {"done": "ok", "partial": "warn", "failed": "bad", "skipped": "plain", "running": "accent"}
KIND_CLASS = {"todo": "accent", "question": "warn", "risk": "bad", "blocked": "bad"}
RESULT_CLASS = {"passed": "ok", "failed": "bad", "not run": "plain"}
CHANGE_CLASS = {"added": "add", "modified": "mod", "deleted": "del", "renamed": "mod"}
CHANGE_MARK = {"added": "+", "modified": "~", "deleted": "−", "renamed": "→"}


# ---------- checking ----------

def _s(value):
    return value if isinstance(value, str) else ""


def _strings(node, path=""):
    """Yield (path, text) for every string in the data."""
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for key, value in node.items():
            yield from _strings(value, f"{path}.{key}" if path else str(key))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _strings(value, f"{path}[{i}]")


def _is_http(url):
    return isinstance(url, str) and (url.startswith("https://") or url.startswith("http://"))


def check(data):
    """Return (errors, warnings) for one recap object."""
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ["the recap is not a JSON object"], warnings

    def need_list(key, required):
        value = data.get(key)
        if value is None and not required:
            return []
        if not isinstance(value, list):
            errors.append(f"{key}: must be a list")
            return []
        return value

    def choice(where, value, allowed):
        if value not in allowed:
            errors.append(f"{where}: {value!r} is not one of {', '.join(allowed)}")
            return False
        return True

    title = _s(data.get("title")).strip()
    words = title.split()
    if not 2 <= len(words) <= 4:
        errors.append(f"title: must be two to four words, got {len(words)}")
    if len(title) > TITLE_CAP:
        errors.append(f"title: {len(title)} characters (cap {TITLE_CAP})")
    if re.search(r"[:—–]| - ", title):
        errors.append("title: a name, not a caption; remove the colon or dash")

    if not DATE.fullmatch(_s(data.get("date"))):
        errors.append("date: must be YYYY-MM-DD")
    choice("lang", data.get("lang"), tuple(LABELS))

    outcome = _s(data.get("outcome")).strip()
    if not outcome:
        errors.append("outcome: required")
    elif len(outcome) > OUTCOME_CAP:
        errors.append(f"outcome: {len(outcome)} characters (cap {OUTCOME_CAP})")

    if "open" not in data:
        errors.append("open: the key is required; use [] only when nothing is open")
    open_items = need_list("open", False)
    for i, item in enumerate(open_items):
        where = f"open[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be an object")
            continue
        if not _s(item.get("what")).strip():
            errors.append(f"{where}.what: required")
        choice(f"{where}.kind", item.get("kind"), OPEN_KINDS)
        choice(f"{where}.owner", item.get("owner"), OWNERS)

    checks = need_list("checks", False)
    results = {}
    for i, item in enumerate(checks):
        where = f"checks[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be an object")
            continue
        cid = _s(item.get("id"))
        if not cid:
            errors.append(f"{where}.id: required")
        elif cid in results:
            errors.append(f"{where}.id: {cid!r} is used twice")
        if not _s(item.get("what")).strip():
            errors.append(f"{where}.what: required")
        if choice(f"{where}.result", item.get("result"), RESULTS) and cid:
            results[cid] = item["result"]

    done = need_list("done", True)
    if isinstance(data.get("done"), list) and not done:
        errors.append("done: at least one item (when nothing was done, there is no recap to write)")
    unfinished = 0
    for i, item in enumerate(done):
        where = f"done[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be an object")
            continue
        if not _s(item.get("what")).strip():
            errors.append(f"{where}.what: required")
        ok_type = choice(f"{where}.type", item.get("type"), TYPES)
        ok_status = choice(f"{where}.status", item.get("status"), STATUSES)
        ok_ver = choice(f"{where}.verified", item.get("verified"), VERIFIED)
        status, kind = item.get("status"), item.get("type")
        if ok_status and status != "done":
            unfinished += 1
        if ok_status and status in ("partial", "failed", "skipped") and not _s(item.get("detail")).strip():
            errors.append(f"{where}.detail: required when the status is {status}; say what is missing or why")
        if ok_ver and item["verified"] == "yes":
            cid = _s(item.get("check"))
            if not cid:
                errors.append(f"{where}.check: verified is yes, so name the check that passed")
            elif cid not in results:
                errors.append(f"{where}.check: no check has the id {cid!r}")
            elif results[cid] != "passed":
                errors.append(f"{where}.check: check {cid!r} is {results[cid]!r}, so the item is not verified")
        if ok_ver and ok_type and item["verified"] == "n/a" and kind != "answer":
            errors.append(f"{where}.verified: n/a is only for type answer; a change is yes or no")
        if ok_status and status in ("failed", "skipped") and item.get("verified") == "yes":
            errors.append(f"{where}.verified: a {status} item cannot be verified")
        evidence = item.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"{where}.evidence: must be a list")
            evidence = []
        if ok_type and ok_status and kind == "change" and status in ("done", "partial") and not evidence:
            errors.append(f"{where}.evidence: a change that is {status} needs at least one piece of evidence")
        for j, ev in enumerate(evidence):
            ew = f"{where}.evidence[{j}]"
            if not isinstance(ev, dict):
                errors.append(f"{ew}: must be an object")
                continue
            choice(f"{ew}.kind", ev.get("kind"), EVIDENCE_KINDS)
            if not _s(ev.get("ref")).strip():
                errors.append(f"{ew}.ref: required")
            if "url" in ev and ev["url"] not in ("", None) and not _is_http(ev["url"]):
                errors.append(f"{ew}.url: must start with http:// or https://")
        if "from" in item and item["from"] not in ("", "summary"):
            errors.append(f"{where}.from: only \"summary\" is allowed")

    for i, item in enumerate(need_list("decisions", False)):
        where = f"decisions[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be an object")
            continue
        if not _s(item.get("what")).strip():
            errors.append(f"{where}.what: required")
        choice(f"{where}.by", item.get("by"), BY)

    asked = need_list("asked", True)
    if isinstance(data.get("asked"), list) and not asked:
        errors.append("asked: at least one request")
    for i, item in enumerate(asked):
        if not isinstance(item, dict) or not _s(item.get("text")).strip():
            errors.append(f"asked[{i}].text: required")

    changes = data.get("changes", {})
    if not isinstance(changes, dict):
        errors.append("changes: must be an object")
        changes = {}
    for key in ("files", "commits", "prs", "artifacts", "external"):
        if key in changes and not isinstance(changes[key], list):
            errors.append(f"changes.{key}: must be a list")
            changes[key] = []
    files = changes.get("files", [])
    if len(files) > MAX_FILES:
        errors.append(f"changes.files: {len(files)} files (cap {MAX_FILES}); keep the ones that matter "
                      "and say how many are left out in notes.gaps")
    for i, item in enumerate(files):
        where = f"changes.files[{i}]"
        if not isinstance(item, dict) or not _s(item.get("path")).strip():
            errors.append(f"{where}.path: required")
            continue
        choice(f"{where}.change", item.get("change"), FILE_CHANGES)
    for i, item in enumerate(changes.get("commits", [])):
        where = f"changes.commits[{i}]"
        if not isinstance(item, dict) or not SHA.fullmatch(_s(item.get("sha"))):
            errors.append(f"{where}.sha: must be 7 to 40 hex characters")
    for i, item in enumerate(changes.get("prs", [])):
        where = f"changes.prs[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be an object")
            continue
        if not _is_http(item.get("url")):
            errors.append(f"{where}.url: must start with http:// or https://")
        choice(f"{where}.state", item.get("state"), PR_STATES)
    for i, item in enumerate(changes.get("artifacts", [])):
        if not isinstance(item, dict) or not _is_http(item.get("url")):
            errors.append(f"changes.artifacts[{i}].url: must start with http:// or https://")
    for i, item in enumerate(changes.get("external", [])):
        if not isinstance(item, dict) or not _s(item.get("what")).strip():
            errors.append(f"changes.external[{i}].what: required")

    notes = data.get("notes", {})
    if not isinstance(notes, dict):
        errors.append("notes: must be an object")
    elif "gaps" in notes and not isinstance(notes["gaps"], list):
        errors.append("notes.gaps: must be a list")

    for path, text in _strings(data):
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path}: looks like {name}; name where the secret lives, never its value")
        found = PRAISE.search(text)
        if found and not path.startswith("asked"):
            warnings.append(f"{path}: \"{found.group(0)}\" is praise, not a fact; the status already says what happened")
        if EMAIL.search(text):
            warnings.append(f"{path}: holds an email address; remove it unless the user asked for it on the page")

    if unfinished and isinstance(data.get("open"), list) and not open_items:
        warnings.append(f"open: empty, and {unfinished} done item(s) are not finished; "
                        "add an open entry for each or correct the status")
    return errors, warnings


# ---------- rendering ----------

def _t(text):
    """Escape text, then turn `code` spans into <code>."""
    return CODE.sub(lambda m: "<code>" + m.group(1) + "</code>", html.escape(_s(text), quote=True))


def _link(label_html, url):
    if _is_http(url):
        return f'<a href="{html.escape(url, quote=True)}" rel="noopener">{label_html}</a>'
    return label_html


def _tag(cls, label):
    return f'<span class="tag {cls}">{html.escape(label)}</span>'


def _section(key, title, inner):
    return (f'<section class="block" aria-labelledby="h-{key}">\n'
            f'<h2 id="h-{key}">{html.escape(title)}</h2>\n{inner}\n</section>')


def _plural(n, pair):
    return f"{n} {pair[0] if n == 1 else pair[1]}"


def render_body(data):
    lab = LABELS[data["lang"]]
    out = []

    done = data.get("done", [])
    open_items = data.get("open", [])
    asked = data.get("asked", [])
    n_done = sum(1 for d in done if d.get("status") == "done")
    n_not = len(done) - n_done
    tally = [_plural(len(asked), lab["tally"]["asked"]), _plural(n_done, lab["tally"]["done"])]
    if n_not:
        tally.append(_plural(n_not, lab["tally"]["notdone"]))
    tally.append(_plural(len(open_items), lab["tally"]["open"]))

    head = [f'<p class="eyebrow">{html.escape(lab["eyebrow"])} · <span class="num">{html.escape(data["date"])}</span></p>',
            f'<h1>{html.escape(data["title"].strip())}</h1>',
            f'<p class="outcome">{_t(data["outcome"].strip())}</p>',
            f'<p class="tally num">{html.escape(" · ".join(tally))}</p>']
    focus = _s(data.get("focus")).strip()
    if focus:
        head.append(f'<p class="focus">{_t(lab["focus"].format(focus=focus))}</p>')
    out.append('<header class="masthead">\n' + "\n".join(head) + "\n</header>")

    if open_items:
        rows = []
        for item in open_items:
            rows.append(
                '<li class="row">' + _tag(KIND_CLASS[item["kind"]], lab["kind"][item["kind"]]) +
                f'<div class="row-main"><p class="what">{_t(item["what"])}</p>'
                f'<p class="sub">{html.escape(lab["owner"][item["owner"]])}</p></div></li>')
        inner = '<div class="open-box"><ul class="rows">\n' + "\n".join(rows) + "\n</ul></div>"
    else:
        inner = f'<div class="open-box"><p class="none">{html.escape(lab["none_open"])}</p></div>'
    out.append(_section("open", lab["open"], inner))

    check_names = {c.get("id"): c.get("what") for c in data.get("checks", [])}
    rows = []
    for item in done:
        main = [f'<p class="what">{_t(item["what"])}</p>']
        if _s(item.get("detail")).strip():
            main.append(f'<p class="detail">{_t(item["detail"])}</p>')
        evidence = item.get("evidence", [])
        if evidence:
            chips = []
            for ev in evidence:
                mono = ' class="mono"' if ev["kind"] in ("file", "commit", "command") else ""
                label = f'<span class="k">{html.escape(lab["ev"][ev["kind"]])}</span><span{mono}>{html.escape(ev["ref"])}</span>'
                chips.append("<li>" + _link(label, ev.get("url")) + "</li>")
            main.append('<ul class="evidence">' + "".join(chips) + "</ul>")
        sub = []
        if item["verified"] == "yes":
            sub.append(html.escape(lab["verified_by"]) + " <code>"
                       + html.escape(_s(check_names.get(item.get("check")))) + "</code>")
        elif item["verified"] == "no":
            sub.append(html.escape(lab["not_verified"]))
        if item.get("from") == "summary":
            sub.append(html.escape(lab["from_summary"]))
        if sub:
            main.append('<p class="sub">' + " · ".join(sub) + "</p>")
        rows.append('<li class="row">' + _tag(STATUS_CLASS[item["status"]], lab["status"][item["status"]]) +
                    '<div class="row-main">' + "".join(main) + "</div></li>")
    out.append(_section("done", lab["done"], '<ul class="rows">\n' + "\n".join(rows) + "\n</ul>"))

    decisions = data.get("decisions", [])
    if decisions:
        rows = []
        for item in decisions:
            why = f'<p class="detail">{_t(item["why"])}</p>' if _s(item.get("why")).strip() else ""
            rows.append('<li class="row">' + _tag("plain" if item["by"] == "default" else "accent", lab["by"][item["by"]]) +
                        f'<div class="row-main"><p class="what">{_t(item["what"])}</p>{why}</div></li>')
        out.append(_section("decisions", lab["decisions"], '<ul class="rows">\n' + "\n".join(rows) + "\n</ul>"))

    checks = data.get("checks", [])
    if checks:
        rows = []
        for item in checks:
            detail = f'<p class="detail">{_t(item["detail"])}</p>' if _s(item.get("detail")).strip() else ""
            rows.append('<li class="row">' + _tag(RESULT_CLASS[item["result"]], lab["result"][item["result"]]) +
                        f'<div class="row-main"><p class="what"><code>{html.escape(item["what"])}</code></p>{detail}</div></li>')
        out.append(_section("checks", lab["checks"], '<ul class="rows">\n' + "\n".join(rows) + "\n</ul>"))

    changes = data.get("changes", {})
    subs = []

    def sub_block(title, items):
        subs.append(f'<div class="sub-block"><h3>{html.escape(title)}</h3>'
                    '<ul class="plain-list">' + "".join(items) + "</ul></div>")

    if changes.get("prs"):
        sub_block(lab["prs"], [
            f'<li><span class="lead">{html.escape(p["state"])}</span><span>'
            + _link(_t(_s(p.get("title")) or p["url"]), p["url"]) + "</span></li>" for p in changes["prs"]])
    if changes.get("artifacts"):
        sub_block(lab["artifacts"], [
            '<li><span class="lead"></span><span>' + _link(_t(_s(a.get("title")) or a["url"]), a["url"]) + "</span></li>"
            for a in changes["artifacts"]])
    if changes.get("commits"):
        sub_block(lab["commits"], [
            f'<li><span class="lead mono">{html.escape(c["sha"][:7])}</span><span>{_t(c.get("subject"))}</span></li>'
            for c in changes["commits"]])
    if changes.get("files"):
        sub_block(lab["files"], [
            f'<li><span class="lead {CHANGE_CLASS[f["change"]]}">{CHANGE_MARK[f["change"]]} '
            f'{html.escape(lab["change"][f["change"]])}</span><span class="mono">{html.escape(f["path"])}</span></li>'
            for f in changes["files"]])
    if changes.get("external"):
        sub_block(lab["external"], [
            f'<li><span class="lead">{_t(e.get("where"))}</span><span>{_t(e["what"])}</span></li>'
            for e in changes["external"]])
    if subs:
        out.append(_section("changes", lab["changes"], "\n".join(subs)))

    items = []
    for item in asked:
        note = (f'<p class="sub">{html.escape(lab["interpreted"])}: {_t(item["note"])}</p>'
                if _s(item.get("note")).strip() else "")
        items.append(f'<li><div class="row-main"><blockquote>{html.escape(item["text"])}</blockquote>{note}</div></li>')
    out.append(_section("asked", lab["asked"], '<ol class="asked">\n' + "\n".join(items) + "\n</ol>"))

    notes = data.get("notes", {})
    gaps = [g for g in notes.get("gaps", []) if _s(g).strip()]
    if notes.get("compacted") is True:
        gaps = [lab["compacted"]] + gaps
    if gaps:
        out.append(_section("gaps", lab["gaps"],
                            '<ul class="gaps">' + "".join(f"<li>{_t(g)}</li>" for g in gaps) + "</ul>"))

    out.append(f'<p class="foot num">{html.escape(lab["foot"].format(date=data["date"]))}</p>')
    return "\n\n".join(out)


def render(data, template):
    """Render checked data into the template. Call check() first."""
    page = template.replace("{{TITLE}}", html.escape(data["title"].strip()))
    page = page.replace("{{LANG}}", html.escape(data["lang"], quote=True))
    return page.replace("{{BODY}}", render_body(data))


# ---------- CLI ----------

def main(argv=None):
    parser = argparse.ArgumentParser(description="Check a session recap and render it as one HTML page.")
    parser.add_argument("recap", help="path to recap.json")
    parser.add_argument("-o", "--out", help="path of the HTML file to write")
    parser.add_argument("--check", action="store_true", help="check only; write nothing")
    parser.add_argument("--template", default=TEMPLATE, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if not args.check and not args.out:
        parser.error("give -o <file.html>, or --check")

    try:
        with open(args.recap, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [f"cannot read {args.recap}: {exc}"], "warnings": [], "out": None},
                         ensure_ascii=False, indent=1))
        return 2

    errors, warnings = check(data)
    out = None
    if not errors and not args.check:
        try:
            with open(args.template, encoding="utf-8") as fh:
                template = fh.read()
        except OSError as exc:
            print(json.dumps({"ok": False, "errors": [f"cannot read the template: {exc}"], "warnings": warnings,
                              "out": None}, ensure_ascii=False, indent=1))
            return 2
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render(data, template))
        out = args.out
    print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings, "out": out},
                     ensure_ascii=False, indent=1))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
