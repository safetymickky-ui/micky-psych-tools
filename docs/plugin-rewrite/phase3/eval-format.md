# claude plugin eval — case and grader format (primer)

Verbatim extract of https://code.claude.com/docs/en/plugin-evals (fetched 2026-09-24; CLI 2.1.281). Sections: write a case manually, fixtures and mocks, grant tools, eval suite reference. Use ONLY these keys; an unknown prompt.md key is an error.

### Write a case manually

Having Claude write the cases with `claude plugin eval init` is the recommended path. To write one yourself instead, start from a blank template. The following command writes a case named `first-case` with a placeholder `prompt.md` and one placeholder grader, and runs nothing:

```bash theme={null}
claude plugin eval init --bare first-case
```

```text theme={null}
evals/first-case/
├── prompt.md            # the prompt sent to Claude, plus run limits
└── graders/
    └── criteria.md      # one grader: how to score the result
```

In `prompt.md` you write the message Claude receives in each run, and set the run's limits and the tools the case may use in its frontmatter. Open `evals/first-case/prompt.md` and replace the placeholder body with a request one of your skills should handle, phrased the way a user would type it rather than naming the skill. This example is for a skill that drafts commit messages; use your own request:

```markdown theme={null}
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Write me a commit message for this change: I renamed getUser to fetchUser and updated the three call sites.
```

