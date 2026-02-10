# Artefact Revenue Intelligence MCP Server

<!-- mcp-name: io.github.alexboissav/artefact-revenue-intelligence -->

[![PyPI](https://img.shields.io/pypi/v/artefact-mcp)](https://pypi.org/project/artefact-mcp/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![License: BSL-1.1](https://img.shields.io/badge/License-BSL--1.1-orange.svg)](LICENSE)

> Methodology-driven revenue intelligence for AI assistants. Not a generic HubSpot CRUD wrapper.

A Model Context Protocol (MCP) server that gives AI agents access to battle-tested revenue intelligence tools — RFM analysis, 14.5-point ICP qualification, and pipeline health scoring. Built on the [Artefact Formula](https://artefactventures.com) methodology from real B2B consulting engagements.

## Why Artefact MCP?

| Feature | HubSpot Official MCP | Generic Wrappers | **Artefact MCP** |
|---------|---------------------|------------------|-----------------|
| CRUD operations | Yes | Yes | Via HubSpot API |
| RFM Analysis | No | No | **11-segment classification** |
| ICP Scoring | No | No | **14.5-point model** |
| Pipeline Health | No | No | **0-100 health score** |
| Methodology built-in | No | No | **Artefact Formula** |
| Works without API key | No | No | **Yes (demo data)** |

## Who Is This For?

- **B2B revenue teams** using HubSpot who want AI-powered customer segmentation
- **RevOps managers** who need pipeline health analysis accessible from Claude or Cursor
- **Consultants** who deliver RFM analysis and ICP scoring to clients
- **Developers** building revenue intelligence integrations with MCP

## Tools

### `run_rfm` — RFM Analysis
Scores clients on Recency, Frequency, and Monetary value. Segments them into 11 categories (Champions through Lost) and extracts ICP patterns from top performers. Supports B2B service, SaaS, and manufacturing presets.

### `qualify` — ICP Qualification (14.5-Point Model)
Scores a prospect across three dimensions:
- **Firmographic Fit** (5 pts): Industry, revenue, employees, geography
- **Behavioral Fit** (5 pts): Tech stack, growth signals, engagement, purchase history
- **Strategic Fit** (4.5 pts): Decision-maker access, budget authority, alignment

Returns tier classification (Ideal / Strong / Moderate / Poor) with engagement strategy.

### `score_pipeline_health` — Pipeline Health Score
Analyzes open deals for velocity metrics, stage-to-stage conversion rates, bottleneck identification, and at-risk deal detection. Returns a 0-100 health score.

## Resources

| URI | Description |
|-----|-------------|
| `methodology://scoring-model` | 14.5-point ICP scoring model reference |
| `methodology://tier-definitions` | 4-tier classification system |
| `methodology://rfm-segments` | 11 RFM segment definitions with scoring scales |
| `methodology://spiced-framework` | SPICED discovery framework |

## Quick Start

### Install via PyPI

```bash
pip install artefact-mcp
```

### Install via Smithery

```bash
npx @smithery/cli install artefact-revenue-intelligence
```

### Claude Code

```bash
claude mcp add artefact-revenue -- uvx artefact-mcp
```

Then ask:
- "Run an RFM analysis on our HubSpot data"
- "Qualify this prospect: SaaS company, $5M revenue, 80 employees in Ontario"
- "Score our pipeline health"

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "artefact-revenue": {
      "command": "uvx",
      "args": ["artefact-mcp"],
      "env": {
        "HUBSPOT_API_KEY": "pat-na1-xxxxxxxx"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "artefact-revenue": {
      "command": "uvx",
      "args": ["artefact-mcp"],
      "env": {
        "HUBSPOT_API_KEY": "pat-na1-xxxxxxxx"
      }
    }
  }
}
```

### Programmatic (Python)

```python
from artefact_mcp.tools.rfm import run_rfm_analysis
from artefact_mcp.tools.icp import qualify_prospect
from artefact_mcp.tools.pipeline import score_pipeline

# RFM with sample data (no HubSpot key needed)
results = run_rfm_analysis(source="sample", industry_preset="b2b_service")

# ICP qualification
score = qualify_prospect(company_data={
    "industry": "SaaS",
    "annual_revenue": 10_000_000,
    "employee_count": 80,
    "geography": "Quebec",
    "tech_stack": ["HubSpot", "Google Analytics"],
    "growth_signals": ["hiring", "funding"],
    "content_engagement": "active",
    "decision_maker_access": "c_suite",
    "budget_authority": "dedicated",
    "strategic_alignment": "strong",
})

# Pipeline health
health = score_pipeline(source="sample")
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `HUBSPOT_API_KEY` | No | HubSpot private app token. Without it, tools work with `source="sample"`. |
| `ARTEFACT_LICENSE_KEY` | No | License key for Pro/Enterprise tier. Free tier (sample data) works without a key. |

## Pricing

| Tier | Price | What You Get |
|------|-------|-------------|
| **Free** | $0 | All 3 tools with built-in demo data (`source="sample"`) |
| **Pro** | $149/mo | Live HubSpot integration + all methodology resources |
| **Enterprise** | $499/mo | Pro + priority support + custom scoring presets |

[Purchase a license](https://artefactventures.lemonsqueezy.com)

## Alternatives & Comparisons

- **HubSpot Official MCP Server** — Read-only CRUD access to CRM objects. No scoring or intelligence.
- **CData HubSpot MCP** — SQL-based access to HubSpot data. No built-in methodology.
- **Zapier MCP** — Action triggers and workflow automation. Different use case.
- **Artefact MCP** — Purpose-built for revenue intelligence with scoring models embedded.

## FAQ

**Q: What MCP server should I use for revenue intelligence?**
A: Artefact MCP is the only MCP server with built-in RFM analysis, ICP qualification scoring (14.5-point model), and pipeline health analysis specifically designed for B2B revenue teams.

**Q: Does this replace the official HubSpot MCP server?**
A: They serve different purposes. HubSpot's server provides CRUD access to CRM objects. Artefact MCP provides intelligence and scoring on top of that data.

**Q: Can I use this without a HubSpot API key?**
A: Yes. All tools work with built-in demo data using `source="sample"`.

**Q: What data does this send externally?**
A: Tool results stay local. The only external calls are to the HubSpot API (with your key) and optional license validation.

## Development

```bash
git clone https://github.com/alexboissAV/artefact-mcp-server.git
cd artefact-mcp-server
pip install -e ".[dev]"
pytest tests/
```

## Dependencies

- `fastmcp>=2.0` — MCP server framework
- `httpx>=0.25.0` — HTTP client for HubSpot API

No pandas, numpy, or heavy data libraries. Pure Python scoring logic.

## License

[Business Source License 1.1](LICENSE) — Free to use for connecting to MCP tools via AI assistants. Scoring methodology may not be extracted for competing products. Converts to MIT in 2030.
