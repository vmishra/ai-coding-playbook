# <Project Name>

Replace this one paragraph: what the repo is, who uses it, what it talks to.
Anchor it in nouns that show up elsewhere in the codebase so the agent can orient fast.

## Run / test / build

- Install: `<cmd>`
- Dev: `<cmd>`
- Test (all): `<cmd>`
- Test (subset): `<cmd> -- <path-or-filter>`
- Typecheck: `<cmd>`
- Lint: `<cmd>`
- Format: `<cmd>`
- Deploy: **ask before deploying**

## Architecture in three sentences

Requests enter at `<entry-file>`, are authenticated by `<auth-file>`, and routed through `<router-file>`.
State lives in `<datastore>`. External dependencies we own: `<list>`. External dependencies we don't: `<list>`.

## Conventions

- Indent: <tabs / N spaces>
- Language style: <ref to prettier/eslint/gofmt config>
- Naming: TS types `PascalCase`, TS fields `camelCase`, DB columns `snake_case`.
- Error handling: <Result type / thrown exceptions / return codes>
- Logging: `<package>`, structured JSON, always include `request_id`.
- Never: add deps without asking, use `any`, commit secrets, skip tests, disable the linter.

## Where to look

- Auth: `./auth/README.md`
- Data model: `./db/README.md`
- API contracts: `./api/openapi.yaml`
- CI pipeline: `./.github/workflows/`

## Known traps

- `<file-or-subsystem>` has a subtle invariant about `<thing>`. Read the comments before changing.
- `<legacy-subsystem>` is scheduled for deprecation in <quarter>. Minimize changes; don't add features here.
- Anything under `db/migrations/` is applied in order and never edited after merge.

## Subsystems

@./billing/GEMINI.md
@./auth/GEMINI.md
@./api/GEMINI.md
