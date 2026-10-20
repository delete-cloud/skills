---
name: review-checklist
description: Use when reviewing a PR or diff for problems outside the changed lines. Covers lock-wait chains that reach the request path, timeout/TTL/batch-size arithmetic at realistic scale, and silent regressions that a per-hunk read misses. Run it alongside the normal line-by-line review, not in place of it.
---

# Review checklist

Run every pass. A per-hunk read checks that the code does what it says. These passes check what the change does to the rest of the system.

## 0. Gather inputs first

- The diff and the PR description.
- Callers of every changed function, two levels up.
- Measured numbers for the touched path: cycle time, N, latency, benchmark output. If they are missing, ask for them.
- Defaults for every timeout, interval, TTL, batch size, pool size and concurrency limit that the diff touches or depends on.

## 1. Lock and wait-chain pass

Do this for every lock, semaphore, channel, WaitGroup or blocking call whose hold time, scope or set of waiters changes:

1. List the work done while it is held. Mark as slow: network I/O, disk I/O, plugin, callback or interface calls, and anything bounded only by a timeout.
2. List every waiter: each function that acquires it, found by grepping the whole repo, not just the diff.
3. For each waiter, record what it holds at that moment, such as other locks or an in-flight request.
4. Repeat step 3 for those held locks. Stop when the chain reaches either:
   - the request path: report it, or
   - a background loop with no further waiters: record it and stop.
5. Worst-case wait = hold time under failure (use the timeout, not the RTT) x the number of serial acquisitions.

Rules:
- "Cannot deadlock" is not "cannot stall". A deadlock test proves nothing about latency.
- Slow work inside a critical section whose chain reaches the request path is a finding candidate. Write out the concrete failure path: trigger, chain, stalled caller, duration. If you cannot write it out, downgrade to P3.
- With a writer-preferring RWMutex, a waiting writer blocks new readers. Include that in the chain.
- Rerun this pass on every fix. A fix for one race often moves I/O back under a lock.

## 2. Numbers pass

For each timeout, interval, TTL, batch size, pool size, concurrency limit and default in or affected by the diff, write one line with four items:
- the value,
- the quantity it competes with,
- the measured value of that quantity,
- the N where they cross.

Crossovers to check:
- Deadline vs cycle duration.
- TTL vs refresh interval plus the worst-case cycle.
- N / batch size vs concurrency: how many waves, and how long they take under timeout.
- Concurrency x concurrent callers vs connection pool size.
- Retries x timeout vs the caller's deadline.
- What a timeout bounds (per item, per chunk, per cycle), and whether that changed for users.

Rules:
- Scale measured values linearly unless there is evidence otherwise. State the assumption.
- "Documented" is not "acceptable". If behavior degrades inside the realistic range of N, report it even when the docs describe it accurately.

## 3. Beyond-the-diff pass

- Read the callers of changed functions and their callers. For each, note which locks it holds and whether it is on the request path.
- Run `git log` and `git blame` on the touched files. Read the commits that added locks or timeouts, or comments such as "must not" or "never".
- Search closed issues and PRs in the touched area for: stall, hang, deadlock, latency, timeout, leak.
- Write down every invariant you find that the docs do not state, for example "nothing slow under lock X, because the request path reads it". Check the diff against each one.
- For each new test, ask whether it fails if the change is reverted or regresses to its most likely wrong variant. A test that passes on both versions is not coverage.

## 4. Maintainer-model pass (upstream projects)

- Identify the area's owners from OWNERS, CODEOWNERS or blame.
- Skim about 20 of their recent review comments on that area. List the failure modes they raise repeatedly.
- Check the diff against that list. Treat each item as a question the maintainer will ask, and answer it in the review.

## 5. Multi-seat reviews

Give each seat a different lens and different inputs:
- **Lock seat:** pass 1. Include callers, datastore and runtime code, and request-path entry points in its context.
- **Numbers seat:** pass 2. Attach benchmarks and config defaults.
- **Correctness seat:** per-hunk semantics, error handling, tests.
- **History seat (optional):** passes 3 and 4.

Rules:
- Do not give every seat the same generic prompt or the same list of review interests. Identical inputs stack blind spots, so extra seats add agreement rather than coverage.
- Do not let the author's list of review interests define the scope. It reflects the author's blind spots.

## Reporting

For each finding, give:
- severity,
- `file:line`,
- the concrete failure path,
- the chain or arithmetic that supports it.

State which passes ran and which inputs were missing (for example: "no benchmark data; numbers pass used assumed N=1000").

## Worked example: a publication loop

A background loop publishes per-endpoint state to Redis each cycle. A change batched the writes. Four per-hunk reviewers accepted it. The maintainer found two problems.

Lock pass:
1. The loop held the publisher lock `p.mu` (read) for the whole batch, including the Redis I/O.
2. `delete()` takes `p.mu` (write), so each delete waited up to one full cycle.
3. `ReleaseEndpoint` calls `delete()`, and a resync loop calls `ReleaseEndpoint` once per endpoint while holding the datastore lock `ds.mu`.
4. Request routing takes `ds.mu` (read), so requests stalled for up to one cycle per removed endpoint.

The reviewers had checked deadlock-freedom and lock order. None asked what `ReleaseEndpoint`'s caller was holding.

The fix:
- Collect IDs under a short lock, do the I/O unlocked, then reconcile removals.
- A later fix ran the cleanup deletes under the write lock, which brought back a stall of K removals x contributors x timeout. Rerunning pass 1 on that fix caught it.

Numbers pass:
1. Benchmark: a 794ms cycle at N=1000. Default whole-cycle deadline: 1s.
2. 794ms x 1.3 = 1.03s, so unattempted tail endpoints start being dropped near N=1300, which is within realistic fleet sizes.

The reviewers had documented the per-cycle deadline instead of checking it against this number. The fix applies the timeout per chunk instead of per cycle.
