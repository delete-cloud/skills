# skills

Personal agent skillhub. Each skill is a standard Agent Skill directory
(`SKILL.md` with YAML frontmatter) installed into local agent skill
directories with [kitup](https://github.com/lathe-cli/kitup).

## Skills

| Skill | Description |
| --- | --- |
| [ops-verification-gate](skills/ops-verification-gate/SKILL.md) | 高风险运维事件门禁：只读诊断 → 明确授权 → 单一最小变更 → 可回滚执行 → 独立真实状态验收 |
| [production-project-iteration](skills/production-project-iteration/SKILL.md) | 非琐碎项目变更闭环：需求定界 → 受限委派 → 独立验证 → 受控部署 → 线上验收（PR/CI/GitOps/生产） |
| [confer-review](skills/confer-review/SKILL.md) | confer MCP 多席位评审编排：席位花名册（swe-2-max/grok-4.7/gpt-6-astra/opus-5-5）、消息模式、claude 席位失败模式与 fallback |
| [create-pr-with-evidence](skills/create-pr-with-evidence/SKILL.md) | 创建带证据的 PR：精确变更范围（base...head）、架构/行为图、风险映射与 UI 前后截图（vendored from [luoling8192/create-pr-with-evidence-skill](https://github.com/luoling8192/create-pr-with-evidence-skill), MIT） |
| [create-issue-with-evidence](skills/create-issue-with-evidence/SKILL.md) | 创建带证据的 issue：已验证的问题陈述、可复现步骤，开源项目附代码定位与修复建议 |

## Install

Requires Python 3 and a network route to public GitHub (kitup fetches via
`api.github.com` / `raw.githubusercontent.com` without authentication, so
this repository must stay public).

```sh
pip install kitup-sdk
python3 install.py            # install or update all skills
python3 install.py --dry-run  # preview target directories
python3 install.py --ref v1   # pin a tag instead of main
```

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
