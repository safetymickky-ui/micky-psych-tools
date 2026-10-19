# design-md-generator

Generates a `DESIGN.md`: a plain-markdown design system that coding agents read to build
UI that stays on-brand. Follows the [Google Stitch DESIGN.md spec](https://stitch.withgoogle.com/docs/design-md/specification/)
(YAML token front matter plus ordered `##` sections), with the extended sections used by
[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md).

## Install

```
/plugin install design-md-generator --marketplace safetymickky-ui/micky-psych-tools
```

## Sources

| Mode | Input | Values come from |
|---|---|---|
| site | a URL | CSS custom properties + computed styles (firecrawl / built-in browser) |
| brief | a mood or product description | invented, labelled as such, contrast-checked |
| codebase | a project path | Tailwind config, `:root` variables, component classes |
| remix | a brand or kit to adapt | awesome-design-md (MIT) or the designmd MCP |

## Use

```
/design-md https://linear.app
/design-md calm healthcare scheduling app, light, accessible
/design-md ./my-app
/design-md like Vercel but with a warm orange accent
```

Or ask in words, for example "make a DESIGN.md for this project".

Every file is linted with `npx @google/design.md lint` (broken references, WCAG contrast,
structure) before it is reported done. An existing `DESIGN.md` is never overwritten; a
`DESIGN.next.md` and a diff are produced instead.

## Optional: designmd MCP

Remix mode can search designmd.ai kits through the `designmd-mcp` server. It is not bundled
(it needs a personal API key). Install it at user scope:

```
claude mcp add -s user designmd -e DESIGNMD_API_KEY=<your-key> -- npx designmd-mcp
```

## Layout

```
commands/design-md.md
skills/design-md-generator/SKILL.md
skills/design-md-generator/references/format.md    # spec digest + skeleton + quality bar
skills/design-md-generator/references/sources.md   # per-mode extraction recipes
```
