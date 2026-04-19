# Chapter 20 — Agent SDKs: Google ADK and Claude Agent SDK

> When the CLI isn't enough. Building custom, programmatic agents on top of Gemini or Claude — including multi-agent systems that do real work.

---

## When you need this

The CLIs in earlier chapters (Gemini CLI, Claude Code) are the right answer for 90% of an engineer's daily work. You hit the ceiling when you need:

- **An agent embedded in your product**, not a developer tool.
- **Multi-agent systems**: an orchestrator coordinating specialists, persistent agents that live beyond a session, agents triggered by events.
- **Fine-grained control** over the agent loop — custom tool routing, custom memory, custom policy.
- **Production deployment** of agents as services (on Vertex AI Agent Engine, Cloud Run, Kubernetes, or wherever).

For that, you drop down a level — from the CLI to the SDK.

Two SDKs matter: Google's **Agent Development Kit (ADK)** and Anthropic's **Claude Agent SDK**. This is where "NDK" in some folks' heads maps to — it's **ADK** from Google.

## Google ADK — the Google-first path

[google.github.io/adk-docs](https://google.github.io/adk-docs/)

ADK is Google's open-source Python framework for building multi-agent systems on Gemini models. It ships with:

- First-class primitives for agents, tools, workflows, and memory.
- Native integration with Google Cloud — Vertex AI, Cloud Run, Agent Engine.
- Multi-agent orchestration primitives (sequential, parallel, hierarchical).
- Session and memory management that scales past "one conversation."
- A built-in dev UI for visualizing agent runs.

### A minimal ADK agent

```python
# agent.py
from google.adk.agents import Agent

weather_agent = Agent(
    name="weather_agent",
    model="gemini-3-pro",
    instruction="You help users check weather. Use the get_weather tool.",
    tools=[get_weather],  # a Python function; ADK wraps it as a tool
)
```

Run it:

```bash
adk run agent.py
```

Deploy it:

```bash
adk deploy vertex agent.py  # to Vertex AI Agent Engine
```

The whole stack — tool definition, memory, deployment — is Python. If your team is already shipping Python, this is the path of least resistance.

### Multi-agent with ADK

```python
from google.adk.agents import Agent
from google.adk.agents.workflow import Sequential, Parallel

researcher = Agent(name="researcher", model="gemini-3-flash", tools=[search, fetch])
writer = Agent(name="writer", model="gemini-3-pro", tools=[])
reviewer = Agent(name="reviewer", model="gemini-3-pro", tools=[])

pipeline = Sequential(
    agents=[
        researcher,
        writer,
        reviewer,
    ],
    name="research_pipeline",
)
```

Three agents; researcher goes first, writer second, reviewer third; each sees the previous agent's output. The ADK [multi-agent docs](https://google.github.io/adk-docs/agents/multi-agents/) cover sequential, parallel, loop, and hierarchical patterns.

### Why pick ADK

- You're on Google Cloud; Vertex is your runtime.
- You want Gemini-first agents.
- Python is your team's language.
- You need real multi-agent systems, not just CLI subagent tricks.

## Claude Agent SDK — the Anthropic path

[docs.claude.com/en/api/agent-sdk/overview](https://docs.claude.com/en/api/agent-sdk/overview)

The Claude Agent SDK lets you build agents on Claude models with access to the same tool primitives Claude Code uses — file operations, shell, web, and custom MCP-backed tools.

TypeScript and Python supported. The two common use cases:

1. **Embedding Claude-powered agents in your product.** Customer support agent, code-review bot, internal tooling.
2. **Writing programmatic versions of Claude Code flows** — batch jobs, scheduled tasks, CI integrations.

### Minimal Claude Agent SDK example (TypeScript)

```ts
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const result = await client.agents.run({
  model: "claude-opus-4-7",
  system: "You are a release-notes assistant. Be concise and factual.",
  tools: [
    {
      type: "custom",
      name: "get_merged_prs",
      description: "Return a list of PRs merged since the given date.",
      input_schema: { /* ... */ },
      handler: async ({ since }) => {
        // Your code that calls GitHub, returns structured data
      },
    },
  ],
  input: "Write release notes for everything merged since 2026-04-01.",
});

console.log(result.final_message.content);
```

### Why pick Claude Agent SDK

- You want Claude's code quality specifically.
- You're integrating into a TypeScript / Node stack.
- You need the tool-use semantics Claude Code uses.
- You want MCP compatibility out of the box.

## The cross-SDK patterns

Regardless of which SDK you pick, these decisions recur:

### 1. Split the model routing

Don't run everything on the premium model. Use Flash / Haiku for tool-result summarization, cheap search, rote formatting. Reserve Pro / Opus for the reasoning step that justifies the cost.

### 2. Separate memory from session

Short-term conversation context is cheap to lose. Long-term memory — user preferences, past decisions, organization data — should live in a real store (Firestore, Postgres, a dedicated vector DB) and be injected into the agent's context at session start.

### 3. Design for idempotency

A production agent will be re-invoked. Tools that mutate state need to be safe on retry. Either make them idempotent by construction (e.g., "create issue X if not exists") or include a de-duplication key.

### 4. Telemetry from day one

Every agent run emits a trace: tool calls, latencies, token usage, outcome. Wire this up before you ship. Retrofitting observability is always painful.

### 5. Test with recorded transcripts

The most useful eval for an agent system is "replay real past conversations and assert the new version doesn't regress." Capture transcripts in staging; replay them in CI.

## When to pick each

Rough guide:

- **Google Cloud shop, Python team, Gemini models preferred, need multi-agent:** **ADK**.
- **Existing Node/TS product, Claude's code quality matters, MCP-heavy:** **Claude Agent SDK**.
- **You want both and have the capacity:** pick the one that matches the dominant language and deployment target; the concepts transfer.

## Antigravity, CLI subagents, SDKs — how they relate

It's worth stating plainly:

- **Antigravity:** a GUI IDE that happens to run agents. Good for interactive work; not where you build production agent systems.
- **CLI subagents (Ch. 11):** tactics for keeping one session clean; not a production primitive.
- **SDKs (this chapter):** the right abstraction for building durable, production agent systems.

Pick the layer that matches the purpose. People trying to build a production agent on top of a CLI end up fighting the tool. People trying to do daily coding through an SDK end up reinventing what the CLIs give you for free.

## References

- [Google ADK docs](https://google.github.io/adk-docs/)
- [ADK multi-agent](https://google.github.io/adk-docs/agents/multi-agents/)
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview)
- [Claude Agent SDK overview](https://docs.claude.com/en/api/agent-sdk/overview)
- [Anthropic SDK on GitHub](https://github.com/anthropics/anthropic-sdk-typescript)
