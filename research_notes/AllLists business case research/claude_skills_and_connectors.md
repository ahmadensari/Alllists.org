# Claude Code skills, plugins, MCP servers and connectors for AllLists.org

Research date: 2026-10-04. Nothing was installed. Verification limits in this session: the `gh` CLI and GitHub API were blocked for these repos ("GitHub access ... not enabled"), commit-feed (.atom) fetches returned nothing, and support.stripe.com and developers.google.com were blocked by the egress proxy. Therefore exact "last commit" dates could NOT be verified directly for most repos. Where a date appears below it is the official MCP registry `updatedAt` field (queried directly from registry.modelcontextprotocol.io), which proves a recent publish but is not the same as a last-commit date. Licences come from repo README pages as summarised by WebFetch, not from the LICENSE file itself unless stated.

## 1. Official Anthropic skills and plugins (frontend, web apps, testing, review, security, documents, spreadsheets, PDF)

### Takeaway
Anthropic's `anthropics/skills` repo and the `anthropics/claude-plugins-official` marketplace already cover almost every non-infrastructure need (frontend design, web app testing, code review, security review, xlsx/pdf/docx). These are first-party, so they are the lowest-risk first installs. The document skills (docx/pdf/pptx/xlsx) are source-available, not open source.

### Cited Findings
- `anthropics/skills` has about 179.6k stars and 57 commits on main; most skills are Apache-2.0, but the docx, pdf, pptx and xlsx skills are "source-available, NOT open source" — [GitHub anthropics/skills](https://github.com/anthropics/skills)
- The `/skills` folder contains: academy-guide, algorithmic-art, brand-guidelines, canvas-design, claude-api, discernment-nudge, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx — [skills folder listing](https://github.com/anthropics/skills/tree/main/skills)
- `anthropics/claude-plugins-official` is "an official Anthropic-managed directory" (Apache-2.0, ~37.4k stars, 4,351 commits). `/plugins` holds Anthropic-built plugins; `/external_plugins` holds partner/community ones. Install: `/plugin install {plugin-name}@claude-plugins-official` or `/plugin > Discover` — [GitHub claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- The same README warns: users must trust a plugin before installing; "Anthropic does not control what MCP servers, files, or software are included in plugins" — [GitHub claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- Anthropic-built plugins listed in `/plugins` include: claude-code-setup, claude-md-management, claude-security, code-modernization, code-review, code-simplifier, commit-commands, feature-dev, frontend-design, hookify, mcp-server-dev, plugin-dev, pr-review-toolkit, security-guidance, pyright-lsp, skill-creator, session-report, ralph-loop, plus many other-language LSP plugins — [plugins folder listing](https://github.com/anthropics/claude-plugins-official/tree/main/plugins)
- This session's plugin catalog lists `code-review` (author Anthropic, publisher tier "anthropic", upstream `anthropics/claude-plugins-official` path `plugins/code-review`): "Automated code review for pull requests using multiple specialized agents with confidence-based scoring". Its `reach` is flagged "privileged" — SearchPlugins result in this session (Anthropic Directory marketplace)
- Stripe also publishes a Claude plugin: `claude plugin install stripe@claude-plugins-official` — [github.com/stripe/ai](https://github.com/stripe/ai)
- Third-party plugins that appeared in this session's SearchPlugins (Anthropic Directory, tier "community" unless noted): "finecomb" exhaustive code review/security checklist (author lian-yue, Markdown only, reach "contained"); "claude-code-review-council" six-specialist reviewer (author Vandal337, reach "privileged", has a PreToolUse hook); "code-review-harness" (naokami3, community); "42crunch-api-security-testing" (tier "partner", publisher 42crunch-ai, upstream github.com/42crunch-ai/claude-plugins); Pi Security, Sola Security, Above Security (community, remote hosted MCP servers — account/telemetry-oriented, not relevant to AllLists) — SearchPlugins result in this session
- In this session SearchSkills for "frontend design / testing / security review / web app" returned zero results (claude.ai account skills), and the account already exposes bundled skills including pdf, xlsx, docx, mcp-builder, skill-creator, web-artifacts-builder, and built-in `security-review`, `code-review`, `simplify` — session skill list

### Inferences
- Per-skill mapping for AllLists: `frontend-design` (server-rendered page polish, avoids generic look), `webapp-testing` (Playwright-driven checks of the running app), `xlsx` (review/clean owner-supplied listing spreadsheets before import), `pdf` (read PDF source documents/forms), `code-review` + `security-guidance` + `claude-security` + `pr-review-toolkit` (review pipeline), `commit-commands` (simple commit/PR flow for a non-technical owner), `claude-md-management` and `claude-code-setup` (keeping project memory and setup tidy), `hookify` (turn "never do X" rules into hooks).
- Licensing caution: if AllLists code or docs are published/redistributed, do not copy the docx/pdf/pptx/xlsx skill contents; using them locally is the intended use.
- Names of plugins `claude-security`, `code-modernization`, `receipts`, `cwc-makers`, `mcp-tunnels`, `project-artifact` are listed but their function was not verified; do not recommend until read.
- The owner is non-technical, so plugins that add slash commands with plain-language names (`commit-commands`, `code-review`) are better than ones needing config.

### Gaps
- The exact contents, permissions and SKILL.md of `frontend-design`, `webapp-testing`, `security-guidance`, `claude-security` were not opened; only directory names were confirmed.
- Last-commit dates for both Anthropic repos not verified (page did not show a date; API blocked).
- Whether `anthropics/skills` skills can be installed as a plugin marketplace (`/plugin marketplace add anthropics/skills`) was not confirmed from docs in this research.

## 2. MCP servers by area (GitHub, Postgres, Google Cloud, Cloudflare, Playwright, Stripe, WhatsApp, Maps, Sentry, filesystem, docs, search/fetch, project tracking)

### Takeaway
Vendor-maintained options exist for GitHub, Google Cloud (Cloud Run, gcloud, Cloud SQL via MCP Toolbox), Cloudflare, Playwright, Sentry, Stripe, Context7, Linear and Notion. PostgreSQL has no current first-party reference server (Anthropic's was archived); use Google's MCP Toolbox or Crystal DBA's Postgres MCP Pro in restricted mode. WhatsApp has no official Meta MCP server (community only). Official Google Maps MCP and Stripe-in-Pakistan eligibility could not be verified from primary sources.

### Cited Findings
**GitHub**
- GitHub MCP Server — publisher GitHub, MIT. Remote hosted `https://api.githubcopilot.com/mcp/` with OAuth (recommended) or Docker `ghcr.io/github/github-mcp-server`; PAT via `GITHUB_PERSONAL_ACCESS_TOKEN` (scopes typically `repo`, `read:org`, `security_events`); `--read-only` flag disables writes; default toolsets context, repos, issues, pull_requests, users; optional actions, code_security, dependabot etc. — [github/github-mcp-server](https://github.com/github/github-mcp-server)
- Claude Code example: `claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"` — [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)
- This session already exposes `mcp__github__*` tools (issues, PRs, actions, secret scanning, merge, delete_file), i.e. a GitHub connector is already available here. The older Anthropic-hosted `github` server was moved to the archived repo — [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**PostgreSQL / Cloud SQL**
- Anthropic's reference repo now lists only Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time as active; GitHub, Google Maps, PostgreSQL, Puppeteer, Redis, Sentry, Slack, SQLite etc. were moved to `servers-archived`; servers are "educational examples" not production-ready; licence Apache-2.0 for new contributions, MIT for existing code — [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- MCP Toolbox for Databases — publisher googleapis (Google), Apache-2.0, v1.13.1 shown; supports PostgreSQL, Cloud SQL, AlloyDB, BigQuery and many others; Claude Code config `npx -y @toolbox-sdk/server --prebuilt=postgres --stdio` with DB env vars; supports IAM auth and restricted "structured queries" — [googleapis/genai-toolbox](https://github.com/googleapis/genai-toolbox)
- Postgres MCP Pro — Crystal DBA, MIT, ~3.4k stars; "Unrestricted" vs "Restricted" mode (restricted = read-only transactions plus resource limits); explain plans, hypothetical-index tuning, health checks; install via Docker/pipx/uv — [crystaldba/postgres-mcp](https://github.com/crystaldba/postgres-mcp)
- Claude Code docs show a read-only Postgres pattern with Bytebase DBHub and a read-only DB user — [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)
- Official MCP registry search for "postgres" returned only a vendor-specific `com.devart/mcp-postgresql` (updated 2026-09-23) and generator tools in its first page — [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=postgres&limit=5)
- Neon (hosted Postgres) has a connector in this session's registry search — not relevant unless AllLists moves to Neon — SearchMcpRegistry result in this session

**Google Cloud**
- Cloud Run MCP — publisher GoogleCloudPlatform, Apache-2.0, 289 commits; tools: deploy-file-contents, list-services, get-service, get-service-log, deploy-local-folder, list-projects, create-project (last three local only); auth via `gcloud auth application-default login`; install `npx -y @google-cloud/cloud-run-mcp`; README says it is not archived or deprecated and a remote option exists; "Google Cloud Platform Terms of Service do not apply to this software component" — [GoogleCloudPlatform/cloud-run-mcp](https://github.com/GoogleCloudPlatform/cloud-run-mcp)
- gcloud MCP — publisher googleapis, Apache-2.0; four servers (gcloud, observability, storage, backupdr); explicitly "in preview ... may see breaking changes" and "not an officially supported Google product"; acts with the active gcloud account's permissions, blocks some commands, and recommends service-account impersonation for least privilege — [googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp)
- Compute Engine specific MCP server: not found in this research (see Gaps). The gcloud MCP could cover it via CLI.
- Google Cloud BigQuery connector exists in this session's registry (not needed for AllLists unless analytics move to BigQuery) — SearchMcpRegistry result

**Cloudflare / DNS**
- Cloudflare MCP repo — publisher Cloudflare, Apache-2.0; 13 domain servers plus recommended "Code Mode" server `https://mcp.cloudflare.com/mcp`; docs server `https://docs.mcp.cloudflare.com/mcp`; DNS Analytics server `https://dns-analytics.mcp.cloudflare.com/mcp`; auth via scoped API tokens or OAuth; the README page did not mention DNS record editing for the individual servers — [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare)
- Official registry lists `com.cloudflare.mcp/mcp` (docs server, updated 2025-09-16) — [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=cloudflare&limit=30)
- A "Cloudflare Developer Platform" connector (tools include kv, workers) is in this session's Anthropic directory, not installed — SearchMcpRegistry result

**Playwright**
- Playwright MCP — publisher Microsoft, Apache-2.0; `claude mcp add playwright npx @playwright/mcp@latest`; docs state it "is **not** a security boundary"; `--allowed-origins` is not a security boundary either; `--headless` supported; registry shows `io.github.microsoft/playwright-mcp` v0.0.75 updated 2026-05-07 — [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp); [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=playwright&limit=30)

**Stripe**
- Stripe MCP — publisher Stripe, repo `stripe/ai` MIT; remote `https://mcp.stripe.com`; recommends restricted API keys; Claude plugin `stripe@claude-plugins-official`; registry entry `com.stripe/mcp` v0.2.4 updated 2025-10-28 — [stripe/ai](https://github.com/stripe/ai); [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=stripe&limit=30)
- A Stripe connector (tools include stripe_api_write, get_balance_summary) is in this session's directory, not installed — SearchMcpRegistry result
- Pakistan: search snippets conflict. One source says Stripe covers Pakistan (PKR, 2.9% + 30c); other sources say Pakistan is not among Stripe's ~46 directly supported countries and that Stripe Atlas (US company incorporation) is the workaround — [learnwithhasan.com](https://learnwithhasan.com/payment-gateways/country/pakistan/); [Medium payometrix](https://medium.com/@payometrix/how-to-open-a-stripe-account-in-pakistan-without-ssn-a87e783b591c); [Stripe feature availability by country (URL from search; page blocked here)](https://support.stripe.com/questions/stripe-feature-availability-by-country). None of these were verified against Stripe's own page.

**WhatsApp Business**
- Meta ships no official WhatsApp MCP server; all are community-built. Many rely on unofficial browser automation or reverse-engineered protocols that violate WhatsApp ToS and risk account bans. Two community servers use the official Meta Cloud API (`whatsapp-mcp-server`, `mcp-server-whatsapp`); free-form messages only work inside the 24-hour customer-service window, templates are needed to start conversations — [dragapp.com blog](https://www.dragapp.com/blog/whatsapp-mcp-server/); [mcpservers.org entry](https://mcpservers.org/servers/codechap/mcp-server-whatsapp)
- Official registry search for "whatsapp" returned nothing in my filtered view (my filter only displayed vendor-prefixed names, so this is weak evidence) — [registry API](https://registry.modelcontextprotocol.io/v0/servers)

**Maps / Places / geocoding**
- Anthropic's Google Maps reference server is archived — [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- Registry results for "google-maps" were third-party scrapers/wrappers (HasData, GMapsExtractor, mcparmory, nexgendata proxy), not Google — [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=google-maps&limit=30). Google's own Maps MCP page (developers.google.com/maps/ai/mcp) was blocked and not read.

**Sentry**
- Sentry MCP — publisher Sentry (getsentry), remote `https://mcp.sentry.dev/mcp`, OAuth scopes org:read, project:read/write, team:read/write, event:write; install via `claude plugin marketplace add getsentry/sentry-mcp` then `claude plugin install sentry-mcp@sentry-mcp`, or `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp`; natural-language search tools need your own LLM provider key; registry v0.42.0 updated 2026-09-25 (actively maintained). Licence: README page pointed to LICENSE.md, not read — [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp); [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=sentry&limit=30)

**Filesystem, Git, Fetch, Memory (reference servers)**
- Active reference servers: Filesystem (configurable access restrictions), Git, Fetch, Memory, Sequential Thinking, Time — [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**Up-to-date library docs**
- Context7 — publisher Upstash, MIT; works with Claude Code (`npx ctx7 setup --claude`); free API key gives higher rate limits; queries send library lookups through Upstash's servers; README says "Context7 projects are community-contributed", and the API backend, parsing and crawling engines are private (only MCP server source is public). Registry v4.1.1 updated 2026-09-14, remote `https://mcp.context7.com/mcp` — [upstash/context7](https://github.com/upstash/context7); [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=context7&limit=30)

**Web search / fetch**
- Fetch reference server (Anthropic, active) — [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers). Claude Code already has built-in WebFetch/WebSearch tools in this session, so a separate server is not needed. Brave Search reference server is archived — same source. Vendor search servers (Brave, Tavily) were not researched.

**Project tracking (Linear / Notion / Slack)**
- Linear: official registry entry `app.linear/linear` v1.0.1 at `https://mcp.linear.app/mcp`, updated 2026-08-04 — [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=linear&limit=30)
- Notion: official registry entry `com.notion/mcp` at `https://mcp.notion.com/mcp` (2025-09-11); Claude Code docs use it as the example remote server — [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=notion&limit=30); [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)
- Slack: reference server archived; registry results were community (pulsemcp, smithery, mcparmory) — [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=slack&limit=30). No Slack vendor server was verified.
- Connectors already on the owner's claude.ai account (this session ListConnectors): Google Calendar (not connected), Indeed (connected), MindMap AI (connected), quran.ai, RankedIn (connected), Steep, Terac, Zapier (not connected). None are build/deploy tools.

**Claude Code install mechanics**
- `claude mcp add [options] <name> <url-or-command>`; scopes local (default, `~/.claude.json`), project (`.mcp.json`, shared in git), user; OAuth via `/mcp`; `--env` for secrets; `claude mcp list/get/remove` — [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)

### Inferences
- Pakistan: Stripe may not be usable for a Pakistan-resident business without a foreign entity (Atlas) or a different processor; do not install the Stripe MCP until the payment provider decision is made. Verify on Stripe's own country page when reachable.
- The best Postgres inspection setup is a read-only DB role plus Postgres MCP Pro (restricted) or MCP Toolbox, pointed at a development or replica copy first, never at production with write rights.
- For Cloud Run deploys, `gcloud` CLI (already installed in this environment) plus a human-approved deploy command may be safer and simpler for a non-technical owner than giving an agent deploy rights through an MCP server.
- "Compute Engine" and "Cloud SQL" operations can be handled by the gcloud MCP or the plain `gcloud` CLI under a limited service account.
- WhatsApp: send-only integration via the official Cloud API should live in the application code, not in an agent-facing MCP, until a clear need appears.

### Gaps
- Direct verification of last-commit dates and LICENSE files for every repo above (tooling blocked).
- A dedicated Compute Engine MCP server and a first-party Cloud SQL MCP server (beyond MCP Toolbox's Cloud SQL support) were not searched.
- Google Maps Platform official MCP/"Code Assist" server: page blocked; unverified.
- Whether Stripe supports Pakistan-based businesses directly: unresolved (conflicting secondary sources; Stripe page blocked).
- WhatsApp community server maintenance status, licences and stars were not checked.
- Vendor Slack, Brave and Tavily servers not verified.

## 3. Registries and what this session exposes

### Takeaway
The official MCP registry is live and queryable by API but is open to anyone, so most hits are unverified third-party entries; only vendor-namespaced entries (io.github.<vendor>, com.stripe, app.linear, com.notion, com.cloudflare.mcp) should be trusted as the vendor's own. The session's directory tools (SearchMcpRegistry, SearchPlugins, ListConnectors, SearchSkills) work and returned the results noted here.

### Cited Findings
- The official registry API (`https://registry.modelcontextprotocol.io/v0/servers?search=<term>&limit=N`) returns entries with `name`, `version`, `status`, `updatedAt`, repository URL and remotes — queried directly in this session — [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/v0/servers?search=postgres&limit=5)
- Searching "github" in the registry returned mostly third-party entries (smithery, mcparmory, a2awire, getstarhunt) and no entry that I could confirm as GitHub's own in the first 30 results, so the registry search does not surface the official GitHub server reliably — [registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=github&limit=30)
- SearchMcpRegistry in this session returned installable Anthropic-directory connectors (not installed): Stripe, Sentry, Cloudflare Developer Platform, Google Cloud BigQuery, Render, Neon, Google Docs, Google Slides, plus unrelated Pushwoosh and Ketryx — SearchMcpRegistry (first query batch)
- Claude Code docs point users to "reviewed connectors in the Anthropic Directory" (claude.ai/directory) and warn about prompt injection from servers that fetch external content — [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)
- punkpeye/awesome-mcp-servers, wong2/awesome-mcp-servers, awesome-claude-code and awesome-claude-skills were NOT opened in this research.

### Inferences
- Prefer the claude.ai Anthropic Directory (reviewed) or the vendor's own docs/repo over registry free-text search results.
- Registry presence is not a safety signal: anyone can publish under a `com.<domain>` or `ai.smithery/` name; verify the namespace matches the vendor's real domain/GitHub org.

### Gaps
- Community awesome-lists were not reviewed (time/tool budget); recommend a follow-up pass if needed, with each pick vetted as in section 2.
- Connectors for Google Cloud Run, Playwright, Context7, Linear, Notion, Slack were not individually checked in SearchMcpRegistry (second batch call with Cloudflare etc. returned only the first 10 ranked results).

## 4. Security: supply chain, prompt injection, secrets, least privilege

### Takeaway
Third-party MCP servers run with your credentials and read untrusted content, so the main risks are prompt injection through data (listings, reviews, web pages, DB rows), classic injection bugs in the server (SQL/command injection), and supply-chain issues from unmaintained forks. Use vendor-maintained servers, read-only credentials, project-scoped config and human approval for writes.

### Cited Findings
- Claude Code warns: "Verify you trust each server before connecting. Servers that fetch external content expose you to prompt injection risk"; in non-interactive mode (`claude -p`/SDK) project `.mcp.json` servers load without prompting — [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)
- Anthropic's own SQLite MCP server had an SQL injection flaw that could be turned into stored-prompt injection (e.g. hijacking a support bot to exfiltrate customer data); it was forked over 5,000 times before being archived, so unpatched copies persist downstream — [The Register](https://www.theregister.com/2025/06/25/anthropic_sql_injection_flaw_unfixed/); [Trend Micro](https://www.trendmicro.com/en/research/25/f/why-a-classic-mcp-server-vulnerability-can-undermine-your-entire-ai-agent.html) (details from search-result summaries; articles not fully read)
- A search result cites CVE-2026-87911, an OS command injection in the AWS Labs postgres MCP server (crafted `COPY ... TO PROGRAM`); I have only the search summary, not the advisory — [SentinelOne vulnerability database entry](https://www.sentinelone.com/vulnerability-database/cve-2026-87911/) (unverified detail)
- Anthropic's reference servers are "educational examples", not production-ready; the Playwright MCP docs say it is "not a security boundary"; the gcloud MCP is preview and unsupported; Cloud Run MCP README says Google Cloud ToS do not apply to it — sources in section 2
- Anthropic does not vet third-party plugin contents: "Users must trust a plugin before installation" — [claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- Plugins can contain hooks (PreToolUse/SessionStart/PostToolUse run code); this session's directory marks some plugins `reach: "privileged"` (e.g. Anthropic's own code-review, community review-council) and others "contained" (Markdown-only) or "remote" — SearchPlugins result
- GitHub MCP guidance: store PATs in env vars not config files, rotate, minimum permissions, use `--read-only` — [github/github-mcp-server](https://github.com/github/github-mcp-server)
- Stripe recommends restricted API keys; Cloudflare supports permission-scoped API tokens; gcloud MCP recommends service-account impersonation — sources in section 2

### Inferences
Least-privilege rules for AllLists:
1. Install only what is needed; start with first-party/vendor servers; pin versions (`@x.y.z`, not `@latest`) for stdio servers once chosen, since `npx -y` pulls code at every start.
2. Database: separate read-only Postgres role, dev/staging copy first; never give an agent the production superuser. Treat all DB text (listing descriptions, user submissions, imported spreadsheets) as untrusted instructions-bearing data (prompt injection through marketplace content is a realistic vector for a listings site).
3. GitHub: fine-grained PAT or OAuth limited to the AllLists repo; read-only mode for review tasks; no merge/delete rights for agents; branch protection on main.
4. Google Cloud: dedicated service account via impersonation with narrow roles (e.g. Cloud Run developer, Cloud SQL client, log viewer); no Owner/Editor; separate project for staging; production deploys require the owner's approval.
5. Cloudflare: API token scoped to DNS edit on one zone only (and only when needed); read-only/analytics otherwise.
6. Secrets: keep in env vars or Google Secret Manager, never in `.mcp.json` committed to git (use `${VAR}` expansion); add `.env` to `.gitignore`; use GitHub secret scanning.
7. Use `claude mcp add --scope project` only for servers the owner has reviewed, and review `.mcp.json`/`.claude/` changes in every PR since they can introduce new tools.
8. Avoid combining private-data access, untrusted content ingestion and an outbound channel (e.g. DB + web fetch + email/Slack/WhatsApp) in one session.
9. Vendor/first-party in this list: GitHub, Google (Toolbox, Cloud Run, gcloud - preview), Cloudflare, Microsoft Playwright, Sentry, Stripe, Upstash (Context7, MIT but closed backend), Linear, Notion, Anthropic. Community: Postgres MCP Pro (Crystal DBA), WhatsApp servers, any awesome-list or smithery/mcparmory-hosted proxies.

### Gaps
- Primary advisories for the SQLite and AWS postgres issues were not fetched; treat as indicative.
- No scan of third-party skills' contents for malicious instructions was performed.
- Not checked: npm provenance/signing of the packages named.

## 5. Agent patterns: subagents in .claude/agents

### Takeaway
Subagents are Markdown files with YAML frontmatter in `.claude/agents/` (project, shareable via git) or `~/.claude/agents/` (personal). For AllLists, define small, read-only reviewers with restricted tools.

### Cited Findings
- Format: frontmatter with required `name` and `description`, optional `tools` (inherits all if omitted), `disallowedTools`, `model` (sonnet/opus/haiku or full ID), `permissionMode`, `maxTurns`, `skills`, `memory` (user/project/local), `isolation: worktree`, `mcpServers`, `hooks`, `color`; the body is the system prompt; changes are detected within seconds, but creating a brand-new `agents` directory needs a restart — [Claude Code subagents docs](https://code.claude.com/docs/en/sub-agents)
- Project agents in `.claude/agents/` are intended to be checked into version control for team sharing — [Claude Code subagents docs](https://code.claude.com/docs/en/sub-agents)
- Anthropic's `code-review` plugin is already a multi-agent reviewer with confidence scoring — [SearchPlugins in-session](https://github.com/anthropics/claude-plugins-official/tree/main/plugins)

### Inferences
Suggested project subagents (all read-only: `tools: Read, Grep, Glob`, add `Bash` only where noted; `model: sonnet`, use opus for security):
- `code-reviewer`: Python/server-rendered correctness, readability, tests present; run after each feature.
- `security-reviewer`: OWASP checks for the marketplace: SQL injection (parameterised queries only), XSS in server-rendered templates (autoescape), CSRF, auth/session, file upload limits, rate limiting, secrets in code, admin routes, listing-contact spam; `tools: Read, Grep, Glob, Bash` for `pip-audit`/`bandit` only.
- `db-migration-reviewer`: reviews Alembic/SQL migrations for locking, destructive ops, missing indexes, reversibility, data backfills, and PostgreSQL version quirks; must be given the schema plus migration diff; never run against production.
- `data-quality-auditor`: inspects imported listing data (duplicates, missing city/category, phone and WhatsApp number formats incl. +92, geocode sanity, junk text); pairs with the xlsx skill for spreadsheet inputs.
- `urdu-english-copy-checker`: checks bilingual UI strings and listing copy for missing translations, RTL/Urdu typography issues, mixed-direction text, consistent terminology, tone, and spelling; read-only on templates/locale files.
- `deploy-checklist` (optional): explains step-by-step Cloud Run/Cloud SQL deploy and rollback in plain language for the non-technical owner; no write tools.
Setup steps for the owner (to be done by an engineer or Claude with approval): create `.claude/agents/<name>.md` files with the frontmatter above, commit them, then invoke by asking "use the security-reviewer agent on this change" or rely on `description` auto-delegation.

### Gaps
- Content of third-party subagent collections (e.g. VoltAgent/awesome-claude-code-subagents, wshobson/agents) not reviewed; I did not evaluate them.
- No verified pre-built Urdu/English i18n checker agent was found; it would need to be custom-written.

## 6. Recommended shortlist (synthesis of the above)

### Takeaway
Start with first-party, low-privilege items that need no infrastructure credentials, then add read-only database and observability, and defer payments and WhatsApp.

### Cited Findings
Sources for each item are in sections 1 to 5; the ordering below is my judgment, not a cited fact.

### Inferences
Minimal first install (max 8, priority order). Publisher/trust and risk in brackets.
1. `.claude/agents` project subagents (security-reviewer, db-migration-reviewer, urdu-english-copy-checker, data-quality-auditor, code-reviewer) — custom, no third-party code, read-only tools. Source: Claude Code docs.
2. `code-review` plugin — Anthropic, `claude plugin install code-review@claude-plugins-official`; flagged "privileged" reach in directory, so review its command file before enabling.
3. `security-guidance` plugin — Anthropic, same marketplace; (function not verified, read README first). Pair with the built-in `/security-review` skill already present in this session.
4. `frontend-design` plugin/skill — Anthropic; presentation-only guidance, low risk.
5. `webapp-testing` skill (anthropics/skills) + Playwright MCP — Microsoft Apache-2.0, `claude mcp add playwright npx @playwright/mcp@latest` (pin the version); run headless against localhost/staging only, not logged in to personal accounts.
6. GitHub MCP — GitHub, MIT; OAuth or fine-grained PAT restricted to this repo, `--read-only` initially. (Note this session already has GitHub tools.)
7. `xlsx` skill — Anthropic (source-available licence) for reviewing import spreadsheets; local file access only.
8. Postgres MCP Pro in restricted mode (Crystal DBA, MIT, community) or MCP Toolbox for Databases (Google, Apache-2.0), against a dev copy with a read-only role.

Later list: Context7 (Upstash; safe-ish docs lookup, data goes via Upstash), Sentry MCP (once Sentry is set up), Cloud Run MCP and gcloud MCP (preview; with a limited service account), Cloudflare MCP (DNS-scoped token; verify DNS edit support), Linear or Notion (only if the owner adopts one), Stripe (after payment provider decision and Pakistan eligibility confirmed), `pdf` skill, `commit-commands`, `hookify`, `claude-md-management`, Google Maps (after confirming an official Google server; otherwise call the Places/Geocoding APIs from application code with a restricted API key).

Avoid list:
- Unofficial WhatsApp bridges (browser automation/reverse-engineered, ToS violation, ban risk) — [dragapp.com](https://www.dragapp.com/blog/whatsapp-mcp-server/)
- Archived Anthropic reference servers (SQLite, PostgreSQL, Puppeteer, Google Maps, GitHub, Slack, Sentry, Brave) and their forks — archived; SQLite had an unpatched SQL injection — [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers); [The Register](https://www.theregister.com/2025/06/25/anthropic_sql_injection_flaw_unfixed/)
- Unvetted registry entries from smithery/mcparmory/a2awire/trycloudflare-hosted endpoints, "stealth" or "bypass Cloudflare" scrapers, and hosted proxy wrappers of vendor APIs — they relay your credentials/data through a third party (registry listings seen in query results).
- Any Postgres server with write access pointed at production; any MCP with broad cloud Owner credentials.
- Security-vendor remote MCPs (Pi Security, Sola, Above Security) and Kobiton, 42Crunch, PactFlow plugins — not relevant to this project's needs and add third-party accounts/data flows (SearchPlugins results).

### Gaps
- Final shortlist should be re-verified (licence file, last commit, README permissions) at install time, since this research could not read commit dates directly.
