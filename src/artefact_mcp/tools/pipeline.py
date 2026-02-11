"""
score_pipeline tool

Analyzes pipeline health by calculating velocity metrics, conversion rates,
bottleneck identification, and at-risk deal detection.

Ported from useDealVelocity.ts (artefact-grow).
"""

from datetime import datetime
from typing import Optional

from artefact_mcp.core.hubspot_client import HubSpotClient


SAMPLE_DEALS = [
    {"id": "D001", "name": "Acme Corp - CRO Platform", "amount": 45000, "stage": "qualifiedtobuy", "pipeline": "default", "create_date": "2025-11-01", "close_date": "2026-03-15", "last_modified": "2026-02-05"},
    {"id": "D002", "name": "Northern Tech - Discovery", "amount": 28000, "stage": "appointmentscheduled", "pipeline": "default", "create_date": "2026-01-10", "close_date": "2026-04-01", "last_modified": "2026-02-08"},
    {"id": "D003", "name": "Maple Mfg - Full Engagement", "amount": 92000, "stage": "presentationscheduled", "pipeline": "default", "create_date": "2025-09-15", "close_date": "2026-02-28", "last_modified": "2026-01-20"},
    {"id": "D004", "name": "Atlantic Services - Audit", "amount": 15000, "stage": "decisionmakerboughtin", "pipeline": "default", "create_date": "2025-12-01", "close_date": "2026-03-01", "last_modified": "2026-02-01"},
    {"id": "D005", "name": "Prairie Logistics - Pipeline", "amount": 38000, "stage": "qualifiedtobuy", "pipeline": "default", "create_date": "2025-10-20", "close_date": "2026-03-30", "last_modified": "2026-01-15"},
    {"id": "D006", "name": "Halifax Consulting - Stalled", "amount": 22000, "stage": "appointmentscheduled", "pipeline": "default", "create_date": "2025-07-01", "close_date": "2026-01-15", "last_modified": "2025-10-20"},
    {"id": "D007", "name": "Vancouver FinTech - Expansion", "amount": 65000, "stage": "contractsent", "pipeline": "default", "create_date": "2025-08-15", "close_date": "2026-02-20", "last_modified": "2026-02-07"},
    {"id": "D008", "name": "Calgary Construction - Intro", "amount": 18000, "stage": "appointmentscheduled", "pipeline": "default", "create_date": "2026-01-25", "close_date": "2026-05-01", "last_modified": "2026-02-03"},
]

# Default pipeline stage order (HubSpot default pipeline)
DEFAULT_STAGE_ORDER = [
    "appointmentscheduled",
    "qualifiedtobuy",
    "presentationscheduled",
    "decisionmakerboughtin",
    "contractsent",
]

STAGE_LABELS = {
    "appointmentscheduled": "Appointment Scheduled",
    "qualifiedtobuy": "Qualified to Buy",
    "presentationscheduled": "Presentation Scheduled",
    "decisionmakerboughtin": "Decision Maker Bought-In",
    "contractsent": "Contract Sent",
}


def _parse_date(value) -> Optional[datetime]:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        try:
            return datetime.strptime(str(value), "%Y-%m-%d")
        except (ValueError, TypeError):
            return None


