# Chapter 13 — Tool Connectivity: Google Cloud, BigQuery, Firebase, Internal APIs

> Wiring your agent into the systems that actually hold your data and run your production. Heavy on Google Cloud because that's where the native integration is strongest.

---

## The concept

So far we've used the agent to read code, edit code, run shell commands, and hit the open web. That covers 70% of coding work. The last 30% needs the agent to talk to *your* systems — cloud resources, databases, internal APIs, issue trackers, observability.

The protocol layer is MCP (Ch. 7). What this chapter covers is the authentication, scoping, and safety patterns specific to real production systems — the stuff that turns a cool demo into something a security team will sign off on.

## The three auth shapes

You'll encounter roughly three patterns across every system worth connecting:

### 1. User-delegated OAuth

The agent acts as *you*, via a flow where you log in once and an MCP server holds a refresh token.

**Pros:** Works with your personal permissions, no service account juggling, audit trail is unambiguous (it was you).

**Cons:** Cannot be shared; your laptop's token is your laptop's. Breaks when you change auth state.

**Use for:** your own local tools, personal automation, anything at an individual-engineer scope.

### 2. Service account / machine identity

The agent authenticates as a non-human identity with its own permissions. In Google Cloud, this is a service account key or, better, Workload Identity Federation.

**Pros:** Reproducible, sharable across team, scoped via IAM, clear permissions boundary.

**Cons:** Key management, potential for over-scoping, audit logs show "service account X" not "engineer Y" unless you're careful.

**Use for:** team-wide agent connections, CI-adjacent flows, anything you'll run more than ad-hoc.

### 3. Scoped token per-tool

Short-lived tokens scoped to exactly one operation. Increasingly common in modern MCP servers.

**Pros:** Principle of least privilege by construction. A compromised session compromises one operation.

**Cons:** More setup complexity.

**Use for:** anything touching production data or capable of state change.

## Principle of least privilege, applied

Every connection is a permission you're granting the agent. Three rules that survive any tool generation:

1. **Prefer read-only.** If the agent doesn't need to write, it shouldn't have write capability.
2. **Prefer scoped.** A server scoped to one project / one dataset / one dir is safer than one scoped to the whole cloud / the whole DB / `/`.
3. **Prefer auditable.** Every action should produce a log entry you can trace to a session and a prompt.

If you can't satisfy all three, you're probably over-granting. Push back on the connection until you can.

## Google Cloud integrations

Because this is a Google-first playbook, and because Google Cloud has the most developed native integration.

### gcloud MCP / auth

The canonical path is `gcloud auth application-default login`, which puts credentials at `~/.config/gcloud/application_default_credentials.json`. Any tool the agent runs that uses an official Google SDK picks these up automatically. This is the lowest-friction path for individual engineers.

For team setups, prefer Workload Identity Federation (no long-lived keys on laptops) — [docs](https://cloud.google.com/iam/docs/workload-identity-federation).

### BigQuery

A highly common agent use case: let the agent query BigQuery to answer data questions in context.

The safe shape:

- Give the agent **read-only** access to a specific dataset via IAM.
- Expose a small MCP server (or a skill) that validates queries before running them, enforces a LIMIT, and times out long-running queries.
- Never give the agent `bigquery.tables.delete` unless you have a very specific reason.

Official guidance: [BigQuery IAM overview](https://cloud.google.com/bigquery/docs/access-control).

### Firebase and Firestore

For full-stack agentic workflows, Firebase Studio (Ch. 14) already has Firebase integration baked in. For CLI use, connect via the Firebase Admin SDK under a service account scoped to the project you need.

Official: [Firebase Admin SDK docs](https://firebase.google.com/docs/admin/setup).

### Cloud Functions and Cloud Run

Agents are good at writing, deploying, and iterating on Cloud Functions / Cloud Run services. The risk isn't the writing; it's the deploying. Put a hook (Ch. 8) in front of any `gcloud run deploy` / `gcloud functions deploy` invocation that requires explicit approval for production projects. Dev projects can be more permissive.

### Cloud Workstations

Remote dev environments that persist across sessions. The Gemini CLI is pre-installed in most official images. See Ch. 14 for IDE-integration details.

### Secret Manager

When the agent needs a secret, pull it from Google Secret Manager rather than having the secret present in any file the agent might read. The pattern:

1. Secret lives in Secret Manager.
2. Your local environment has a small wrapper that fetches the secret and exposes it as an env var at session start.
3. The agent sees only the env var reference in configs; it never sees the secret value.

## Internal APIs

For internal services, the right shape is almost always "write a thin MCP server that wraps the API, running locally or on an internal host, authenticating via your team's SSO."

- Start read-only. Add write tools one at a time with explicit permission prompts.
- Document every tool with a description the agent can reason over: "Creates a new incident ticket. Use when the user asks to file an incident."
- Version the tool signatures; once a tool is in production use, renaming it breaks every session that relied on it.

Many teams host their internal MCP servers in a small `internal-agent-tools` repo with one folder per system. Good pattern.

## Observability is load-bearing

For any connection to a production system:

- **Every call produces a log entry** attributable to the session and the originating prompt.
- **The log is reviewed when things go wrong.** You want this habit in place before the first "why did the agent delete X" moment.
- **Rate limits are enforced at the server, not the client.** A misbehaving agent should hit a server-side rate limit and fail, not fan out 1,000 requests.

These aren't nice-to-haves. For anything touching production, they're the cost of doing business.

## Anti-patterns that bite

- **"Give the agent admin to save time."** You save 30 minutes. One bad prompt costs you a weekend and an incident review.
- **"Share a service account key in Slack so everyone can use it."** Now you don't know who did what, and the key lives in a channel forever.
- **"Put the API token in `CLAUDE.md` so the agent always has it."** The `CLAUDE.md` is loaded into every session and logged in every transcript. The token is now everywhere.
- **"It's just a read-only connection, it's fine."** Read-only to *which rows?* "SELECT * FROM users" is a read-only query you probably don't want the agent making.

## A good default connectivity shape for a team

- User OAuth or ADC for individual-engineer connections.
- Workload Identity Federation for team-shared service accounts.
- A small internal `mcp-tools` repo with per-service servers, each read-only by default.
- Hooks on any deploy commands.
- Audit log hook turned on for everyone.
- No secrets in memory files, commands, skills, or repos. Env vars sourced from Secret Manager or a local `.envrc` via direnv.

This gets you 95% of the value with a defensible security posture.

## References

- [gcloud auth docs](https://cloud.google.com/sdk/gcloud/reference/auth)
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [BigQuery IAM](https://cloud.google.com/bigquery/docs/access-control)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Secret Manager](https://cloud.google.com/secret-manager/docs)
- [MCP spec (Ch. 7)](https://modelcontextprotocol.io)
