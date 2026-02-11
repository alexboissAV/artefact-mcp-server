# Changelog

All notable changes to this project will be documented in this file.

## [0.2.1] - 2026-02-10

### Fixed

- **Smart source defaults** — `run_rfm` and `score_pipeline_health` now default to `source="auto"`, which uses HubSpot if `HUBSPOT_API_KEY` is set, otherwise falls back to sample data. Free users no longer hit a license error on first use.
- **Realistic sample data** — Replaced toy company names ("Acme SaaS Inc.") with believable anonymized names ("Nextera Systems", "Precision Components Group"). Sample dates are now relative (always fresh) instead of hardcoded timestamps that go stale.
- **Actionable HubSpot error messages** — 401/403/429 errors now include step-by-step fix instructions (which scopes to enable, where to find Private Apps in HubSpot settings).
- **Sample data hint** — When results come from sample data, output includes a `_note` explaining how to connect live HubSpot data.

## [0.2.0] - 2026-02-10

### Added

- **ICP inline scoring overrides** — Pro users can now pass `scoring_config` to the `qualify` tool to customize scoring parameters per call: primary/adjacent/excluded industries, revenue range, employee range, primary/secondary geography. AI assistants translate natural language ICP descriptions into config automatically.
- **Pipeline stage auto-detection** — When using live HubSpot data, pipeline stages are now fetched from HubSpot's API instead of using hardcoded defaults. Works with any custom pipeline configuration.
- **`fetch_pipeline_stages()` HubSpot client method** — New method to retrieve pipeline stage definitions in display order.

### Changed

- `ICPScorer` now accepts optional `scoring_config` dict in constructor for parameter overrides.
- `_calculate_velocity()` and `_find_at_risk_deals()` accept optional stage order/labels for dynamic pipelines.
- `score_pipeline()` auto-detects stages when HubSpot client is available, falls back to defaults gracefully.

## [0.1.2] - 2026-02-10

### Fixed

- Fixed `mcp-name` case mismatch in README for Official MCP Registry validation.
- Added `.mcpregistry_*` to `.gitignore` to prevent token file leaks.

## [0.1.1] - 2026-02-10

### Added

- **Tool safety annotations** — All 3 tools now declare `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` per MCP spec. Required for Claude Desktop Extensions approval.
- **COMPARISON.md** — Detailed comparison vs HubSpot Official MCP, CData, Zapier, and generic wrappers.
- **ARCHITECTURE.md** — System diagram, data flow documentation, scoring engine reference.
- **CHANGELOG.md** — Release history.
- **GitHub Discussions** — Community engagement with seed topics.

## [0.1.0] - 2026-02-10

### Added

- **RFM Analysis tool** (`run_rfm`) — Scores clients on Recency, Frequency, and Monetary value. Segments into 11 categories. Extracts ICP patterns from top performers. Supports B2B service, SaaS, and manufacturing presets.
- **ICP Qualification tool** (`qualify`) — 14.5-point scoring model across Firmographic Fit (5 pts), Behavioral Fit (5 pts), and Strategic Fit (4.5 pts). Returns tier classification and engagement strategy.
- **Pipeline Health tool** (`score_pipeline_health`) — Calculates 0-100 health score with velocity metrics, stage-to-stage conversion rates, bottleneck identification, and at-risk deal detection.
- **4 methodology resources** — Scoring model, tier definitions, RFM segments, SPICED framework.
- **HubSpot integration** — Pull live CRM data for all 3 tools via HubSpot API v3.
- **Built-in sample data** — All tools work without an API key using `source="sample"`.
- **License gating** — Free tier (sample data), Pro ($149/mo), Enterprise ($499/mo) via LemonSqueezy.
- **4 industry presets** — Default, B2B Service, SaaS, Manufacturing (different RFM thresholds).
- **64 unit tests** — Full test coverage for all scoring engines, tools, and license module.