def _calculate_velocity(
    deals: list[dict],
    now: datetime,
    stage_order: list[str] | None = None,
    stage_labels: dict[str, str] | None = None,
) -> dict:
    """Calculate stage velocity metrics from deal data.

    Estimates time-in-stage based on deal creation date and current stage,
    since HubSpot stage history requires per-deal API calls.

    Args:
        deals: List of deal dicts.
        now: Current datetime.
        stage_order: Ordered list of stage IDs. Falls back to DEFAULT_STAGE_ORDER.
        stage_labels: Map of stage ID to display label. Falls back to STAGE_LABELS.
    """
    _order = stage_order or DEFAULT_STAGE_ORDER
    _labels = stage_labels or STAGE_LABELS

    stage_durations: dict[str, list[int]] = {}
    deal_stages: dict[str, set[str]] = {}

    for deal in deals:
        stage = deal.get("stage", "")
        create_date = _parse_date(deal.get("create_date"))
        last_modified = _parse_date(deal.get("last_modified"))

        if not stage or not create_date:
            continue

        # Track which deals are in which stages
        if stage not in deal_stages:
            deal_stages[stage] = set()
        deal_stages[stage].add(deal.get("id", ""))

        # Calculate days in current stage (from last modified as proxy)
        ref_date = last_modified or now
        if ref_date.tzinfo and not now.tzinfo:
            ref_date = ref_date.replace(tzinfo=None)
        days = max((now - create_date.replace(tzinfo=None)).days, 0)

        if stage not in stage_durations:
            stage_durations[stage] = []
        stage_durations[stage].append(days)

    # Average days per stage
    avg_days: dict[str, float] = {}
    max_avg = 0.0
    bottleneck = None

    for stage in _order:
        if stage in stage_durations:
            durations = stage_durations[stage]
            avg = sum(durations) / len(durations)
            avg_days[_labels.get(stage, stage)] = round(avg, 1)
            if avg > max_avg:
                max_avg = avg
                bottleneck = _labels.get(stage, stage)

    overall = round(sum(avg_days.values()), 0)

    # Conversion rates (deals that moved past each stage)
    conversion_rates: dict[str, float] = {}
    for i in range(len(_order) - 1):
        current = _order[i]
        next_stage = _order[i + 1]

        # Deals at or past current stage
        current_count = 0
        next_count = 0
        current_idx = _order.index(current)
        next_idx = _order.index(next_stage)

        for deal in deals:
            deal_stage = deal.get("stage", "")
            if deal_stage in _order:
                deal_idx = _order.index(deal_stage)
                if deal_idx >= current_idx:
                    current_count += 1
                if deal_idx >= next_idx:
                    next_count += 1

        rate = round(next_count / current_count * 100) if current_count > 0 else 0
        label = f"{_labels.get(current, current)} -> {_labels.get(next_stage, next_stage)}"
        conversion_rates[label] = rate

    return {
        "avg_days_per_stage": avg_days,
        "bottleneck_stage": bottleneck,
        "overall_cycle_days": int(overall),
        "conversion_rates": conversion_rates,
    }


def _find_at_risk_deals(
    deals: list[dict],
    now: datetime,
    stage_labels: dict[str, str] | None = None,
) -> list[dict]:
    """Identify deals that are at risk based on age and stagnation."""
    _labels = stage_labels or STAGE_LABELS
    at_risk = []

    for deal in deals:
        create_date = _parse_date(deal.get("create_date"))
        last_modified = _parse_date(deal.get("last_modified"))
        close_date = _parse_date(deal.get("close_date"))

        if not create_date:
            continue

        # Days since last activity
        ref = last_modified or create_date
        if ref.tzinfo:
            ref = ref.replace(tzinfo=None)
        days_stagnant = (now - ref).days

        # Days since creation
        cd = create_date.replace(tzinfo=None) if create_date.tzinfo else create_date
        days_total = (now - cd).days

        # Past close date?
        past_due = False
        if close_date:
            cld = close_date.replace(tzinfo=None) if close_date.tzinfo else close_date
            past_due = now > cld

        risk_reasons = []
        if days_stagnant > 30:
            risk_reasons.append(f"No activity for {days_stagnant} days")
        if past_due:
            risk_reasons.append("Past expected close date")
        if days_total > 180:
            risk_reasons.append(f"Open for {days_total} days (>6 months)")

        if risk_reasons:
            at_risk.append({
                "id": deal.get("id"),
                "name": deal.get("name"),
                "days_in_pipeline": days_total,
                "stage": _labels.get(deal.get("stage", ""), deal.get("stage", "")),
                "amount": deal.get("amount", 0),
                "risk_reasons": risk_reasons,
            })

    at_risk.sort(key=lambda x: len(x["risk_reasons"]), reverse=True)
    return at_risk


