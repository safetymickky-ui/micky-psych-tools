#!/usr/bin/env python3
"""build_html.py — render a bullet-reconstruct .md into ONE self-contained .html file.

- Markdown -> HTML with python-markdown (4-space nested bullets).
- Header: the first `# ` line is the title; an italic line right after it (`*...*`)
  becomes the source line. --title / --source-html override them.
- Images: every local image is embedded as base64, so the single file works offline,
  on a phone, and in print. An image alone on its line becomes a <figure>; its markdown
  title becomes the caption:
      ![Table 1: postulated mechanisms](snips/table-1.png "Table 1 · p. 2 · Author 2026")
- Never adds loading="lazy": a lazy data-URI image stays blank in print, in previews and
  in full-page captures.
- Light/dark (prefers-color-scheme), print CSS, Thai-capable font stack.

Usage:
  python3 build_html.py notes.md [--out notes.html] [--title T] [--source-html H]
                        [--footer-html H] [--allow-remote]

Exit 0 when written; 1 when an image is missing or remote (unless --allow-remote);
2 on a usage error. Needs python-markdown (python3 -m pip install markdown).
"""
import argparse
import base64
import html
import os
import re
import sys

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("missing dependency: markdown (python3 -m pip install markdown)")

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
        ".webp": "image/webp", ".svg": "image/svg+xml"}

CSS = r"""
:root{--bg:#fbfaf7;--fg:#1d1f23;--muted:#5b616b;--rule:#e2dfd6;--accent:#1d5d8a;
--card:#ffffff;--card-rule:#dcd8cf;--li2:#394049}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#15171b;--fg:#e8e6e0;
--muted:#a4a8af;--rule:#2d3137;--accent:#86b9e0;--card:#f3f1eb;--card-rule:#3b4048;--li2:#c8cbd0}}
:root[data-theme="dark"]{--bg:#15171b;--fg:#e8e6e0;--muted:#a4a8af;--rule:#2d3137;--accent:#86b9e0;
--card:#f3f1eb;--card-rule:#3b4048;--li2:#c8cbd0}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);
font:17px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans",
"Noto Sans Thai","Sarabun","Leelawadee UI",Tahoma,sans-serif}
main{max-width:46rem;margin:0 auto;padding:28px 16px 56px}
header{padding-bottom:14px;margin-bottom:4px;border-bottom:1px solid var(--rule)}
h1{font-size:1.5rem;line-height:1.28;margin:0 0 8px;letter-spacing:-.01em}
.src{color:var(--muted);font-size:.9rem;margin:0}
.src a,main a{color:var(--accent)}
h2{font-size:1.18rem;line-height:1.3;margin:32px 0 8px;padding-top:14px;border-top:1px solid var(--rule)}
header+h2{border-top:0;padding-top:4px}
h3{font-size:1.01rem;line-height:1.35;margin:22px 0 6px;color:var(--accent)}
ul,ol{margin:6px 0 10px;padding-left:1.2rem}
li{margin:5px 0}
li>ul,li>ol{margin:3px 0 6px;padding-left:1.1rem}
li li{color:var(--li2);font-size:.96em}
li::marker{color:var(--muted)}
strong{font-weight:650}
table{border-collapse:collapse;margin:10px 0 16px;font-size:.92em;display:block;overflow-x:auto}
th,td{border:1px solid var(--rule);padding:5px 8px;text-align:left;vertical-align:top}
figure{margin:14px 0 22px;background:var(--card);border:1px solid var(--card-rule);
border-radius:10px;padding:12px 12px 10px}
figure img{display:block;width:100%;height:auto}
img{max-width:100%;height:auto}
figcaption{font-size:.8rem;line-height:1.45;color:#565c66;margin-top:8px}
footer{margin-top:36px;padding-top:12px;border-top:1px solid var(--rule);color:var(--muted);font-size:.8rem}
@media print{body{background:#fff;color:#000;font-size:10.5pt}main{max-width:none;padding:0}
figure{break-inside:avoid;border-color:#bbb}h2,h3{break-after:avoid}a{color:inherit}}
"""


