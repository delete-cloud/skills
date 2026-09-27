---
name: confer-review
description: Drive multi-seat peer review through the confer MCP server (devin swe-2-max, grok-4.7 high, codex gpt-6-astra, claude opus-5-5) for sre-main packets and receipts. Includes seat roster, message patterns, failure modes, and fallbacks learned from production use.
---

# Confer Multi-Seat Review

Orchestrate bilateral/multi-agent review of packets and receipts via the `confer`
MCP server. Seats are private by default: never paste one seat's answer into
another seat's prompt unless the user explicitly asks for critique or
collaboration.

## Room

- `list_rooms` with `scope: "current"` and `workspace` = the absolute task
  directory (normalized to the Git worktree root). Reuse an existing room for
  the same host session.
- `create_room` only for a new session or when the user asks for a fresh room.
- The main room for sre-main work: `forgejo-av-path-review`
  (`61347e6b-323b-496b-858e-792efefc5f98`).

## Seat roster (verified 2026-09)

| Seat | agent | model | reasoning_effort | Notes |
|---|---|---|---|---|
| devin | `devin` | `swe-2-max` | — | Strong on repo context; native session resumes well |
| grok | `grok` | `grok-4.7` | `high` | Reliable, fast; catches P2/P3 wording issues |
| codex | `codex` | `gpt-6-astra` | `medium` | (alias `astra-6` also seen) Good on concrete failure paths |
| claude | `claude` | `claude/claude-opus-5-5` | `medium` | See failure modes below |

A seat that sets `model` or `reasoning_effort` must also set `agent`.

## Message pattern

`send_message` with `recipients` = seat names (or `"*"` to broadcast). Every
recipient gets a `delivery_id`; collect answers with `wait_output`. Seat queues
are per-seat FIFO — a second message waits behind a running delivery.

For reviews, give the seat everything it needs inline:

- the decision/verdict asked for (e.g. `accept` vs `changes-required`)
- the severity rubric: **P1** blocking (concrete failure path violates hard
  rules / unsafe production outcome), **P2** blocking (in-scope defect making
  the artifact misleading/unverifiable/unsafe to run, stop, or roll back),
  **P3** non-blocking, **Question/Nit**
- the packet/receipt path or inline diff, plus exact scope boundaries
- a reminder that speculative risk without a concrete failure path is at
  most P3 (matches `AGENTS.md`)

## Failure modes and fallbacks (learned 2026-09-27)

- **Claude seats die `error=unknown` on long-running tasks** (~25–50 min,
  typically when asked to read large files or carry heavy accumulated
  context). Mitigation: keep prompts bounded, inline the review material
  instead of asking the seat to walk the repo, cap file reads. A fresh seat
  does NOT fix this — task size does.
- **Claude model naming via the magpie gateway** (`ANTHROPIC_BASE_URL=https://magpie.kinaz.me`):
  - works: `claude/claude-opus-5-5`, `claude/claude-opus-5`,
    `claude/claude-opus-4-8`, `claude/claude-sonnet-5`, `claude/claude-haiku-4-5-20251001`
  - fails: bare `claude-opus-5-5[1m]` (CLI default appends the 1M-context
    variant suffix; gateway doesn't know it), bare `claude-opus-4-5`
  - `/v1/models` omits all claude entries — do not validate against the
    list; test `/v1/messages` directly
- **Direct fallback:** `timeout 240 claude -p "<prompt>" --model
  "claude/claude-opus-5-5"` works when seats die (verified). Confer seat
  failure ≠ model unavailability.
- **Gateway upstream flap:** magpie routes to a Claude subscription backend
  over tailnet (grokbot-box); transient 4xx/5xx bursts recover on their own.
  Re-test before assuming persistent breakage.
- Two-seat quorum (codex + grok) is acceptable when claude is unavailable;
  record the missing seat in the receipt rather than blocking.

## Review loop

1. Write packet → commit on a `ops/`/`docs/` branch → open PR.
2. Broadcast the packet to seats with the rubric above.
3. Apply P1/P2 fixes (and cheap P3s) as revision commits; re-send only the
   changed hunks plus a delta note.
4. Repeat until accept; record each seat's verdict and round in the receipt.
5. Execute only after explicit user authorization; write the receipt with
   exact commands, timestamps, counters, and rollback verification.
