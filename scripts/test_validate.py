"""Tests for scripts/validate.py (S10-W0-1).

Run: python3 -m unittest discover -s scripts -p 'test_validate.py' -q
Every fixture is built in a temporary directory; nothing touches the repo tree.
"""
import io
import json
import os
import tempfile
import unittest

import validate

DESC = "Does a thing for tests. " * 12  # ~290 chars, above the WARN threshold


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return path


def skill_md(name, desc=DESC, newline="\n"):
    return newline.join(["---", f"name: {name}", f"description: {desc}", "---", "", "# Body", ""])


def make_repo(root, plugins=None, entry_extra=None):
    """A minimal valid marketplace with one plugin `alpha` holding one skill `alpha`."""
    plugins = plugins if plugins is not None else ["alpha"]
    entries = []
    for name in plugins:
        entry = {"name": name, "source": f"./plugins/{name}"}
        entry.update(entry_extra or {})
        entries.append(entry)
        write(root, f"plugins/{name}/.claude-plugin/plugin.json",
              json.dumps({"name": name, "version": "1.0.0"}))
        write(root, f"plugins/{name}/skills/{name}/SKILL.md", skill_md(name))
    write(root, ".claude-plugin/marketplace.json",
          json.dumps({"name": "test-mkt", "owner": {"name": "Owner"}, "plugins": entries}))


def run(root):
    out = io.StringIO()
    code = validate.main(root, out)
    return code, out.getvalue()


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def test_clean_repo_passes(self):
        make_repo(self.root)
        code, out = run(self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("all checks passed", out)
        self.assertNotIn("FAIL", out)

    def test_missing_marketplace_is_counted_fail_not_crash(self):
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  .claude-plugin/marketplace.json at repo root exists", out)

    def test_malformed_marketplace_is_counted_fail(self):
        write(self.root, ".claude-plugin/marketplace.json", "{not json")
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("is valid JSON", out)

    def test_missing_plugin_json_is_counted_fail_and_continues(self):
        make_repo(self.root, plugins=["alpha", "beta"])
        os.remove(os.path.join(self.root, "plugins/alpha/.claude-plugin/plugin.json"))
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  .claude-plugin/plugin.json exists", out)
        self.assertIn("plugin: beta", out)  # the run went on to the next plugin

    def test_malformed_plugin_json_is_counted_fail(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/.claude-plugin/plugin.json", "[1, 2")
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn(".claude-plugin/plugin.json is valid JSON", out)

    def test_missing_declared_mcp_file_is_counted_fail(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/.claude-plugin/plugin.json",
              json.dumps({"name": "alpha", "version": "1.0.0", "mcpServers": "./.mcp.json"}))
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  declared mcpServers file ./.mcp.json exists", out)

    def test_stdio_and_http_mcp_servers_pass(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/.claude-plugin/plugin.json",
              json.dumps({"name": "alpha", "version": "1.0.0", "mcpServers": "./.mcp.json"}))
        write(self.root, "plugins/alpha/.mcp.json", json.dumps({"mcpServers": {
            "local": {"command": "node", "args": ["server.js"]},
            "remote": {"type": "http", "url": "https://example.invalid/mcp"},
        }}))
        code, out = run(self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("PASS  ./.mcp.json: server local is http/sse", out)

    def test_mcp_server_without_command_or_url_fails(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/.claude-plugin/plugin.json",
              json.dumps({"name": "alpha", "version": "1.0.0", "mcpServers": "./.mcp.json"}))
        write(self.root, "plugins/alpha/.mcp.json", json.dumps({"mcpServers": {"bad": {"type": "http"}}}))
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  ./.mcp.json: server bad", out)

    def test_crlf_frontmatter_parses(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/skills/alpha/SKILL.md", skill_md("alpha", newline="\r\n"))
        code, out = run(self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("frontmatter parses", out)
        self.assertIn("frontmatter name matches directory", out)

    def test_short_description_warns_not_fails(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/skills/alpha/SKILL.md", skill_md("alpha", desc="Too short."))
        code, out = run(self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("WARN  skills/alpha: description 10 chars is short", out)
        self.assertNotIn("min 200", out)

    def test_no_length_floor_line_on_normal_description(self):
        make_repo(self.root)
        code, out = run(self.root)
        self.assertEqual(code, 0)
        self.assertNotIn("WARN", out)
        self.assertNotIn("min 200", out)

    def test_description_over_cap_fails(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/skills/alpha/SKILL.md", skill_md("alpha", desc="x" * 1025))
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  skills/alpha: description 1025 chars (hard cap 1024)", out)

    def test_invalid_yaml_fails_when_not_ratcheted(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/skills/alpha/SKILL.md",
              skill_md("alpha", desc="Colon: inside an unquoted value: breaks strict YAML."))
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertEqual(out.count("FAIL"), 1)
        self.assertIn("FAIL  plugins/alpha/skills/alpha/SKILL.md: yaml-error:", out)

    def test_invalid_yaml_warns_when_ratcheted(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/skills/alpha/SKILL.md",
              skill_md("alpha", desc="Colon: inside an unquoted value: breaks strict YAML."))
        write(self.root, "docs/rewrite/ratchet.json", json.dumps({"schema": 1, "entries": [
            {"check_id": "yaml-parse", "path": "plugins/alpha/skills/alpha/SKILL.md", "message": "x"}]}))
        code, out = run(self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("WARN  plugins/alpha/skills/alpha/SKILL.md: yaml-error:", out)
        self.assertIn("all checks passed", out)

    def test_ratchet_entry_for_other_check_does_not_mask_yaml(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/skills/alpha/SKILL.md",
              skill_md("alpha", desc="Colon: inside an unquoted value: breaks strict YAML."))
        write(self.root, "docs/rewrite/ratchet.json", json.dumps({"entries": [
            {"check_id": "R70", "path": "plugins/alpha/skills/alpha/SKILL.md", "message": "x"}]}))
        code, _ = run(self.root)
        self.assertEqual(code, 1)

    def test_malformed_ratchet_is_counted_fail(self):
        make_repo(self.root)
        write(self.root, "docs/rewrite/ratchet.json", "{")
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("docs/rewrite/ratchet.json is readable", out)

    def test_version_parity_is_not_checked(self):
        make_repo(self.root, entry_extra={"version": "9.9.9"})
        code, out = run(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("marketplace entry version", out)

    def test_malformed_legacy_evals_json_is_counted_fail(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/skills/alpha/evals/evals.json", "{")
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("skills/alpha/evals/evals.json is valid JSON", out)

    def test_command_without_description_fails(self):
        make_repo(self.root)
        write(self.root, "plugins/alpha/commands/go.md", "---\nargument-hint: x\n---\nbody\n")
        code, out = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  commands/go.md: frontmatter description present", out)


if __name__ == "__main__":
    unittest.main()
