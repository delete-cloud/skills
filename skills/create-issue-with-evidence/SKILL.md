---
name: create-issue-with-evidence
description: Prepare and file a bug report or issue with a verified problem statement, a reproducible procedure, and, for open-source projects, linked code locations and a suggested fix. Use when the user asks to report, file, draft, or write up an issue or bug for a project.
---

# Create Issue With Evidence

Write an issue that a maintainer can confirm without asking a follow-up question. The issue must explain the observed failure, how to trigger it, and why it happens when that is known. It is not a narrative of the investigation.

## Repository Rules

The target project's instructions take priority over this skill. Before you draft, read `CONTRIBUTING.md`, `SECURITY.md`, `.github/ISSUE_TEMPLATE/`, and any issue forms.

- If the project has an issue template or form, keep its required fields. Add the sections from this skill that improve triage.
- Use the project's labels, title conventions, and version reporting format.
- If the bug is a security vulnerability, stop. Follow `SECURITY.md` or the private disclosure channel. Do not file a public issue.

## Workflow

1. Confirm the target: the repository or tracker, and whether the project is open source. Ask the user if it is ambiguous. Never guess a repository URL.
2. Search existing issues and pull requests, open and closed, for the error string, symbol names, and symptoms. If a match exists, propose a comment on that issue with new evidence instead of a duplicate.
3. Collect the environment: product version, build or commit, install method, OS and architecture, and relevant configuration. Record the version that you actually inspected.
4. State the problem. Separate the observed behavior, the expected behavior, and the user impact.
5. Reproduce the failure. Follow the reproduction workflow below. If you cannot reproduce it, say so and state what you tried.
6. For an open-source project, trace the failure to code. Follow the code location workflow below.
7. For an open-source project, optionally propose a fix. Follow the fix proposal rules below.
8. Read [the issue body template](references/issue-body.md). Compose the body from verified evidence only.
9. Redact the body. Follow the redaction rules below.
10. Show the final title and body to the user. File it only after the user confirms the target and the content.
11. File through the available `gh` or tracker workflow. Then open the issue and verify the title, labels, code blocks, links, and rendering.

## Problem Statement

- Lead with one sentence that names the failing component, the trigger, and the effect.
- Quote the exact error message, error code, or log line. Do not paraphrase an error.
- State expected and actual behavior as a pair.
- State the impact: frequency, scope, data loss, security effect, and whether a workaround exists.
- Separate verified facts from inference. Label each inferred cause as `Suspected` until code or a reproduction confirms it.

## Reproduction Workflow

The reproduction is the most valuable part of the issue. Make it run in an environment that the maintainer controls.

1. Reduce the trigger to the smallest sequence of steps, commands, or API calls that causes the failure.
2. Reproduce it in an isolated environment: a fresh session, a scratch directory, a container, or a throwaway account. Do not use production state as the only evidence.
3. Run the reproduction at least once from a clean start. Record whether it fails every time or intermittently, and the observed rate when it is intermittent.
4. When the failure depends on timing or a race, describe the window and how the reproduction hits it. Provide a script when manual timing is unreliable.
5. Capture the evidence that proves the failure: the exact error output, a log excerpt with timestamps, an exit code, or a response body. Trim it to the relevant lines and keep the order.
6. Map the reproduction timeline to the original incident when one exists. Show that both produce the same signature.
7. Clean up the reproduction: terminate test sessions, delete scratch resources, and state any residual state that remains.

If the reproduction requires a private environment, explain which conditions a maintainer must recreate. Mark the issue `Not reproduced in isolation` when that is true.

## Code Location Workflow

Apply this workflow only to an open-source project, or when the user can share the code.

1. Locate code in the public source at a stable revision: a tag or a commit SHA. Do not link to a moving branch head.
2. Link each location as a permalink with a line range. Name the symbol in the link text.
3. Cover the failure path from the entry point to the throw site. Include the state owner and the code that should have cleaned up or guarded the state.
4. If you inspected a bundled, minified, or installed build instead of source, say so. Give the version and the symbol names. Do not present bundle line numbers as source line numbers.
5. Keep each quoted snippet short. Quote only the lines that prove the claim.

For a closed-source project, omit this section. Describe the behavior through public interfaces, logs, and error codes.

## Fix Proposal Rules

This section is optional. Include it only for an open-source project, and only when the analysis supports it.

- Describe the fix direction and the invariant it restores. A full patch belongs in a pull request.
- When several fixes are possible, list them with their trade-offs. Recommend one and give the reason.
- Name the side effects and the safety logic that the fix must preserve. Do not suggest swallowing an exception when the surrounding code depends on it.
- Suggest a regression test that encodes the reproduction.
- Mark the proposal as a suggestion. The maintainers own the design decision.

## Redaction Rules

- Remove tokens, keys, cookies, passwords, and credential file contents.
- Replace user IDs, emails, hostnames, internal IPs, workspace IDs, and private repository names with placeholders unless the maintainer needs them. Keep placeholders consistent across the body.
- Replace absolute home paths with `~` or a placeholder.
- Keep session, request, or trace IDs only when the maintainer can use them to look up server-side logs.
- Inspect the final body for secrets before you show it to the user.

## Issue Body Contract

Use the structure in [the issue body template](references/issue-body.md). Match the detail to the severity and the complexity of the failure.

- Every issue needs `## Problem`, `## Environment`, and `## Reproduction`.
- Add `## Root cause analysis` when code or logs confirm the mechanism.
- Add `## Related code` only for an open-source project.
- Add `## Suggested fix` only for an open-source project, and only when the analysis supports it.
- Add `## Workaround` when one is verified.
- Keep a simple bug report short. Do not add a section only to satisfy the template.

Do not write "always," "never," "root cause," or "fixed by" without evidence. Write `Not verified` for any claim that you did not check.
