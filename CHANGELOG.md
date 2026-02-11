# Changelog

All notable changes to this project will be documented in this file.

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
