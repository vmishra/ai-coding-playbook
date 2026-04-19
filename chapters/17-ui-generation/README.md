# Chapter 17 — UI Generation: Stitch, Claude Design, v0, Figma Dev Mode

> From "I need a screen for this" to working components. The current landscape, the Google-native path, and the handoff mechanics that turn generated UI into code you can ship.

---

## The concept

Two years ago, "generate a UI" meant a pretty screenshot. Today it means components you can drop into a real codebase — with design tokens, responsive behavior, and a hand-off path that includes more than "here's a PNG, good luck."

Three distinct things are happening in this space, and they blur together in marketing:

1. **Text-to-UI generation.** "Make me a dashboard that shows X, Y, Z." You get a design + code.
2. **Design-system-aware generation.** The above, but the output respects your existing components and tokens — not some generic Tailwind card.
3. **Design-to-code handoff.** A Figma (or equivalent) design exists; an MCP server turns it into accurate, structured code for your agent to incorporate.

Treat these as three tools for three problems. Picking wrong wastes time.

## The current landscape (April 2026)

### Stitch (Google Labs) — the Google-first text-to-UI tool

[stitch.withgoogle.com](https://stitch.withgoogle.com) — free during Labs preview, powered by Gemini.

**What it's best at:** exploratory UI generation from text, image, or URL. Infinite canvas for iterating. Strong when you need to go from "rough idea" to "working component skeleton" in minutes.

**Exports:**
- HTML/CSS
- Tailwind CSS
- React / JSX
- Paste-to-Figma for teams already in Figma
- **`DESIGN.md`** — a plain-text, agent-readable design spec describing components, tokens, spacing, and usage rules

The `DESIGN.md` export is the interesting one for this playbook. It's structured so that Gemini CLI, Claude Code, Cursor, or any other coding agent can read it and generate code that conforms to the design — bypassing the classic Figma-inspect-copy-paste-tweak loop.

**SDK:** [github.com/google-labs-code/stitch-sdk](https://github.com/google-labs-code/stitch-sdk) — `@google/stitch-sdk` on npm. Includes an MCP tool client so your CLI can query Stitch designs programmatically.

### Claude Design — Anthropic's new design product (launched April 17, 2026)

Anthropic shipped [Claude Design](https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/) as a research preview to all paid Claude subscribers (Pro, Max, Team, Enterprise) in April 2026.

**What it's best at:** prototypes, pitch decks, one-pagers, mockups. Generates from natural-language prompts; refines via chat, inline comments on specific elements, direct text edits, or Claude-generated sliders (spacing, color, layout).

**Design-system awareness:** it can read your team's codebase and design files and apply your design system to every project — the big differentiator vs most text-to-UI tools.

**Exports:** PDFs, shareable URLs, PPTX, and push-to-Canva (editable and collaborative).

**When to reach for it:** anything visual-but-not-production. Slide decks, prototypes, marketing mockups, teaching artifacts. For shipping production components, Stitch + a coding agent is usually tighter.

Sources: [VentureBeat](https://venturebeat.com/technology/anthropic-just-launched-claude-design-an-ai-tool-that-turns-prompts-into-prototypes-and-challenges-figma), [MacRumors](https://www.macrumors.com/2026/04/17/anthropic-claude-design/).

### v0 (Vercel) — production React components

[v0.app](https://v0.app). Best-in-class for generating React + shadcn/ui components that drop into a Next.js / React codebase cleanly. Not an exploratory tool like Stitch — it's "give me a form that does X, make it look like the rest of my app."

React-only. If your app isn't React, skip it.

### Figma Dev Mode MCP

For teams where Figma is already source of truth, Figma's first-party MCP server is the current canonical design-to-code handoff.

[Official docs](https://developers.figma.com/docs/figma-mcp-server/) • [Setup guide](https://help.figma.com/hc/en-us/articles/32132100833559).

**What it exposes:**
- `get_code` (alias: `get_design_context`) — returns React + Tailwind representation of a selected frame/component.
- `get_image` — screenshot.
- `get_variable_defs` — design tokens (colors, spacing, typography).
- Code Connect integration (map components in Figma to components in code).
- Canvas-writing tools to create/modify frames, components, variables, auto layout.

**Transports:**
- **Desktop:** `http://127.0.0.1:3845/mcp` (via Figma desktop app).
- **Remote:** `https://mcp.figma.com/mcp` (hosted, broader feature set, recommended).

**Plan requirements:** generally a Dev or Full seat on Professional / Organization / Enterprise plans. Verify current tier on Figma's docs.

## Configuring Figma Dev Mode MCP

### Claude Code

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
# Or the desktop variant:
claude mcp add --transport http figma http://127.0.0.1:3845/mcp
```

### Gemini CLI

`~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "figma": { "httpUrl": "https://mcp.figma.com/mcp" }
  }
}
```

Verify with `/mcp`.

## Recommended workflow (Google-first)

For anyone shipping product UI on a Google-adjacent stack, the shortest useful path is:

1. **Explore in Stitch.** Text-prompt or sketch-upload a first version. Iterate visually.
2. **Export `DESIGN.md`** when the design is converging.
3. **Open your agentic CLI** (Gemini CLI or Claude Code) in the target repo.
4. **Feed the design to the agent** as a file reference: `@DESIGN.md`, or "Use the design system defined in DESIGN.md" in a brief.
5. **Implement** using your existing components and conventions. The agent aligns new code with both the design spec and the repo's conventions.

For design-source-of-truth-in-Figma workflows:

1. **Design in Figma.** Use Code Connect to link components.
2. **Enable Figma Dev Mode MCP** (remote or desktop).
3. **In the CLI**, ask for implementation: "Use get_code on the currently selected frame. Generate a React component matching our `src/components/` conventions."
4. **Review the diff carefully** — the MCP output is usually close, rarely exact.

## Generated UI into a real codebase

Watch for these seams regardless of source tool:

- **Design tokens not wired up.** Generated components often inline hex values instead of using your `theme.ts`. Ask explicitly: "Use tokens from `src/tokens/`, not literal values."
- **Accessibility shortcuts.** Generated UI frequently omits ARIA attributes, keyboard handlers, and focus management. Brief for them: "Respect keyboard focus traps, provide alt text, label every interactive element."
- **Layout systems that don't match.** If your app uses a specific grid system (MUI, Chakra, a custom component), tell the agent to match it, not reach for vanilla flex/grid.
- **Component duplication.** Agents will happily reinvent `<Button>` that already exists. Brief: "Before creating any new component, grep `src/components/` for an existing one that fits."

## A concrete UI brief

Don't just say "make me a settings page." Give the agent this:

```
Build a settings page for workspace-level notification preferences.

Design source: @DESIGN.md (or: use get_code on frame "Settings / Notifications")

Constraints:
- Use components from src/components/ when they exist. Grep before creating.
- Tokens come from src/tokens/ (colors, spacing, type). Do not inline hex values.
- Tailwind is not in this project — use CSS Modules as elsewhere in src/.
- The form should follow the pattern in src/pages/settings/profile.tsx —
  react-hook-form + zod schema in src/schemas/.
- A11y: every toggle needs a <label>, the form must trap focus when open,
  submit on Enter, cancel on Esc.

Output:
- src/pages/settings/notifications.tsx
- src/schemas/notifications.ts
- Route registration in src/routes.tsx

Verification:
- pnpm typecheck passes.
- pnpm test -- notifications passes (write tests).
- Page renders with no console errors.
```

The difference between a good UI brief and a mediocre one is identical to the difference between a good code brief and a bad one. Scope, constraints, verification — Ch. 3.

## Anti-patterns

- **Generating from vibes without a design anchor.** You get "AI-looking" UI — beveled shadows, purple gradients, glass morphism — that matches nothing on your product. Always anchor to `DESIGN.md`, a Figma source, or your existing components.
- **Piping straight to production.** Generated UI is a starting point. Run it past a real designer and a real a11y review before shipping user-facing.
- **Locking into one tool.** Stitch is great today; Claude Design is new and promising; Figma Dev Mode MCP is the mature enterprise path. You'll likely use two of these, not one.

## References

- [Stitch by Google Labs](https://stitch.withgoogle.com)
- [Stitch SDK on GitHub](https://github.com/google-labs-code/stitch-sdk)
- [Stitch product blog](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/)
- [Claude Design launch](https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/)
- [v0.app](https://v0.app)
- [Figma Dev Mode MCP docs](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP tools and prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
