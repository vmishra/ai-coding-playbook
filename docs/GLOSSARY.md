# Glossary

Terms used throughout the playbook, defined once so the chapters can stay lean. Listed roughly in order of how often you'll encounter them.

## Agent
A program that uses an LLM in a loop: it reads, decides, calls tools, observes results, and decides again. An *agentic coding tool* is an agent whose available tools include filesystem edits, shell commands, and (usually) network calls.

## Context window
The total number of tokens the model can see at once — the system prompt, your messages, tool results, and the model's own outputs combined. Every byte you put in costs money and crowds out something else. Managing the context window is most of what "working effectively with an agent" actually is.

## Token
A rough unit of text the model processes. For English, one token ≈ 4 characters ≈ 0.75 words. Code tends to tokenize less efficiently (more tokens per character) than prose.

## Prompt caching
A vendor-side mechanism where the first N bytes of your prompt are cached and reused across calls, at a fraction of the cost and latency. Both Google and Anthropic support it. The cost discipline this imposes — keep the stable stuff at the top, the volatile stuff at the bottom — is the real lesson, and it generalizes to any future mechanism.

## Compaction
The process of replacing a long conversation history with a shorter summary, freeing context. Every agentic tool either does this automatically, on command, or both. Knowing when to trigger it manually is a skill.

## Hook
A user-defined shell command the tool runs on an event — before a tool call, after a tool call, on submit, on exit. Hooks are how you enforce policy ("don't let the agent run `rm -rf`") and how you automate local workflow ("run the formatter after every edit").

## MCP (Model Context Protocol)
An open protocol for exposing tools and data to an LLM agent. A *server* exposes tools; a *client* (your CLI) consumes them. Introduced by Anthropic, adopted broadly including by Google's Gemini CLI and Agent Development Kit. The point is interoperability: one protocol, many agents.

## Slash command
A named, reusable prompt (or short script) invoked with `/name`. Lives in `~/.claude/commands/` or `~/.gemini/commands/`. Not the same as a skill.

## Skill (Claude Code)
A self-contained capability — a folder with a `SKILL.md` plus supporting files — that the agent can discover and use when relevant. Includes instructions, optional code, and metadata. More structured than a slash command, more lightweight than a subagent.

## Subagent
A second instance of the agent spawned by the primary agent, typically with a narrower context and a specific task. Used to parallelize work and to keep large exploratory reads out of the primary context.

## Extension (Gemini CLI)
The Gemini CLI analogue to skills — a directory with `gemini-extension.json` declaring MCP servers, context files, and custom commands.

## Context rot
The degradation of agent quality as a session grows long. Earlier context gets crowded by later results; irrelevant detail pollutes the window; decisions start drifting. Every long session hits this. Chapter 9 is about avoiding it.

## Tool use
The mechanism by which the LLM invokes a capability (read a file, run a command, search the web). The model emits a structured tool call; the runtime executes it; the result comes back as a tool result message.

## Vertex AI Model Garden
Google Cloud's catalog of foundation models — Gemini, Gemma, plus third-party options like Llama and Claude (via partnerships). The typical path for running models in a Google production footprint.

## ADK (Agent Development Kit)
Google's open-source Python framework for building multi-agent systems. Deploys to Vertex AI Agent Engine or Cloud Run. Covered in Ch. 20.

## Claude Agent SDK
Anthropic's SDK for building custom agents on top of the Claude API with Claude Code's tool-use primitives. Covered in Ch. 20.

## Firebase Studio
Google's browser-based, AI-assisted full-stack dev environment. Successor / relative of Project IDX. Covered in Ch. 14.

## Cloud Workstations
Google Cloud's managed, VM-backed remote dev environments. Production-grade alternative to local dev. Covered in Ch. 14.

## Antigravity
Google's agentic IDE, positioned as a higher-abstraction complement to Gemini CLI. Chapter 19.

## Stitch
Google Labs' text-to-UI tool at [stitch.withgoogle.com](https://stitch.withgoogle.com). Exports HTML/CSS, Tailwind, React, and a `DESIGN.md` format meant for agents. Chapter 17.
