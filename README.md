# skills

Personal agent skillhub. Each skill is a standard Agent Skill directory
(`SKILL.md` with YAML frontmatter) installed into local agent skill
directories with [kitup](https://github.com/lathe-cli/kitup).

## Skills

| Skill | Description |
| --- | --- |
| [ops-verification-gate](skills/ops-verification-gate/SKILL.md) | 高风险运维事件门禁：只读诊断 → 明确授权 → 单一最小变更 → 可回滚执行 → 独立真实状态验收 |
| [production-project-iteration](skills/production-project-iteration/SKILL.md) | 非琐碎项目变更闭环：需求定界 → 受限委派 → 独立验证 → 受控部署 → 线上验收（PR/CI/GitOps/生产） |

## Install

Requires Python 3 and a network route to public GitHub (kitup fetches via
`api.github.com` / `raw.githubusercontent.com` without authentication, so
this repository must stay public).

```sh
pip install kitup-sdk
python3 install.py            # install or update both skills
python3 install.py --dry-run  # preview target directories
python3 install.py --ref v1   # pin a tag instead of main
```

Targets (user scope), per `hosts.json`:

- Kimi Code CLI: `~/.kimi-code/skills/<name>/`
- Codex: `~/.codex/skills/<name>/`

`hosts.json` overrides kitup's built-in host table for `kimi-cli`, whose
upstream path mapping predates the official Kimi Code user skills directory
(`~/.kimi-code/skills/`); see the
[Kimi Code skills docs](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html).

Installed copies are owned by app id `nmem`: re-running `install.py`
updates them in place, and `kitup`'s uninstall API removes every owned copy.
