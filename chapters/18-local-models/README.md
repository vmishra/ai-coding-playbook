# Chapter 18 — Local Models for Coding

> When the model runs on your laptop, a server rack, or your own Vertex endpoint — not on a vendor's API. Who should care, why, and the setup that actually works.

---

## When this matters

Local / self-hosted models have three use cases where they beat a hosted API:

1. **Privacy / data residency.** Code that can't leave your machine, a cluster, or a specific cloud region.
2. **Cost at high volume.** Running 100 engineers against premium APIs all day is expensive. Running a shared Qwen3-Coder endpoint on a few A100s often isn't.
3. **Offline / latency-sensitive work.** Laptop on a train. Trading floor with microsecond sensitivities. Air-gapped environment.

If none of these apply to you, hosted APIs are the right answer. Local is engineering overhead you don't need.

## The model landscape (April 2026)

For coding specifically, three families lead:

### Qwen3-Coder (Alibaba)

The current community favorite. Native 256k context, extendable to 1M via YaRN. Strong agentic tool-use. Multiple sizes:

- **Qwen3-Coder-30B-A3B-Instruct** — MoE, ~3B active params. Fits in ~17 GB VRAM at Q4 — practical on a single 24 GB GPU or a high-end Mac.
- **Qwen3-Coder-480B-A35B-Instruct** — MoE, ~35B active. Server-class.
- **Qwen3-Coder-Next** — newer, ~80B / ~3B active, 262k context.

Source + how-to-run: [Unsloth's Qwen3-Coder guide](https://unsloth.ai/docs/models/tutorials/qwen3-coder-how-to-run-locally).

### DeepSeek-V3.2 / DeepSeek-Coder-V2

Released January 2026. 671B total / 37B active MoE, 164k context, with DeepSeek Sparse Attention (DSA) for long-context efficiency. Multi-GPU to run locally; great via [Vertex AI Model Garden](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/deepseek/deepseek-v32) if you don't want to self-host. DeepSeek-Coder-V2 (236B / 21B active) remains a widely-deployed dedicated coder SKU.

Source: [HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-V3.2).

### Google Gemma / CodeGemma

[CodeGemma](https://ai.google.dev/gemma/docs/codegemma) is Google's open coding variant (2B / 7B). [Gemma 4](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/) shipped April 2, 2026 under Apache 2.0 with an emphasis on high-quality offline coding. If you're in a Google shop and want to run open weights locally, this is the lowest-friction family — Google's tooling composes with it best.

## Runners

### Ollama — the easiest local runner

```bash
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull qwen3-coder:30b-a3b

# Run it
ollama run qwen3-coder:30b-a3b
```

Ollama exposes an OpenAI-compatible server at `http://localhost:11434/v1`. Anything that speaks OpenAI's Chat Completions API speaks Ollama.

### LM Studio — same space, GUI

Good for laptops, particularly Apple Silicon. Exposes the same OpenAI-compatible API.

### llama.cpp — closer to the metal

When you want precise control over quantization, offload layers, or run on unusual hardware.

### vLLM — production-grade serving

```bash
pip install vllm
vllm serve <model-id>   # OpenAI-compatible API on :8000
```

The right choice for team-shared endpoints. Strong throughput, batching, multi-GPU support. [Docs](https://docs.vllm.ai/en/stable/serving/openai_compatible_server/).

## Hooking local models up to your agent

All three of the current best coding-agent IDEs/CLIs speak the OpenAI Chat Completions API shape to local models:

### Continue.dev (VS Code + JetBrains + CLI)

The most flexible option for local. Configure any OpenAI-compatible endpoint in `~/.continue/config.json`:

```json
{
  "models": [{
    "title": "Local Qwen3-Coder",
    "provider": "ollama",
    "model": "qwen3-coder:30b-a3b",
    "apiBase": "http://localhost:11434/v1"
  }]
}
```

[Docs](https://docs.continue.dev/customize/model-providers/more/vllm).

### Cline

VS Code extension, Plan / Act modes. Select "OpenAI Compatible" and paste the base URL. [Provider config docs](https://docs.cline.bot/provider-config/openai-compatible).

### Aider

Git-aware terminal agent. Local-friendly from the start:

```bash
aider \
  --openai-api-base http://localhost:11434/v1 \
  --model openai/qwen3-coder:30b-a3b
```

## Using local models *with* Gemini CLI or Claude Code

Both primary CLIs are tightly bound to their respective first-party models. You generally cannot swap Gemini CLI for a local model directly — it's built for Gemini. Same for Claude Code.

If you need local-model agentic CLI work, the right shape is:

- **Continue.dev** for in-IDE agentic flows on local models.
- **Aider** for CLI-based, git-first local-model work.
- **Gemini CLI or Claude Code** for their respective first-party models when privacy/cost aren't forcing local.

## Vertex AI Model Garden — the hybrid path

If you're in a Google Cloud shop and "local" really means "private, but we don't want to operate the infra," Vertex AI Model Garden is the right middle ground.

Two modes:

1. **Model-as-a-Service (MaaS).** Fully managed, serverless endpoints for Qwen, DeepSeek, and many others. No GPU provisioning. [DeepSeek MaaS docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/deepseek) • [Qwen MaaS docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/qwen).

2. **Self-deployed endpoints.** Open a model card in the Model Garden console, click Deploy, pick region and machine type — Vertex provisions a dedicated inference endpoint in your project. [Overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/open-models/deploy-model-garden).

**When to pick which:** MaaS for variable traffic and fastest time-to-token; self-deployed endpoints when data residency, custom quantization, throughput-per-dollar tuning, or private-VPC requirements come into play.

## Practical cost math

Rough numbers, with caveats:

- **Hosted premium API (Opus, Gemini 3 Pro):** dollars per heavy session.
- **Local Qwen3-Coder-30B on a 24GB GPU:** electricity, maybe a few cents per session. But hardware + ops overhead.
- **Vertex MaaS Qwen / DeepSeek:** between the two. No ops, but pay-per-token.

The crossover point for local self-hosting is usually ~50+ engineers on daily use, assuming you have someone who can run a GPU host. Below that, hosted is better; above that, local starts dominating on cost — though rarely on code quality.

## A note on quality

Open models have closed most of the gap on many tasks. For the hardest multi-file refactors, cross-language work, and tricky reasoning, hosted frontier models still have an edge. Benchmarks move quarterly — if you care, run your own evals on your own code, not SWE-bench screenshots.

## References

- Qwen3-Coder: [Unsloth guide](https://unsloth.ai/docs/models/tutorials/qwen3-coder-how-to-run-locally)
- DeepSeek: [HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-V3.2), [Vertex MaaS](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/deepseek/deepseek-v32)
- Gemma 4: [blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/), [CodeGemma](https://ai.google.dev/gemma/docs/codegemma)
- Ollama: [ollama.com](https://ollama.com)
- vLLM: [docs.vllm.ai](https://docs.vllm.ai)
- Continue.dev: [docs.continue.dev](https://docs.continue.dev)
- Cline: [docs.cline.bot](https://docs.cline.bot)
- Aider: [aider.chat](https://aider.chat)
- Vertex Model Garden: [cloud.google.com/vertex-ai/generative-ai/docs/model-garden](https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden)