def _calculate_health_score(
    deals: list[dict], velocity: dict, at_risk: list[dict]
) -> tuple[int, str]:
    """Calculate overall pipeline health score (0-100)."""
    if not deals:
        return 0, "Critical"

    score = 100

    # Penalty for at-risk deals
    risk_pct = len(at_risk) / len(deals) * 100
    if risk_pct > 50:
        score -= 40
    elif risk_pct > 30:
        score -= 25
    elif risk_pct > 15:
        score -= 10

    # Penalty for slow velocity
    cycle = velocity.get("overall_cycle_days", 0)
    if cycle > 180:
        score -= 25
    elif cycle > 120:
        score -= 15
    elif cycle > 90:
        score -= 5

    # Penalty for low conversion rates
    rates = velocity.get("conversion_rates", {})
    if rates:
        avg_rate = sum(rates.values()) / len(rates)
        if avg_rate < 30:
            score -= 20
        elif avg_rate < 50:
            score -= 10

    # Bonus for deal count
    if len(deals) < 3:
        score -= 15  # Too few deals
    elif len(deals) >= 10:
        score += 5  # Healthy pipeline volume

    score = max(0, min(100, score))

    if score >= 70:
        label = "Healthy"
    elif score >= 40:
        label = "Warning"
    else:
        label = "Critical"

    return score, label


def score_pipeline(
    pipeline_id: Optional[str] = None,
    source: str = "hubspot",
    hubspot_client: Optional[HubSpotClient] = None,
) -> dict:
    """Score pipeline health with velocity metrics and at-risk detection.

    Args:
        pipeline_id: Optional pipeline ID filter.
        source: "hubspot" or "sample".
        hubspot_client: Pre-configured HubSpotClient (required for source="hubspot").

    Returns:
        Pipeline health analysis dict.
    """
    now = datetime.now()

    if source == "sample":
        deals = SAMPLE_DEALS
    elif source == "hubspot":
        if not hubspot_client:
            raise ValueError(
                "HubSpot client required for source='hubspot'. "
                "Set HUBSPOT_API_KEY environment variable."
            )
        deals = hubspot_client.fetch_open_deals(pipeline_id)
    else:
        raise ValueError(f"Invalid source: {source}. Use 'hubspot' or 'sample'.")

    # Auto-detect pipeline stages from HubSpot when using live data
    stage_order = None
    stage_labels = None

    if source == "hubspot" and hubspot_client:
        try:
            hs_stages = hubspot_client.fetch_pipeline_stages(pipeline_id or "default")
            if hs_stages:
                stage_order = [s["id"] for s in hs_stages]
                stage_labels = {s["id"]: s["label"] for s in hs_stages}
        except (ValueError, Exception):
            pass  # Fall back to defaults if pipeline fetch fails

    if not deals:
        return {
            "health_score": 0,
            "health_label": "Critical",
            "total_deals": 0,
            "total_value": 0,
            "velocity": {},
            "conversion_rates": {},
            "at_risk_deals": [],
            "stage_distribution": {},
        }

    _labels = stage_labels or STAGE_LABELS
    total_value = sum(d.get("amount", 0) for d in deals)

    # Velocity metrics
    velocity = _calculate_velocity(deals, now, stage_order, stage_labels)

    # At-risk deals
    at_risk = _find_at_risk_deals(deals, now, stage_labels)

    # Health score
    health_score, health_label = _calculate_health_score(deals, velocity, at_risk)

    # Stage distribution
    stage_dist: dict = {}
    for deal in deals:
        stage = _labels.get(deal.get("stage", ""), deal.get("stage", ""))
        if stage not in stage_dist:
            stage_dist[stage] = {"count": 0, "value": 0}
        stage_dist[stage]["count"] += 1
        stage_dist[stage]["value"] += deal.get("amount", 0)

    return {
        "health_score": health_score,
        "health_label": health_label,
        "total_deals": len(deals),
        "total_value": round(total_value, 2),
        "velocity": {
            "avg_days_per_stage": velocity["avg_days_per_stage"],
            "bottleneck_stage": velocity["bottleneck_stage"],
            "overall_cycle_days": velocity["overall_cycle_days"],
        },
        "conversion_rates": velocity["conversion_rates"],
        "at_risk_deals": at_risk,
        "stage_distribution": stage_dist,
    }