def split_header(text):
    """(title, source_md, body) — pull the H1 and an italic source line off the top."""
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    title = source = None
    if i < len(lines) and lines[i].startswith("# "):
        title = lines[i][2:].strip()
        i += 1
        j = i
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and re.fullmatch(r"(\*[^*].*\*|_[^_].*_)", lines[j].strip()):
            source = lines[j].strip()
            i = j + 1
    return title, source, "\n".join(lines[i:])


def inline(md_text):
    out = markdown.markdown(md_text, output_format="html")
    return re.sub(r"^<p>|</p>$", "", out.strip())


def embed_images(body, base_dir, allow_remote):
    errors, count = [], [0]

    def repl(m):
        tag = m.group(0)
        src = re.search(r'\ssrc="([^"]*)"', tag)
        if not src:
            return tag
        url = html.unescape(src.group(1))
        if url.startswith("data:"):
            return tag
        if re.match(r"^[a-z]+://", url, re.I):
            if not allow_remote:
                errors.append(f"remote image (breaks offline use): {url}")
            return tag
        path = os.path.normpath(os.path.join(base_dir, url))
        ext = os.path.splitext(path)[1].lower()
        if not os.path.isfile(path):
            errors.append(f"image not found: {url}")
            return tag
        if ext not in MIME:
            errors.append(f"unsupported image type: {url}")
            return tag
        with open(path, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode("ascii")
        count[0] += 1
        tag = re.sub(r'\sloading="[^"]*"', "", tag)
        return tag.replace(src.group(0), f' src="data:{MIME[ext]};base64,{b64}"')

    body = re.sub(r"<img\b[^>]*>", repl, body)
    return body, errors, count[0]


def to_figures(body):
    """<p><img …></p> alone in a paragraph -> <figure> with the title (or alt) as caption."""
    n = [0]

    def repl(m):
        img = m.group(1)
        t = re.search(r'\stitle="([^"]*)"', img) or re.search(r'\salt="([^"]*)"', img)
        cap = t.group(1) if t else ""
        img = re.sub(r'\stitle="[^"]*"', "", img)
        n[0] += 1
        caption = f"<figcaption>{cap}</figcaption>" if cap else ""
        return f"<figure>{img}{caption}</figure>"

    body = re.sub(r"<p>\s*(<img\b[^>]*>)\s*</p>", repl, body)
    return body, n[0]


def build(md_path, out_path=None, title=None, source_html=None, footer_html=None, allow_remote=False):
    with open(md_path, encoding="utf-8") as fh:
        text = fh.read()
    t, s, body_md = split_header(text)
    title = title or t or os.path.splitext(os.path.basename(md_path))[0]
    if source_html is None:
        source_html = inline(s.strip("*_")) if s else ""
    body = markdown.markdown(body_md, extensions=["sane_lists", "tables"], output_format="html")
    body, figs = to_figures(body)
    body, errors, n_img = embed_images(body, os.path.dirname(os.path.abspath(md_path)), allow_remote)
    if footer_html is None:
        footer_html = ("Bullet reconstruction. Figure and table images are cropped from the source file.")
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<main>
<header>
<h1>{html.escape(title)}</h1>
{f'<p class="src">{source_html}</p>' if source_html else ''}
</header>
{body}
<footer>{footer_html}</footer>
</main>
</body>
</html>
"""
    out_path = out_path or os.path.splitext(md_path)[0] + ".html"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return out_path, len(page.encode("utf-8")), n_img, figs, errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md")
    ap.add_argument("--out")
    ap.add_argument("--title")
    ap.add_argument("--source-html")
    ap.add_argument("--footer-html")
    ap.add_argument("--allow-remote", action="store_true")
    a = ap.parse_args()
    if not os.path.isfile(a.md):
        print(f"not a file: {a.md}", file=sys.stderr)
        sys.exit(2)
    out, size, n_img, figs, errors = build(a.md, a.out, a.title, a.source_html, a.footer_html, a.allow_remote)
    print(f"wrote {out} ({size / 1024:.0f} KB): {n_img} image(s) embedded, {figs} figure(s)")
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
