# skills

English | [中文](README.zh-CN.md)

Personal agent skillhub. Each skill is a standard Agent Skill directory
(`SKILL.md` with YAML frontmatter) installed into local agent skill
directories with [kitup](https://github.com/lathe-cli/kitup).

## Skills

| Skill | Description |
| --- | --- |
| [ops-verification-gate](skills/ops-verification-gate/SKILL.md) | High-risk ops-event gate: read-only diagnosis → explicit authorization → single minimal change → rollback-capable execution → independent real-state acceptance |
| [production-project-iteration](skills/production-project-iteration/SKILL.md) | Closed loop for non-trivial project changes: scope definition → constrained delegation → independent verification → controlled deployment → production acceptance (PR/CI/GitOps/production) |
| [e2e-review-evidence](skills/e2e-review-evidence/SKILL.md) | Verify e2e coverage and PR review conclusions: real versus substitute paths, execution evidence, failure diagnosis, and project-specific review gates |
| [review-checklist](skills/review-checklist/SKILL.md) | Review beyond the diff: trace lock-wait chains to request handling, check timeout/TTL arithmetic at realistic scale, inspect caller and maintainer history, and assign distinct review lenses |
| [confer-review](skills/confer-review/SKILL.md) | confer MCP multi-seat review orchestration: seat roster (swe-2-max/grok-4.7/gpt-6-astra/opus-5-5), message patterns, claude seat failure modes and fallbacks |
| [create-pr-with-evidence](skills/create-pr-with-evidence/SKILL.md) | Create evidence-backed PRs: precise change range (base...head), architecture/behavior diagrams, risk mapping, and UI before/after screenshots (vendored from [luoling8192/create-pr-with-evidence-skill](https://github.com/luoling8192/create-pr-with-evidence-skill), MIT) |
| [create-issue-with-evidence](skills/create-issue-with-evidence/SKILL.md) | Create evidence-backed issues: verified problem statement, reproducible steps, plus code locations and a suggested fix for open-source projects |
| [teaching-assistant](skills/teaching-assistant/SKILL.md) | Teaching-assistant mode, not a code generator: Socratic questioning, hints over answers, 2-5 line micro-examples; for coursework, textbook/course study, or tutor mode |
| [lody-duo](skills/lody-duo/SKILL.md) | Lody host workflow: the current session keeps goal, authorization, and acceptance, and delegates investigation, implementation, and independent review to Lody Agent Roles via Lody MCP (vendored from [samzong/samzong](https://github.com/samzong/samzong/tree/main/.agents/skills/lody-duo), MIT) |
| [liability-review](skills/liability-review/SKILL.md) | Read-only review of a local diff or existing PR for correctness, evidence, and maintainer risk; findings need a concrete failure path; required by lody-duo's Review roles (vendored from [samzong/samzong](https://github.com/samzong/samzong/tree/main/.agents/skills/liability-review), MIT) |
| [critical-bug-finder](skills/critical-bug-finder/SKILL.md) | Scoped audit for critical implementation bugs only: crash, data corruption, security bypass, deadlock/race, or broken core logic; every finding needs a concrete trigger, real failure mode, and severe consequence (vendored from [samzong/samzong](https://github.com/samzong/samzong/tree/main/skills/critical-bug-finder), MIT) |
| [confer](skills/confer/SKILL.md) | Coordinate Claude Code, Codex, Cursor Agent, Grok, Antigravity CLI, Copilot CLI, and Kimi Code through private local MCP rooms: seat selection, relays, independent investigation, and synthesized verified results (vendored from [delete-cloud/confer](https://github.com/delete-cloud/confer/tree/main/skills/confer)) |

## Install

Requires Python 3 and a network route to public GitHub (kitup fetches via
`api.github.com` / `raw.githubusercontent.com` without authentication, so
this repository must stay public).

```sh
uv run --with kitup-sdk python3 install.py            # install or update all skills
uv run --with kitup-sdk python3 install.py --dry-run  # preview target directories
uv run --with kitup-sdk python3 install.py --ref v1   # pin a tag instead of main
```

Prefer `uv` over `pip` on every machine; only fall back to
`pip install kitup-sdk && python3 install.py` when uv is unavailable.

Workflow: install from `main` only, after PRs merge. Installing from a
PR branch (`--ref <branch>`) records that branch in each installed
copy's `.kitup.json` provenance, and deleting the branch leaves a stale
ref — kitup will not rewrite it on a same-hash reinstall. To preview a
skill before merge, copy the skill directory into a skills dir manually
instead.

Targets (user scope), per `hosts.json` and kitup's built-in host table:

- Kimi Code CLI: `~/.kimi-code/skills/<name>/`
- Codex: `~/.codex/skills/<name>/`
- Devin: `~/.config/devin/skills/<name>/`

`hosts.json` overrides kitup's built-in host table for `kimi-cli`, whose
upstream path mapping predates the official Kimi Code user skills directory
(`~/.kimi-code/skills/`); see the
[Kimi Code skills docs](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html).

Installed copies are owned by app id `nmem`: re-running `install.py`
updates them in place, and `kitup`'s uninstall API removes every owned copy.
