# Chapter 21 — Advanced Workflows and Playbooks

> End-to-end recipes. Each one shows the whole discipline in motion — not a feature demo, a thing you'd actually do on a Tuesday.

---

## How to read this chapter

Each workflow below is a worked example. The template is the same:

1. **The situation.** What you're trying to do and why.
2. **The brief.** Exactly what you'd type / send.
3. **The flow.** How the session unfolds.
4. **What to watch for.** Failure modes specific to this workflow.
5. **The artifacts.** What lands in the repo when you're done.

You can copy any of these into your own `specs/` or `playbooks/` directory and adapt.

---

## Workflow 1 — Triaging a bug report

### Situation

A user filed a bug. Report is vague. Before you dive in, you want to know: is it real, is it us, what's the scope, what's the nearest fix.

### Brief (Gemini CLI or Claude Code)

```
## Outcome
A triage report for issue #1234.

## Scope
- Read the issue and any linked comments (`gh issue view 1234`).
- Read any logs/traces the reporter attached.
- Search the codebase for the relevant area; don't edit anything.

## Constraints
- Don't propose a fix yet. Triage first.
- If the bug might be user error, say so plainly — don't assume we're at fault.

## Deliver
- One-paragraph description of the actual behavior.
- Reproduction steps (even if they're "can't repro locally yet").
- Suspected cause with file paths and line numbers.
- Severity (sev1-4) with justification.
- Next step — "fix in PR", "needs more info from user", "not a bug".
```

### Flow

1. Agent fetches the issue.
2. Agent greps the relevant code.
3. Agent reads the logs.
4. Agent produces the triage.

### Watch for

- **"Can't repro" turning into "I think it might work."** If the agent can't reproduce, it can't triage. Accept the "need more info" outcome rather than pushing for a guess.
- **Scope creep into fixing.** Resist. Triage first, fix second. Two separate sessions.

### Artifacts

- `docs/triage/issue-1234.md` — the triage report, committed. Next time someone looks at this issue, it's there.

---

## Workflow 2 — Multi-file migration

### Situation

Moving a codebase from library A to library B. Twenty-five files affected. Straightforward per-file but tedious.

### Brief

```
## Outcome
All import and usage sites of `lodash` removed; replaced with vanilla ES
equivalents.

## Scope
- All .ts and .tsx files in src/.
- Not tests (they continue to use the library; different concern).
- Not the package.json change (I'll do that last, after all files are clean).

## Constraints
- Preserve semantic equivalence. `_.get(obj, 'a.b.c')` → optional chaining.
- Don't break TypeScript types. If a lodash function has subtle type
  handling the vanilla version doesn't, flag it rather than swap blindly.
- One PR per logical chunk (e.g., all `_.get` sites, all `_.map` sites),
  not one monster PR.

## Approach
- First: grep for every lodash import, group by lodash function used.
- Second: for each group, propose the replacement pattern (ONE example,
  for my approval).
- Third: once I approve the pattern, fan out via subagents — one per chunk.
- Fourth: run tests and typecheck after each chunk; don't proceed if red.
```

### Flow

1. Primary agent does the survey.
2. You approve the replacement patterns.
3. Primary spawns subagents for each group.
4. Each subagent fixes its chunk and runs targeted tests.
5. Primary aggregates and commits per group.

### Watch for

- **Subagents producing subtly different replacements for the same pattern.** Enforce the approved pattern explicitly in each subagent's brief.
- **One subagent failing silently.** Check all their outputs, not just the first.
- **Bulk commit.** Don't merge 25 files as one commit — even if they share a theme, grouping by concern preserves bisectability.

### Artifacts

- Multiple small PRs. A `docs/migrations/lodash-removal.md` write-up.

---

## Workflow 3 — Feature from spec to shipped

### Situation

You have a spec for a new feature. You want to go from spec to shipped without drifting.

### Brief

```
## Outcome
Feature implemented, tested, PR opened.

## Scope
- Read specs/notification-preferences.md fully.
- Implement it in the files listed in the spec's "files" section.
- Write tests matching the repo's existing conventions.
- Open a PR using our /pr-description skill.

## Constraints
- Do not extend scope beyond the spec. If something's ambiguous, stop and
  ask.
- Respect existing components, tokens, and patterns (see CLAUDE.md).
- Tests must run green before the PR.

## Process
1. Plan first (plan mode). Do not edit any file until I approve the plan.
2. Implement the feature.
3. Write tests. If any test exposes ambiguity in the spec, stop.
4. Run full test suite and typecheck. Fix until green.
5. Run /pr-description. Open the PR with gh.
```

### Flow

Plan → approve → implement → test → PR. Every step has a pause where you can redirect.

### Watch for

