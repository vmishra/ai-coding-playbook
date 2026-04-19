# Contributing

Thanks for considering a contribution. This project aims to be the most useful, least wasteful reference on AI-assisted coding. Contributions that move it toward that goal are very welcome.

## The bar

Before opening a PR, ask yourself:

1. **Does this help a real developer do real work?** "I added a section on X" is not a contribution. "I added a section on X because I hit problem Y and couldn't find guidance anywhere" is.
2. **If you're contributing an asset (skill, command, hook, MCP config), does it run?** Not "it looked right in the editor" — does it actually execute end-to-end on a fresh install?
3. **Is the prose written by a human?** We are not the right place for AI-generated filler. Polish with an AI if you like, but the voice and judgment have to be yours.

## What we want

- **Fixes**: broken commands, outdated tool behavior, version drift, typos, dead links.
- **New assets**: skills, slash commands, hook scripts, MCP configs — things people can copy and use. Each asset ships with its own README explaining what it does, when to use it, and what it costs.
- **Field reports**: "I tried approach A on a 2M-LOC monorepo and it fell over at step 3" is gold. These become case studies.
- **New chapters**: propose in an issue first. The TOC is intentionally finite.

## What we don't want

- PRs that rephrase existing content to sound more impressive.
- Assets that only work in your specific environment without saying so.
- Chapter reshuffles without a clear reader-benefit argument.
- Anything that reads like a vendor pitch.

## PR checklist

- [ ] One logical change per PR. Split if needed.
- [ ] Commit messages describe the *why*, not just the *what*.
- [ ] If you added an asset, you tested it on a fresh install.
- [ ] If you changed a chapter, you updated the TOC if structure moved.
- [ ] If you linked to a tool, you linked to the *official* docs, not a blog post.
- [ ] No AI-generated filler. If in doubt, cut.

## Style

- **Second person** ("you do this"), present tense. We're talking to a person, not documenting an API.
- **Specific over general**. "Use `--max-turns 8`" beats "tune the turn limit."
- **Short paragraphs**. If a paragraph has more than 5 sentences, split it.
- **Code blocks are for code**, not for quoting tool names or paths. Use backticks inline.

## Reporting issues

File an issue. Include:

- Tool + version (`claude --version`, `gemini --version`)
- What you expected, what happened
- A minimal repro if possible

That's it. Thanks for helping.
