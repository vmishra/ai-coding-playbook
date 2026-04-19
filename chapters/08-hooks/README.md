# Chapter 8 — Hooks and Automation

> Policy as code. The primitive that makes agentic coding safe enough for a real engineering org.

---

## The concept

An agent loops through tool calls. A **hook** is a shell command (or HTTP endpoint) the runtime executes on specific events in that loop — before a tool runs, after it runs, when the session starts, when it stops, when compaction happens, when a file changes on disk. The hook sees the event's payload, does what it needs to do, and optionally *returns a decision* that the runtime honors: allow, deny, modify, or warn.

Hooks are the layer where policy lives. Not policy documents — policy that *executes*. If your team has rules like "no one edits production migrations from their laptop" or "secrets must be scrubbed before they hit the model's context" or "the formatter runs after every edit," a hook is the right shape.

They sit orthogonal to everything else you've built so far:

- Memory tells the agent what's true.
- Commands, skills, and MCP give the agent capability.
- Hooks control what the agent is actually *allowed to do*, and what side effects happen around its actions.

## What hooks are good for

Five patterns that pay for themselves immediately:

1. **Blocking destructive commands.** `rm -rf`, `git push --force`, database drops, deletes in production configs. A pre-tool-use hook with a regex is five lines and catches real mistakes.
2. **Secret redaction.** A pre-tool-use hook scrubs API keys and PII from shell outputs and file reads before they reach the model context. Especially important when you're operating on real customer data.
3. **Auto-formatting and linting.** Post-tool-use hook on edits: run the formatter, run the linter, if it fails let the agent see the error and self-correct. Keeps diffs clean without you nagging.
4. **Build gates.** After any edit to a core file, run a fast typecheck or smoke test. If it fails, surface the error to the agent immediately instead of 20 turns later.
5. **Audit logging.** Every tool call appended to a local JSONL with timestamp, tool, inputs (redacted), decision, and outcome. Priceless for debugging why an agent did something weird, and the basis of any serious compliance story.

Hooks become the backbone of your team's "safe defaults" for agentic coding. Memory teaches the agent the house rules; hooks enforce them.

## When *not* to use a hook

- **"When someone asks for X, do Y."** That's a skill, not a hook. Hooks run on events, not on intent.
- **"Always behave a certain way in file X."** That's a path-scoped memory rule or skill, not a hook.
- **Complex multi-step workflows.** A hook should be a small, fast, single-purpose check or transform. If it's 200 lines, it's an internal tool with a wrapper, invoked by the agent when relevant.

## The universal hook pattern

Both Gemini CLI and Claude Code converge on the same design, with slightly different event names:

1. **The event fires.** The runtime calls your hook, passing a JSON payload on stdin (or in an HTTP body).
2. **Your hook runs.** It has access to the tool name, inputs, file paths — whatever the event exposes. It can inspect, log, modify, or decide.
3. **Your hook returns.** Three conventions, consistently:
   - **Exit 0 + JSON on stdout** → fine-grained control (allow/deny/ask, reason, modifications).
   - **Exit 2** → hard block; stderr is surfaced to the agent as an error.
   - **Other nonzero exit** → non-blocking warning.

Internalize that pattern. The two tools' event lists differ; the protocol is the same.

## Design principles

### 1. Hooks must be fast

Every event is in the hot path. A 2-second hook on `PreToolUse` makes every tool call 2 seconds slower. Stay under 100ms unless you have a specific reason.

### 2. Fail closed for safety, open for convenience

For a block-destructive-commands hook: fail closed (if the hook crashes, the tool doesn't run). For an auto-formatter: fail open (if prettier crashes, the edit still succeeds).

### 3. Hooks are code — version them

Check hooks into the repo. Review changes to them. A hook that blocks `rm -rf` in the billing repo deserves the same treatment as the code it protects.

### 4. Keep logic out of settings.json

`settings.json` should *configure* the hook (which event, which matcher, which script). The hook itself is a real file in `.claude/hooks/` or `.gemini/hooks/` — with comments, tests, and a clear name.

### 5. Test your hooks out-of-band

Run the hook script with a fake payload on stdin. Confirm it behaves. Both tools swallow hook stdout/stderr in interesting ways; don't rely on printf debugging.

## Realizations

- [Claude Code — Hooks walkthrough](./claude-code/README.md) — every event, config shape, output protocol, block-rm-rf example.
- [Gemini CLI — Hooks walkthrough](./gemini-cli/README.md) — event list, config shape, matching, security-check example.

## A word on blast radius

A hook that does the wrong thing runs on every matching event. If your block-rm hook is misconfigured, you might block all Bash calls, or none. Before rolling out a hook to the team, run it in your own environment for a week. Treat hooks with the seriousness you'd treat production code — because that's what they are.

## References

- Claude Code — [Hooks reference](https://docs.claude.com/en/docs/claude-code/hooks)
- Gemini CLI — [Hooks docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/index.md)
