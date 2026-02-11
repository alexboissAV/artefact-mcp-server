"""
Artefact Revenue Intelligence MCP Server

FastMCP server that exposes 3 revenue intelligence tools and 4 methodology resources.
Free tier works with sample data. Pro/Enterprise tiers require ARTEFACT_LICENSE_KEY.
"""

import json
import os
import sys
from typing import Optional

from fastmcp import FastMCP

from artefact_mcp.core.hubspot_client import HubSpotClient
from artefact_mcp.core.license import validate_license, require_license, LicenseInfo
from artefact_mcp.tools.rfm import run_rfm_analysis
from artefact_mcp.tools.icp import qualify_prospect
from artefact_mcp.tools.pipeline import score_pipeline
from artefact_mcp.resources.methodology import get_resource, list_resources

# --- License validation at startup ---
_license: LicenseInfo = validate_license()

if not _license.valid:
    print(f"[Artefact MCP] License error: {_license.error}", file=sys.stderr)
    print("[Artefact MCP] Running in free mode (sample data only).", file=sys.stderr)
    _license.tier = "free"
elif _license.tier == "free":
    print("[Artefact MCP] No license key found. Running in free mode (sample data only).", file=sys.stderr)
    print("[Artefact MCP] Purchase a license at https://artefactventures.lemonsqueezy.com", file=sys.stderr)
else:
    print(f"[Artefact MCP] License valid — tier: {_license.tier}", file=sys.stderr)
    if _license.customer_name:
        print(f"[Artefact MCP] Licensed to: {_license.customer_name}", file=sys.stderr)

# --- Server ---

mcp = FastMCP(
    "Artefact Revenue Intelligence",
    instructions=(
        "Revenue intelligence tools powered by the Artefact Formula methodology. "
        "Includes RFM analysis, ICP scoring (14.5-point model), and pipeline health scoring. "
        + (
            "Connect to HubSpot for live data or use built-in sample data."
            if _license.tier != "free"
            else "Running in free mode — use source='sample' for demo data. "
            "Purchase a Pro license for live HubSpot integration."
        )
    ),
)


def _get_hubspot_client() -> Optional[HubSpotClient]:
    """Create a HubSpot client if API key is available."""
    api_key = os.getenv("HUBSPOT_API_KEY")
    if api_key:
        return HubSpotClient(api_key)
    return None


# --- Tools ---


@mcp.tool(
    annotations={
        "title": "RFM Analysis",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
def run_rfm(
    source: str = "hubspot",
    industry_preset: str = "default",
) -> str:
    """Run RFM (Recency, Frequency, Monetary) analysis on client data.

    Scores clients based on purchase behavior, segments them into 11 categories,
    and extracts ICP patterns from top performers.

    Args:
        source: Data source — "hubspot" for live HubSpot data, "sample" for built-in demo data.
        industry_preset: Scoring preset — "b2b_service", "saas", "manufacturing", or "default".

    Returns:
        JSON with scored clients, segment distribution, ICP patterns, and tier recommendations.
    """
    try:
        require_license(source, _license)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    client = _get_hubspot_client() if source == "hubspot" else None
    try:
        result = run_rfm_analysis(
            source=source,
            industry_preset=industry_preset,
            hubspot_client=client,
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        if client:
            client.close()


@mcp.tool(
    annotations={
        "title": "ICP Qualification",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
def qualify(
    company_id: Optional[str] = None,
    company_data: Optional[str] = None,
) -> str:
    """Score a prospect against the Artefact 14.5-point ICP model.

    Evaluates Firmographic Fit (5 pts), Behavioral Fit (5 pts), and Strategic Fit (4.5 pts).
    Returns tier classification (1-4), score breakdown, and recommended engagement strategy.

    Provide EITHER company_id (HubSpot ID, requires HUBSPOT_API_KEY) OR company_data (JSON string).

    Args:
        company_id: HubSpot company ID to fetch and score.
        company_data: JSON string with company attributes. Example keys:
            industry, annual_revenue, employee_count, geography, tech_stack (list),
            growth_signals (list), content_engagement ("active"|"occasional"|"none"),
            purchase_history ("regular"|"occasional"|"never"),
            decision_maker_access ("c_suite"|"director"|"manager"|"indirect"|"none"),
            budget_authority ("dedicated"|"shared"|"possible"|"none"),
            strategic_alignment ("strong"|"partial"|"misaligned").

    Returns:
        JSON with total score, tier, breakdown, exclusion check, and recommended action.
    """
    # company_id requires HubSpot = requires license
    if company_id:
        try:
            require_license("hubspot", _license)
        except ValueError as e:
            return json.dumps({"error": str(e)})

    parsed_data = None
    if company_data:
        try:
            parsed_data = json.loads(company_data) if isinstance(company_data, str) else company_data
        except (json.JSONDecodeError, TypeError) as e:
            return json.dumps({"error": f"Invalid company_data JSON: {e}"})

    client = _get_hubspot_client() if company_id else None
    try:
        result = qualify_prospect(
            company_id=company_id,
            company_data=parsed_data,
            hubspot_client=client,
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        if client:
            client.close()


@mcp.tool(
    annotations={
        "title": "Pipeline Health Score",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
def score_pipeline_health(
    pipeline_id: Optional[str] = None,
    source: str = "hubspot",
) -> str:
    """Analyze pipeline health with velocity metrics, conversion rates, and at-risk detection.

    Calculates overall health score (0-100), identifies bottleneck stages,
    measures stage-to-stage conversion rates, and flags stalled or overdue deals.

    Args:
        pipeline_id: Optional HubSpot pipeline ID to filter. Default: all pipelines.
        source: "hubspot" for live data, "sample" for built-in demo data.

    Returns:
        JSON with health score, velocity metrics, conversion rates, at-risk deals, and stage distribution.
    """
    try:
        require_license(source, _license)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    client = _get_hubspot_client() if source == "hubspot" else None
    try:
        result = score_pipeline(
            pipeline_id=pipeline_id,
            source=source,
            hubspot_client=client,
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        if client:
            client.close()


# --- Resources ---


@mcp.resource("methodology://scoring-model")
def scoring_model() -> str:
    """ICP 14.5-point scoring model reference."""
    return get_resource("scoring-model")


@mcp.resource("methodology://tier-definitions")
def tier_definitions() -> str:
    """4-tier classification system (Ideal / Strong / Moderate / Poor)."""
    return get_resource("tier-definitions")


@mcp.resource("methodology://rfm-segments")
def rfm_segments() -> str:
    """11 RFM segment definitions with scoring scales."""
    return get_resource("rfm-segments")


@mcp.resource("methodology://spiced-framework")
def spiced_framework() -> str:
    """SPICED discovery framework reference."""
    return get_resource("spiced-framework")


def main():
    """Entry point for the MCP server."""
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "streamable-http":
        host = os.getenv("MCP_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_PORT", os.getenv("PORT", "8000")))
        mcp.run(transport="streamable-http", host=host, port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