Each run starts in an empty working directory, so put whatever the task needs in the prompt itself, or [set up the workspace](#add-setup-or-history-with-case-yaml) first. The [full list of frontmatter fields](#prompt-md-fields) covers the model, timeout, tags, and environment variables.

Each file under `graders/` is one check applied after the run. Open `evals/first-case/graders/criteria.md` and replace the placeholder with a rubric for the judge model, written as concrete PASS and FAIL conditions:

```markdown theme={null}
---
type: llm
---

PASS if <what a correct response contains>.
FAIL if <what a wrong or missing response looks like>.
```

Then add a second grader that checks whether your skill is what produced the answer. Create `evals/first-case/graders/skill-fired.md`, replacing `your-skill-name` with the `name` from your skill's `SKILL.md`:

```markdown theme={null}
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?your-skill-name"'
---
```

This passes when Claude invoked that skill at least once during the run, including by its namespaced `plugin-name:skill-name` form. [Grader types](#grader-types) lists the other checks available, such as matching a regex or confirming a file was created.

With both files saved, run the case the way the [quickstart](#create-your-first-eval-suite) does, with `claude plugin eval .` from the plugin root.

<h3 id="set-run-limits-and-tools-in-prompt-md">
  Set run limits and tools in prompt.md
</h3>

Set a case's `max_turns`, `timeout_seconds`, `model`, `tags`, and the `allowed_tools` it may use in `prompt.md` frontmatter; the [prompt.md frontmatter](#prompt-md-fields) reference lists every field and its default. Claude receives the body exactly as you wrote it. `@path` mentions in it aren't expanded into file attachments, so if Claude needs to read a file, grant a tool for it in `allowed_tools`.

<h3 id="grade-the-result">
  Choose and weight graders
</h3>

A grader's frontmatter sets its `type`, and optionally a `weight` that makes it count for more of the run's score and an [`arm`](#compare-against-a-no-plugin-baseline) that controls how it's scored against the baseline. Of the six types, `regex`, `tool_used`, `tool_order`, and `file_exists` are computed from the transcript and files and cost nothing, while `llm` and `baseline` call a judge model and add to the run's cost.

There are no custom-code graders. [Grader types](#grader-types) lists each type's options and pass condition, and [what a grader can look at](#what-a-grader-can-look-at) lists the values `target` and `focus` accept.

The judge for `llm` and `baseline` graders is a small fast model by default. Pass `--judge-model sonnet` or a full model ID to use a stronger one for nuanced rubrics.

#### Choose graders that give a stable signal

An `llm` grader asks a model for a verdict, so its answer can differ between runs, and it differs more the longer the text it has to read. These habits keep a suite's scores steady enough to trust:

* For long output such as a generated file, grade it with a `regex` grader over the file's contents, which checks the whole file the same way every time. Keep `llm` graders for short outputs, with rubrics written as concrete PASS and FAIL conditions.
* Give each case one grader on the result, such as the final message or a produced file, and one on how Claude got there, such as `tool_used` or `tool_order`. Together they tell you both whether the answer was right and whether your plugin produced it.
* If a case's `tool_used: Skill` grader passes but `Δ` is negative, suspect the judge before the plugin. A small judge model can mark a correct answer wrong because it's formatted differently from what the rubric describes. Re-run with `--judge-model sonnet`, and tighten the rubric so formatting doesn't decide the verdict.
* To check that a build or test passed inside the run, have the prompt ask Claude to run it and write the outcome to a file, grade that file, and assert the command ran with a `tool_used` grader whose `input_match` names the command.

<h3 id="compare-against-a-no-plugin-baseline">
  Score against the no-plugin baseline
</h3>

When a plugin is under test, each case runs in two arms by default. The with-arm is its runs with the plugin loaded, and the without-arm is the same number of runs with no plugin at all. The summary and report show both scores and `Δ`, the with-arm score minus the without-arm score. Pass `--ablation none` to run only the with-arm, which halves the cost when you don't need the comparison, such as while iterating on graders.

In a two-arm run, some graders are reported with `scored: false`. A check like "the skill was invoked" can never pass without the plugin, so counting it would push the without-arm toward zero and inflate `Δ`. To keep the two arms comparable, Claude Code excludes such graders from the score in both arms and reports them in the with-arm as pass/fail indicators only. That includes:

* Every `tool_used` grader whose `tool` is `Skill`
* Any grader you mark `arm: with-only`

If every grader in a case is one of these, they're scored normally instead, since there would be nothing left to score. Set `arm: both` on a grader to score it in both arms regardless, which is what you want for a "must not invoke the skill" check with `min: 0` and `max: 0`. Under `--ablation none` nothing is excluded, so the same suite can produce a different absolute score in the two modes.

### Use a different eval directory

If `evals/` is already taken by another tool, keep the suite in a different directory. You can record that directory in the plugin's `plugin.json` so every run and every collaborator uses it, or pass it on the command line for a single run:

* **In `plugin.json`**: add `"experimental": { "evals": "quality/evals" }`.
* **On the command line**: pass `--eval-dir quality/evals` to both `claude plugin eval` and `claude plugin eval init`.

If you set both, the flag's directory is used. Give a relative path of plain directory names such as `qa` or `quality/evals`. An absolute path or one containing `..` isn't accepted: as a flag value it's an error, while an unusable manifest value prints a `Warning:` line and the run uses `evals/` instead. Cases, results, and `init` output all move to that directory.

## Set up fixtures and mocks

A case can need more than a prompt: files or a git repository in the workspace, an earlier conversation to continue, or answers from the MCP servers your plugin talks to. Each of those is set up beside the case so runs stay repeatable.

<h3 id="add-setup-or-history-with-case-yaml">
  Seed the workspace or conversation
</h3>

Each run starts in an empty workspace. When a case needs more than the prompt, add a `case.yaml` beside `prompt.md` with a `context` block.

To create fixture files or a git repository first, write a Bash script in the case directory and name it in `context.scaffold_script`. The script runs as you, outside the agent's sandbox, and only when you pass `--scaffold`, so pass that flag only for suites you or your organization wrote. To continue an earlier conversation, save the transcript as a `.jsonl` file and name it in `context.history_file`, and the case's prompt becomes the next user turn. To let Claude read fixture directories in the case during the run, list them in `context.add_dirs`.

A `case.yaml` also needs `schema_version: "1.1"` and `name`; the [case.yaml fields](#case-yaml-fields) reference has the full list.

This `case.yaml` seeds a workspace from a script and lets Claude read fixtures from a `resources/` directory:

```yaml theme={null}
schema_version: "1.1"
name: changelog-from-diff
tags: [smoke]
context:
  scaffold_script: fixture.sh
  add_dirs: [resources]
```

<h3 id="mock-mcp-servers">
  Mock MCP servers
</h3>

You can evaluate a plugin whose skills call MCP tools without the real service behind them. Put one Markdown file per tool under `evals/mocks/<server>/<tool>.md` for the whole suite, or under a case's own `mocks/` directory for one case, where `<server>` is the server's name in your plugin's [MCP configuration](/docs/en/plugins-reference#mcp-servers).

A run never starts your plugin's real MCP servers unless you ask. Claude Code registers a stand-in under each server's own name. Tools with a mock file answer from it and are allowed without an `--allow-tools` grant, and a tool with no mock file isn't available to Claude. A server with no mocks at all appears in the case's `mocked:` progress line as `plugin_<plugin>_<server>[not started: no mock]`.

The file's body is what the tool returns to Claude. This mock stands in for a `create_issue` tool on a server named `tracker`, checks the input Claude sends, and echoes the title back. Save it as `evals/mocks/tracker/create_issue.md`:

```markdown theme={null}
---
expect:
  title: string
  priority: [low, medium, high]
---

Created issue #4821: {{input.title}}
```

Insert fields from the call's input with `{{input.<field>}}`, and the contents of a fixture file beside the mock with `{{file:fixtures/{input.<field>}.json}}`. The `expect:` block guards the input. If a call violates it, the run aborts with score 0 and records why, so a case can assert what your plugin asked the server to do. Set `error: true` to return the body as a tool error instead, or `type: agent` to have a small model answer as the server from instructions in the body. The [mock file reference](#mock-files) lists every key and the `_server.md` and `_tools.json` files.

To grade the calls themselves, point a grader at `target: mock_calls`.

To run against the plugin's real MCP servers instead, pass one of these flags. Either way those processes run as you, outside the run's sandbox, and their tools need an [`--allow-tools` grant](#grant-tools):

* **`--allow-real-servers`**: start the real process for each server you haven't mocked, and keep answering mocked tools from their files
* **`--mocks off`**: ignore `mocks/` entirely and start every server the plugin declares

#### Replay agent mock answers

A `type: agent` mock answers with a call to the [`--judge-model`](#command-options), so its output varies between runs and changes if you change the judge. When a run completes without an error or abort, Claude Code saves each answer an agent mock gave under the results directory in `mock-recordings/`.

Open `ADOPT.txt` there to see each recording and the `.replay/<server>/` directory to copy it into, beside the mock that produced it. After you copy a recording there, later runs answer the identical call from it with no model call. Commit `mocks/.replay/` with the rest of `mocks/` so CI runs are repeatable.

## Run evals

Once a suite exists, `claude plugin eval` runs it. You choose which plugin and cases run with the target argument, grant any tools the cases need beyond the read-only set with `--allow-tools`, and control run count, models, cost, and output with the other options.

### Choose what to evaluate

Most of the time you run `claude plugin eval .` from the plugin root, which runs every case in the suite with the plugin you're standing in loaded. To run a single case file, or to evaluate a plugin you installed rather than one you're developing, pass a different target:

| Target                                                    | What runs                                                                                                                                                                                         |
| :-------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A plugin's root directory, such as `.`                    | Every case under its eval directory, with that plugin loaded                                                                                                                                      |
| A single `prompt.md` or `case.yaml` file                  | That case, with its enclosing plugin loaded                                                                                                                                                       |
| An installed plugin by name, `name` or `name@marketplace` | The cases in the installed copy's eval directory, with the installed copy loaded. Results are written under `./evals/results/` in your current directory, or `./<dir>/results/` with `--eval-dir` |
| `name@skills-dir`                                         | The same, for a [skills-directory plugin](/docs/en/plugins-reference#skills-directory-plugins)                                                                                                         |
| Omitted                                                   | The current directory as a path                                                                                                                                                                   |

Add `--case <glob>` to filter by case name and `--tag <tag>` to keep cases with any of the given tags. Put the target before `--tag`, `--allow-tools`, and `--json`. The first two take a list and `--json` takes an optional path, so each of them reads a target that follows as its own value.

### Grant tools

Runs never stop to ask for permission. Built-in tools that need a grant you didn't give, such as `Bash`, `Write`, `Edit`, `WebFetch`, and `WebSearch`, are removed from the session, so Claude can't call them at all.

The allowlist is the read-only tools the case lists in `allowed_tools`, from `Read`, `Glob`, `Grep`, `NotebookRead`, `Skill`, `Agent`, `TodoWrite`, and the task tools `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate`, and `TaskStop`, plus whatever you grant with `--allow-tools`. That grant applies to every case in the run. To let cases use `Bash`, `Write`, `Edit`, `WebFetch`, or `WebSearch`, grant them yourself:

```bash theme={null}
claude plugin eval . --allow-tools Write Edit "Bash(npm test *)"
```

When a case asked for a tool you didn't grant, the run lists it on stderr as `not granted`. Tools on a [mocked](#mock-mcp-servers) MCP server need no grant. Tools on a real plugin MCP server need both the server started, with `--allow-real-servers` or `--mocks off`, and a grant by name, such as `--allow-tools "mcp__plugin_my-plugin_github__*"`; a plugin's MCP tools are named `mcp__plugin_<plugin>_<server>__<tool>`.

When you grant `Bash` in any form, every command runs under Claude Code's [OS-level sandbox](/docs/en/sandboxing). Writes are confined to the run's workspace, your home directory and Claude Code configuration are unreadable, and network access is limited to domains you grant with `--allow-tools "WebFetch(domain:example.com)"`. If you grant Bash or PowerShell on a machine with no sandbox backend, Claude Code refuses each run rather than running it unconfined, and the case shows a run error and usually scores 0. Native Windows has no backend, so run shell-granting suites under WSL2; on Linux, install `bubblewrap` and `socat` first. See the [sandboxing prerequisites](/docs/en/sandboxing).

### Command options

This table covers the options for run count, models, scoring, cost, tool grants, mocks, and output. Run `claude plugin eval --help` for the complete list, which also includes `--case`, `--tag`, `--eval-dir`, `--no-scaffold`, `--report`, and `--verbose`.

| Option                     | Default                                                                        | Effect                                                                                                                                                                                                                                                                                     |

## Eval suite reference

Everything an eval suite can contain lives under the plugin's eval directory, `evals/` unless you [configured another](#use-a-different-eval-directory). This tree shows every file `claude plugin eval` reads or writes there; only `prompt.md` or `case.yaml` is required for a case to exist:

```text theme={null}
evals/
├── <case>/                        # one directory per case; nest under a non-case directory to group
│   ├── prompt.md                  # frontmatter: case and run fields; body: the prompt
│   ├── case.yaml                  # optional: context.* fields, or the whole case in one file
│   ├── graders/
│   │   └── <name>.md              # one grader per file; frontmatter: type and options; body: rubric
│   ├── mocks/                     # optional: mocks for this case only, same layout as below
│   └── <fixtures, scripts, transcripts referenced by case.yaml>
├── mocks/                         # optional: suite-wide MCP mocks
│   ├── <server>/
│   │   ├── <tool>.md              # one mocked tool; body: the tool result
│   │   ├── _server.md             # optional: one agent that answers several tools
│   │   ├── _tools.json            # optional: saved tools/list response for real descriptions and schemas
│   │   └── fixtures/              # files inserted with {{file:fixtures/...}}
│   └── .replay/<server>/          # adopted agent-mock recordings, answered without a model call
└── results/<timestamp>/           # written by each run; add results/ to .gitignore
    ├── aggregate-result.json
    ├── report.html
    └── mock-recordings/           # agent-mock answers from clean runs, with ADOPT.txt
```

<h3 id="prompt-md-fields">
  prompt.md frontmatter
</h3>

`prompt.md` frontmatter accepts these fields. An unknown key is an error:

| Field                  | Default                      | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| :--------------------- | :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `schema_version`       | `"1.1"`, set for you         | Case format version. Cases written as `prompt.md` get it automatically, so you rarely set it                                                                                                                                                                                                                                                                                                                                                                                  |
| `name`                 | The directory name           | Case name. `--case` globs match it and the report keys on it                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `description`          |                              | For humans. Not used at run time                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `tags`                 | `[]`                         | Labels for `--tag` filtering. A case runs if any of its tags matches                                                                                                                                                                                                                                                                                                                                                                                                          |
| `plugins`              | The nearest enclosing plugin | Plugin directories under test, relative to the case directory. Set `plugins: ["../.."]` when auto-detection doesn't find your plugin; see [the plugin didn't load](#the-baseline-arm-shows-no-plugin-or-delta-is-zero)                                                                                                                                                                                                                                                        |
| `runs`                 | `3`                          | Runs per arm, 1 to 50. `--runs` overrides it                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `expected_outcome`     |                              | For humans. Not used at run time                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `model`                | The child session's default  | Model for the agent under test. `--model` overrides it                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `max_turns`            | `10`                         | Turn cap, up to 200. Hitting it is recorded as a run error and usually lowers the score, so set it generously                                                                                                                                                                                                                                                                                                                                                                 |
| `timeout_seconds`      | `300`                        | Wall-clock cap per run, up to 3600                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `allowed_tools`        | `[]`                         | Tools the case wants, such as `[Read, Glob, Grep, Skill]`. Read-only tools are granted when listed here; for anything else, see [Grant tools](#grant-tools)                                                                                                                                                                                                                                                                                                                   |
| `append_system_prompt` |                              | Text appended to the child session's system prompt                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `env`                  | `{}`                         | Extra environment variables for the child session. Keys must match `EVAL_[A-Z0-9_]*`; any other key fails the run. The run inherits only an allowlist from your shell: basics such as `PATH` and locale, proxy and certificate settings, the variables that select and authenticate your model provider, most `ANTHROPIC_*` and `CLAUDE_CODE_*` configuration, and `EVAL_*`. To hand the plugin anything else, such as a toolchain setting, export it as an `EVAL_*` variable |

<h3 id="case-yaml-fields">
  case.yaml fields
</h3>

`case.yaml` describes the same case in YAML and adds the fields that point at other files. It requires `schema_version: "1.1"` and `name`. The `prompt.md` fields `description`, `tags`, `plugins`, `runs`, and `expected_outcome` go at the top level; `model`, `max_turns`, `timeout_seconds`, `allowed_tools`, `append_system_prompt`, and `env` go under `execution:`. When both files exist, `prompt.md` frontmatter overrides the matching `case.yaml` fields, the `prompt.md` body is the prompt, and `graders/*.md` are added after any graders listed in `case.yaml`.

These fields exist only in `case.yaml`:

| Field                     | Purpose                                                                                                                                                                                                                 |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `context.scaffold_script` | A Bash script in the case directory that runs in the empty workspace before Claude starts, to create fixture files or a git repository. It runs only when you pass [`--scaffold`](#add-setup-or-history-with-case-yaml) |
| `context.history_file`    | A `.jsonl` transcript in the case directory to resume. The case's prompt becomes the next user turn                                                                                                                     |
| `context.add_dirs`        | Directories inside the case directory that Claude may read during the run, granted read-only                                                                                                                            |
| `execution.prompt`        | The prompt, when you keep the whole case in `case.yaml` and omit `prompt.md`                                                                                                                                            |
| `graders`                 | A list of graders, each with a `name` plus the same keys a `graders/*.md` file takes in frontmatter. For `llm` graders, put the rubric in `criteria`                                                                    |

### Grader frontmatter

Every grader file under `graders/` takes these keys in frontmatter, plus the options for its type. The grader's name is the filename without `.md`:

| Key      | Default  | Purpose                                                                                                                                                                     |
| :------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`   | required | One of the [grader types](#grader-types)                                                                                                                                    |
| `weight` | `1`      | Relative weight in the run's score. Any positive number                                                                                                                     |
| `arm`    | unset    | `with-only` excludes the grader from scoring in a [two-arm run](#compare-against-a-no-plugin-baseline); `both` forces a `tool_used: Skill` grader to be scored in both arms |

#### What a grader can look at

`regex` graders take a `target` and `llm` graders take a `focus`. Both accept the same values:

| Value                            | What the grader sees                                                                                                                                                                                                                                                                                           |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `last_message`                   | Claude's final response text. This is the default                                                                                                                                                                                                                                                              |
| `trace`                          | The session as JSON, one message per line. A `regex` grader sees every message; an `llm` judge sees the first 12 and the last 12. Quotes and newlines inside it are JSON-escaped, so a regex matches `\"` rather than `"`                                                                                      |
| `files`                          | The list of paths Claude created during the run, one per line. Not their contents, and not files that a scaffold created or that Claude only modified                                                                                                                                                          |
| `{ source: file, path: <path> }` | The contents of one file in the workspace after the run. Use this to grade what the plugin produced. A PNG, JPEG, GIF, or WebP file is shown to an `llm` judge as an image. An `llm` judge refuses other binary files such as `.pptx` or PDF; render them to an image or write them out as text and grade that |
| `mock_calls`                     | Each call Claude made to a [mocked MCP tool](#mock-mcp-servers), with its input and the mock's answer                                                                                                                                                                                                          |

#### Grader types

Each grader type below lists its options and when it passes:

| Type          | Options                               | Passes when                                                                                                                                                                                                                  |
| :------------ | :------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `regex`       | `pattern`, `flags`, `match`, `target` | The JavaScript regex `pattern` is found in the target. Set `match: not_contains` to require absence or `match: "count:N"` to require exactly N matches. Put case-insensitivity in `flags: i`; inline `(?i)` isn't supported  |
| `tool_used`   | `tool`, `input_match`, `min`, `max`   | The number of calls to `tool` whose JSON-encoded input matches the optional `input_match` regex is between `min`, default 1, and `max`, default unlimited. To assert a tool was never called, set both `min: 0` and `max: 0` |
| `tool_order`  | `before`, `after`                     | Both tools were called and the first matching `before` call precedes the first matching `after` call. Each is a tool name or `{ tool, input_match }`                                                                         |
| `file_exists` | `path`, `exists`                      | A file Claude created matches the `path` glob, or none does with `exists: false`. Only files created during the run count                                                                                                    |
| `llm`         | `criteria`, `focus`                   | A judge model votes PASS on the rubric in at least two of three votes. In the `.md` layout the file body is the criteria                                                                                                     |
| `baseline`    | `baseline_file`, `criteria`           | A judge finds the run satisfies the criteria at least as well as the reference transcript at `baseline_file`, a `.jsonl` in the case directory                                                                               |

<h3 id="mock-files">
  Mock files
</h3>

A `<tool>.md` file under `mocks/<server>/` answers one tool. Its body is the tool result, with `{{input.<field>}}` and `{{file:fixtures/<name>}}` substitutions. Its frontmatter accepts these keys:

| Key          | Default | Purpose                                                                                                                                                                                                                                                                             |
| :----------- | :------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`       | `fixed` | `fixed` returns the body as written. `agent` treats the body as instructions for a small model that plays the server for the run and sees earlier calls as history                                                                                                                  |
| `expect`     | unset   | A map from dotted input paths to a type name such as `string`, `number`, `boolean`, `array`, or `object`, a `/regex/`, a literal, or a list of allowed literals. A call that violates it aborts the run with score 0 and is reported as `aborted` with the server, tool, and reason |
| `error`      | `false` | `fixed` only. Return the body as a tool error                                                                                                                                                                                                                                       |
| `abort_when` | unset   | `agent` only. Prose listing the only conditions under which the agent may abort the run                                                                                                                                                                                             |

Two optional files sit beside the tool files in a server's directory:

* **`_server.md`**: a single `type: agent` mock that answers several tools, listed in its `tools:` frontmatter key. A `<tool>.md` for the same tool takes precedence. Put an `expect:` guard on the individual `<tool>.md`, not here
* **`_tools.json`**: a saved `tools/list` response from the real server, so mocked tools carry their real descriptions and input schemas instead of a permissive placeholder

A case's own `mocks/` directory uses the same layout and overrides the suite's mocks file by file.

