#!/usr/bin/env python3
"""Shared measurement helper for the phase-3 rewrite specs. Read-only.

Usage:
  python3 measure.py skill <path/to/SKILL.md> [...]   frontmatter + description + body metrics
  python3 measure.py text  "<description text>"       metrics for a proposed description
  python3 measure.py textfile <file>                  same, text read from a file (no frontmatter)
  python3 measure.py file  <path> [...]               lines / bytes / est. tokens of any file

Token estimate = chars / 4 (the architecture's convention, section 9).
Quoted phrases = text inside "..." or curly double quotes; these feed the trigger lock.
"""
import json
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

QUOTE_RE = re.compile(r'"([^"\n]{1,120})"|“([^”\n]{1,120})”')


def quoted(text):
    out = []
    for m in QUOTE_RE.finditer(text or ""):
        out.append(m.group(1) if m.group(1) is not None else m.group(2))
    return out


def desc_metrics(desc):
    desc = desc or ""
    low = desc.lower()
    use = low.find("use when")
    notfor = max(low.find("not for"), low.find("not:"))
    return {
        "chars": len(desc),
        "utf8_bytes": len(desc.encode("utf-8")),
        "est_tokens": round(len(desc) / 4),
        "use_when_at": use,
        "not_for_at": notfor,
        "has_first_or_second_person": bool(re.search(r"\b(I|you|your|we|my)\b", re.sub(QUOTE_RE, "", desc))),
        "has_angle_brackets": ("<" in desc or ">" in desc),
        "quoted_phrases": quoted(desc),
    }


def split_frontmatter(raw):
    raw = raw.replace("\r\n", "\n")
    if not raw.startswith("---\n"):
        return None, raw
    end = raw.find("\n---", 4)
    if end < 0:
        return None, raw
    return raw[4:end], raw[end + 4 :].lstrip("\n")


def skill(path):
    raw = open(path, encoding="utf-8").read()
    fm_text, body = split_frontmatter(raw)
    res = {"path": path, "frontmatter_present": fm_text is not None}
    fm = None
    if fm_text is not None and yaml is not None:
        try:
            fm = yaml.safe_load(fm_text)
            res["yaml_valid"] = True
        except Exception as e:  # noqa: BLE001
            res["yaml_valid"] = False
            res["yaml_error"] = str(e).splitlines()[0][:200]
    if isinstance(fm, dict):
        res["frontmatter_keys"] = sorted(fm.keys())
        d = fm.get("description") or ""
        w = fm.get("when_to_use") or ""
        res["description"] = desc_metrics(d)
        res["when_to_use_chars"] = len(w)
        res["description_plus_when_to_use_chars"] = len(d) + len(w)
        res["disable_model_invocation"] = fm.get("disable-model-invocation", False)
    elif fm_text is not None:
        # fallback: crude description grab when YAML is invalid
        m = re.search(r"^description:\s*(.*)$", fm_text, re.M)
        if m:
            res["description_raw_line"] = desc_metrics(m.group(1).strip().strip('"'))
    res["body_lines"] = body.count("\n") + 1
    res["body_chars"] = len(body)
    res["body_est_tokens"] = round(len(body) / 4)
    res["linked_files"] = sorted(set(re.findall(r"(?:references|scripts|assets|examples|templates)/[\w./-]+", body)))
    res["plugin_root_paths"] = sorted(set(re.findall(r"\$\{CLAUDE_[A-Z_]+\}[^\s`'\")]*", body)))
    return res


def text(desc):
    return {"description": desc_metrics(desc)}


def filem(path):
    data = open(path, "rb").read()
    txt = data.decode("utf-8", errors="replace")
    return {"path": path, "lines": txt.count("\n") + (0 if txt.endswith("\n") else 1), "bytes": len(data), "est_tokens": round(len(txt) / 4)}


def main(argv):
    if len(argv) < 3 or argv[1] not in {"skill", "text", "textfile", "file"}:
        print(__doc__)
        return 2
    mode, args = argv[1], argv[2:]
    if mode == "skill":
        out = [skill(p) for p in args]
    elif mode == "text":
        out = [text(" ".join(args))]
    elif mode == "textfile":
        out = [text(open(args[0], encoding="utf-8").read().strip())]
    else:
        out = [filem(p) for p in args]
    print(json.dumps(out if len(out) > 1 else out[0], ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