- **Agent expanding scope under "related cleanup."** Cut back hard.
- **Test failures silently softened.** Inspect any test the agent "fixed" — it may have reduced assertion strength rather than fixing real breakage.
- **PR description that sells.** Cut marketing language. Factual. Diff does the showing.

### Artifacts

- The implementation.
- New tests.
- A PR.
- Zero silent side effects.

---

## Workflow 4 — On-call triage

### Situation

You're on-call. A pager fired. You want to assess fast.

### Brief

```
## Outcome
A 90-second decision: ack and investigate, escalate, or stand down.

## Scope
- Read the alert: !{gcloud logging read "..."}
- Check the recent deploy history: !{gcloud run revisions list ...}
- Pull the relevant dashboards via the MCP observability server if available.

## Constraints
- Do NOT make any production change.
- Do NOT touch any Terraform, IaC, or config.
- If it looks like it warrants a rollback, tell me which revision to roll
  back to, don't do it.

## Deliver
- Two-sentence assessment.
- Suspected cause with confidence (low / medium / high).
- Recommended action.
- If escalating, which team owns the component.
```

### Watch for

- **Unauthorized write actions.** The brief above is read-only by design. Pair with a hook that hard-denies any deploy / terraform / kubectl apply during on-call sessions.
- **False confidence.** Low confidence assessments are valid outputs. "I don't know, escalate to team X" is often the correct answer.

### Artifacts

- A post-incident summary if the incident was real.
- Appendix to the on-call runbook if this exposed a gap.

---

## Workflow 5 — Research-driven decision

### Situation

Picking between approaches: do we use library A or B for this new feature?

### Brief

```
## Outcome
A decision doc at docs/decisions/<date>-<topic>.md with a recommendation.

## Scope
- Research both options on the web. Primary sources first.
- Read our existing code for any evidence of which would fit.
- Talk to no one; this is you synthesizing public info plus our codebase.

## Format (write to the file)
# <Topic>

## Decision
<1 sentence>

## Context
<what we're trying to do>

## Options considered
### A
Pros / cons / fit-with-our-stack / cited sources

### B
Pros / cons / fit-with-our-stack / cited sources

## Rationale
<why we picked what we picked>

## Open questions
<things we don't yet know, and how we'd resolve them>

## Constraints
- Every "pro/con" must cite a source or a specific code location.
- Don't pretend to know things you don't.
- If a third option is obvious and neither A nor B, flag it.
```

### Flow

Subagent researches each option → subagent reads local codebase for fit → primary synthesizes the doc.

### Watch for

- **Both options "balanced" regardless of facts.** Push back: "Be honest. If A is clearly better for our case, say so. If you can't tell, say that too."
- **Stale sources.** Require publish dates. Anything > 18 months old, verify against current docs.

### Artifacts

- A committed decision doc. Future you will thank you.

---

## Workflow 6 — Code review at scale

### Situation

You have 8 PRs open against your service. You need to triage them before standup.

### Brief

```
## Outcome
A short triage for each open PR: ready / needs-work / blocked-on-me.

## Scope
- For each PR in the current repo's open-PR list (`gh pr list`),
  read its diff and description.
- Don't leave GitHub comments.

## Deliver
A table:
| PR | Title | Status | Headline concern (if any) |
|---|---|---|---|
| #123 | ... | ready | — |
| #124 | ... | needs-work | Tests insufficient — `auth.ts:45` boundary case uncovered |

Plus a 1-sentence recommendation for the next-action PR.
```

### Watch for

- **Agent giving everything "needs-work" to seem diligent.** Calibrate it: "Half of these are probably fine. Be willing to mark them ready."
- **Headline concerns that aren't headlines.** "Missing a semicolon" is noise; "auth bypass on unauthenticated path" is a headline. Tune briefs over time.

### Artifacts

- A mental model of which PR to review next.

---

## Meta — what these have in common

Read the briefs above and notice what repeats:

- Four-part structure (outcome, scope, constraints, process/deliver).
- Plan-first / approval-checkpoint almost everywhere.
- Explicit restrictions on scope creep.
- Explicit "don't do X" where X is an obvious but wrong move.
- A named, committable artifact at the end.

This is the compound effect of Part I through Part V. The workflows are *applications*, not new techniques.

If you find yourself writing a new workflow from scratch every session, you haven't built the habits from the earlier chapters yet. Go back and work through one of them until briefing in this shape is automatic.

## What's next

You've reached the end of the book. Some next moves:

- Adapt the workflows above into `playbooks/` in your own repo.
- Fork this repo, extend the TOC with your team's specifics.
- Submit field reports — real case studies — via issue. The best feedback loop for this playbook is users who tried it and have notes.
- Go ship something.
