"""
qualify_prospect tool

Scores a prospect/company against the Artefact 14.5-point ICP model.
Accepts a HubSpot company ID or manual company data dict.
"""

from typing import Optional

from artefact_mcp.core.icp_scorer import ICPScorer
from artefact_mcp.core.hubspot_client import HubSpotClient


def qualify_prospect(
    company_id: Optional[str] = None,
    company_data: Optional[dict] = None,
    hubspot_client: Optional[HubSpotClient] = None,
) -> dict:
    """Score a prospect against the 14.5-point ICP model.

    Args:
        company_id: HubSpot company ID. If provided, fetches data from HubSpot.
        company_data: Manual dict with company attributes. Used if company_id is None.
        hubspot_client: Pre-configured HubSpotClient (required if company_id given).

    Returns:
        Full scoring result dict.
    """
    if not company_id and not company_data:
        raise ValueError("Either company_id or company_data must be provided.")

    scorer = ICPScorer()

    if company_id:
        if not hubspot_client:
            raise ValueError(
                "HubSpot client required when using company_id. "
                "Set HUBSPOT_API_KEY environment variable."
            )
        hs_data = hubspot_client.fetch_company(company_id)

        # Map HubSpot fields to ICP scorer input format
        company_data = {
            "company_name": hs_data.get("name", "Unknown"),
            "hubspot_id": company_id,
            "industry": hs_data.get("industry", ""),
            "annual_revenue": hs_data.get("annual_revenue"),
            "employee_count": hs_data.get("employee_count"),
            "geography": hs_data.get("geography", ""),
            # These behavioral/strategic fields can't be auto-populated from HubSpot
            # basic fields — the tool will score them as 0 if not provided
            "tech_stack": company_data.get("tech_stack", []) if company_data else [],
            "growth_signals": company_data.get("growth_signals", []) if company_data else [],
            "content_engagement": company_data.get("content_engagement", "none") if company_data else "none",
            "purchase_history": company_data.get("purchase_history", "never") if company_data else "never",
            "decision_maker_access": company_data.get("decision_maker_access", "none") if company_data else "none",
            "budget_authority": company_data.get("budget_authority", "none") if company_data else "none",
            "strategic_alignment": company_data.get("strategic_alignment", "misaligned") if company_data else "misaligned",
        }

    result = scorer.score_company(company_data)

    return {
        "company": {
            "name": company_data.get("company_name", company_data.get("name", "Unknown")),
            "hubspot_id": company_data.get("hubspot_id"),
            "industry": company_data.get("industry"),
        },
        "total_score": result.total_score,
        "tier": result.tier,
        "breakdown": result.breakdown,
        "exclusion_check": result.exclusion_check,
        "recommended_action": result.recommended_action,
        "engagement_strategy": result.engagement_strategy,
    }
