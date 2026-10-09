#!/usr/bin/env python3
"""Install skills from this repository into local agent skill directories.

Uses kitup-sdk with a github_bundle source, so installed copies carry
github provenance (owner/repo/path/resolvedCommit) in their .kitup.json
metadata. Re-running this script updates kitup-owned installs in place.

Usage:
    pip install kitup-sdk
    python3 install.py            # install/update all skills
    python3 install.py --dry-run  # preview targets
    python3 install.py --ref v1   # pin a tag/branch instead of main
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from kitup import (
    BaseOptions,
    GitHubBundleOptions,
    InstallOptions,
    github_bundle,
    install_bundled_skill,
    plan_bundled_skill,
)

OWNER = "delete-cloud"
REPO = "skills"
SKILLS = [
    "ops-verification-gate",
    "production-project-iteration",
    "create-pr-with-evidence",
    "create-issue-with-evidence",
]
AGENTS = ["kimi-cli", "codex", "devin"]  # kimi-cli needs the hosts.json override below
APP_ID = "nmem"

REPO_ROOT = Path(__file__).resolve().parent
HOSTS_FILE = REPO_ROOT / "hosts.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="main", help="git ref to install from")
    parser.add_argument("--dry-run", action="store_true", help="preview only")
    args = parser.parse_args()

    base = BaseOptions(home=str(Path.home()), hosts_file=str(HOSTS_FILE))
    failed = False

    for skill in SKILLS:
        bundle = github_bundle(
            GitHubBundleOptions(
                owner=OWNER,
                repo=REPO,
                path=f"skills/{skill}",
                ref=args.ref,
            )
        )
        options = InstallOptions(
            base=base,
            app_id=APP_ID,
            skill_bundle=bundle,
            scope="user",
            agents=AGENTS,
        )
        report = plan_bundled_skill(options) if args.dry_run else install_bundled_skill(options)
        targets = [(t.host_id, t.target_dir) for t in report.installed + report.updated]
        print(f"{skill} ({'plan' if args.dry_run else 'installed'}):")
        for host_id, target_dir in targets:
            print(f"  {host_id}: {target_dir}")
        if report.conflicts or report.errors:
            failed = True
            print(f"  conflicts={report.conflicts} errors={report.errors}", file=sys.stderr)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
