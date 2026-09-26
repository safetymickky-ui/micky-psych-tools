#!/usr/bin/env python3
"""Unit tests for bullet-reconstruct's scripts (stdlib unittest).

    python3 -m unittest discover -s plugins/bullet-reconstruct/tests

The snip test builds a one-page PDF in raw PDF syntax (a bold "Table 1." caption over a
vector table, plus an in-text "Table 2" mention with no graphic), so no binary fixture
is committed. Tests that need a missing package are skipped, not failed.
"""
import base64
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "skills", "bullet-reconstruct", "scripts")
HAS_MD = importlib.util.find_spec("markdown") is not None
HAS_PDF = all(importlib.util.find_spec(m) is not None for m in ("pdfplumber", "PIL"))
PNG_1PX = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")


def run(script, *args, cwd):
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                          cwd=cwd, capture_output=True, text=True)


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class CoverageCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        write(os.path.join(self.tmp, "source.txt"),
              "A meta-analysis of 245 studies found 39.7% prevalence. Effects held for seven decades.")

    def units(self, units):
        write(os.path.join(self.tmp, "units.json"), json.dumps({"source": "t", "units": units}))

    def test_pass_when_anchors_and_numbers_are_found(self):
        self.units([{"id": 1, "unit": "prevalence", "anchors": ["39.7", "245"], "status": "present"}])
        write(os.path.join(self.tmp, "notes.md"), "- **Prevalence** 39.7% across 245 studies over ~7 decades")
        r = run("coverage_check.py", "units.json", "--output", "notes.md", "--source", "source.txt", cwd=self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("all found in source", r.stdout)  # "7" matches the word "seven"

    def test_missing_anchor_downgrades_a_self_graded_unit(self):
        self.units([{"id": 1, "unit": "prevalence", "anchors": ["39.7"], "status": "present"}])
        write(os.path.join(self.tmp, "notes.md"), "- **Prevalence** was high")
        r = run("coverage_check.py", "units.json", "--output", "notes.md", cwd=self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("present -> missing", r.stdout)

    def test_anchor_spanning_markdown_emphasis_still_matches(self):
        self.units([{"id": 1, "unit": "design", "anchors": ["not a systematic review", "STAR*D"],
                     "status": "present"}])
        write(os.path.join(self.tmp, "notes.md"), "- explicitly **not** a systematic review; `STAR\\*D`")
        r = run("coverage_check.py", "units.json", "--output", "notes.md", cwd=self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_number_not_in_source_fails(self):
        self.units([{"id": 1, "unit": "prevalence", "anchors": ["39.7"], "status": "present"}])
        write(os.path.join(self.tmp, "notes.md"), "- 39.7% prevalence, 41.2% in women")
        r = run("coverage_check.py", "units.json", "--output", "notes.md", "--source", "source.txt", cwd=self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("41.2", r.stdout)

    def test_distorted_counts_as_full_loss(self):
        self.units([{"id": i, "unit": f"u{i}", "status": "present"} for i in range(9)]
                   + [{"id": 9, "unit": "u9", "status": "distorted"}])
        r = run("coverage_check.py", "units.json", cwd=self.tmp)
        self.assertEqual(r.returncode, 1)  # 1/10 = 10%, not under the 10% ceiling
        self.assertIn("DISTORTED", r.stdout)

    def test_bad_status_is_a_usage_error(self):
        self.units([{"id": 1, "unit": "x", "status": "kept"}])
        self.assertEqual(run("coverage_check.py", "units.json", cwd=self.tmp).returncode, 2)


@unittest.skipUnless(HAS_MD, "python-markdown not installed")
class BuildHtml(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, "snips"))
        with open(os.path.join(self.tmp, "snips", "t1.png"), "wb") as fh:
            fh.write(PNG_1PX)

    def test_embeds_images_as_figures(self):
        write(os.path.join(self.tmp, "notes.md"),
              "# Title here\n\n*Author. Journal 2026*\n\n## Section\n\n- **Key** claim\n\n"
              '![Table 1: what it shows](snips/t1.png "Table 1 · p. 2 · Author 2026")\n\n- after\n')
        r = run("build_html.py", "notes.md", "--out", "notes.html", cwd=self.tmp)
        self.assertEqual(r.returncode, 0, r.stderr)
        page = read(os.path.join(self.tmp, "notes.html"))
        self.assertIn("<h1>Title here</h1>", page)
        self.assertIn('class="src">Author. Journal 2026', page)
        self.assertIn("data:image/png;base64,", page)
        self.assertIn("<figure>", page)
        self.assertIn("<figcaption>Table 1 · p. 2 · Author 2026</figcaption>", page)
        self.assertNotIn("loading=", page)
        self.assertNotIn("snips/t1.png", page)

    def test_missing_image_fails(self):
        write(os.path.join(self.tmp, "notes.md"), "# T\n\n![x](snips/nope.png)\n")
        r = run("build_html.py", "notes.md", cwd=self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("image not found", r.stderr)


def tiny_pdf(path):
    """One page: bold 'Table 1.' caption over a ruled, shaded table; a lone 'Table 2' line."""
    content = b"\n".join([
        b"BT /F2 10 Tf 72 700 Td (Table 1.) Tj ET",
        b"BT /F1 10 Tf 115 700 Td (Test caption for the snip) Tj ET",
        b"0.85 g 72 612 228 76 re f 0 g",
        b"1 w 72 690 m 300 690 l S 72 650 m 300 650 l S 72 610 m 300 610 l S",
        b"BT /F1 9 Tf 80 670 Td (Row one) Tj ET",
        b"BT /F1 9 Tf 80 630 Td (Row two) Tj ET",
        b"BT /F1 10 Tf 72 400 Td (Table 2 shows nothing here) Tj ET",
    ])
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
        b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
    ]
    out, offsets = bytearray(b"%PDF-1.4\n"), []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    with open(path, "wb") as fh:
        fh.write(bytes(out))


@unittest.skipUnless(HAS_PDF, "pdfplumber / Pillow not installed")
class SnipFigures(unittest.TestCase):
    def test_vector_table_is_snipped_and_text_mention_skipped(self):
        tmp = tempfile.mkdtemp()
        tiny_pdf(os.path.join(tmp, "t.pdf"))
        r = run("snip_figures.py", "t.pdf", "--out", "snips", "--dpi", "100", cwd=tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        man = json.loads(read(os.path.join(tmp, "snips", "manifest.json")))
        self.assertEqual([s["file"] for s in man["snips"]], ["table-1.png"])
        self.assertTrue(man["snips"][0]["caption"].startswith("Table 1. Test caption"))
        self.assertEqual([s["label"] for s in man["skipped"]], ["Table 2"])
        from PIL import Image
        with Image.open(os.path.join(tmp, "snips", "table-1.png")) as im:
            h = im.size[1]
        self.assertGreater(h, 90)  # caption + table body, not the caption alone


if __name__ == "__main__":
    unittest.main()
