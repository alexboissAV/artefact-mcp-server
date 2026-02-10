"""
Static methodology resources for the Artefact Revenue Intelligence MCP server.

Exposed as MCP resources so AI assistants can reference the scoring models,
tier definitions, segment definitions, and SPICED framework.
"""

SCORING_MODEL = """# ICP Scoring Model (14.5 Points)

## Firmographic Fit (5 points)
- **Industry** (2 pts): Primary target = 2.0, Adjacent = 1.0, Tangential = 0.5, Outside = 0
- **Revenue Range** (1.5 pts): Sweet spot ($1.6M-$70M) = 1.5, Acceptable = 1.0, Stretch = 0.5, Outside = 0
- **Employee Count** (1 pt): Ideal (10-200) = 1.0, Borderline = 0.5, Outside = 0
- **Geography** (0.5 pts): Primary (Canada) = 0.5, Secondary (US) = 0.25, Outside = 0

## Behavioral Fit (5 points)
- **Tech Stack Match** (2 pts): Full core (HubSpot+) = 2.0, Most = 1.5, Partial = 1.0, Minimal = 0.5, None = 0
- **Growth Signals** (1.5 pts): Multiple (3+) = 1.5, Some (2) = 1.0, Weak (1) = 0.5, None = 0
- **Content Engagement** (1 pt): Active = 1.0, Occasional = 0.5, None = 0
- **Purchase Frequency** (0.5 pts): Regular = 0.5, Occasional = 0.25, Never = 0

## Strategic Fit (4.5 points)
- **Decision-Maker Access** (2 pts): C-suite = 2.0, Director = 1.5, Manager = 1.0, Indirect = 0.5, None = 0
- **Budget Authority** (1.5 pts): Dedicated = 1.5, Shared = 1.0, Possible = 0.5, None = 0
- **Strategic Alignment** (1 pt): Strong = 1.0, Partial = 0.5, Misaligned = 0

## Exclusions
Industries excluded from scoring: Agencies, Consulting firms, B2C/Retail, Non-profits, Staffing, Events Services, VC/PE

## 5 Discriminators (Must Have 4 of 5)
1. HubSpot Active User (Mandatory)
2. Revenue Architecture Conviction (Mandatory)
3. Marketing Function Engaged (Mandatory)
4. Clear Growth Targets (High)
5. Multiple Stakeholders (High)
"""

TIER_DEFINITIONS = """# ICP Tier Definitions

## Tier 1: Ideal (12.0 - 14.5 points)
- **Color:** Green | **HubSpot:** tier_1_ideal
- Pursue aggressively. Same-day response. Senior team, custom proposals, full pricing.
- Expected: 40-60% win rate, shortest cycle, highest LTV
- Distribution: 10-15% of addressable market

## Tier 2: Strong (9.0 - 11.9 points)
- **Color:** Blue | **HubSpot:** tier_2_strong
- Active pursuit. 24h response. Standard team, selective discounting.
- Expected: 25-40% win rate, moderate cycle, good LTV
- Distribution: 20-30% of addressable market

## Tier 3: Moderate (6.0 - 8.9 points)
- **Color:** Yellow | **HubSpot:** tier_3_moderate
- Selective — inbound or strategic only. 48h response. Junior team.
- Expected: 10-25% win rate, longer cycle, lower LTV
- Distribution: 30-40% of addressable market

## Tier 4: Poor (0 - 5.9 points)
- **Color:** Red | **HubSpot:** tier_4_poor
- Deprioritize — nurture only. No SLA. Fully automated.
- Expected: <10% win rate, longest cycle, lowest LTV
- Distribution: 20-30% of addressable market

## Health Check
- Tier 1: 10-15% (>25% or <5% = adjust thresholds)
- Tier 1+2: 30-45% (>60% or <20% = review criteria)
- Tier 4: 20-30% (>50% or <10% = revisit model)
"""

RFM_SEGMENTS = """# RFM Segment Definitions (11 Segments)

| Segment | R | F | Total | Action |
|---------|---|---|-------|--------|
| **Champions** | >=4 | >=4 | >=13 | Reward loyalty, ask for referrals |
| **Loyal Customers** | >=3 | >=3 | >=11 | Cross-sell, maintain relationship |
| **Potential Loyalists** | >=4 | 2-3 | >=9 | Nurture with targeted content |
| **New Customers** | =5 | =1 | >=8 | Exceptional onboarding |
| **Promising** | =4 | =1 | >=7 | Second purchase incentive |
| **Need Attention** | =3 | 2-3 | 7-10 | Re-engagement campaigns |
| **About to Sleep** | 2-3 | 1-2 | 5-8 | Win-back campaigns |
| **At Risk** | <=2 | >=3 | >=8 | Urgent outreach, investigate |
| **Can't Lose Them** | 1-2 | >=4 | >=10 | Executive outreach, service recovery |
| **Hibernating** | <=2 | <=2 | <=6 | Low-cost re-engagement |
| **Lost** | =1 | =1 | <=4 | Remove from active campaigns |

## Scoring Scales (1-5)
- **Recency:** Days since last purchase (lower = better). Default: <=30=5, 31-90=4, 91-180=3, 181-365=2, 366+=1
- **Frequency:** Transaction count (higher = better). Default: 10+=5, 5-9=4, 3-4=3, 2=2, 1=1
- **Monetary:** Revenue percentile (higher = better). Default: Top 20%=5, 60-80%=4, 40-60%=3, 20-40%=2, Bottom 20%=1

## Industry Presets
- **B2B Service:** Longer recency windows (60/180/365/730 days)
- **SaaS:** Shorter recency windows (30/60/90/180 days)
- **Manufacturing:** Longest cycles (90/365/730/1095 days)
"""

SPICED_FRAMEWORK = """# SPICED Discovery Framework

SPICED is Artefact Ventures' discovery methodology for extracting deal intelligence.

| Letter | Dimension | What to Extract |
|--------|-----------|-----------------|
| **S** | Situation | Current state — growth plateau, operational silos, tech stack, team structure |
| **P** | Pain | Core pain — revenue predictability, invisible ROI, departmental silos, manual processes |
| **I** | Impact | Quantified impact — $2-5M revenue lost annually, missed opportunities, team churn |
| **C** | Critical Event | Trigger — investor pressure, competitive threat, missed quarter, leadership change |
| **E** | Economic Buyer | Decision maker — typically CEO + CFO, 2-3 month decision cycle |
| **D** | Decision Process | Committee of 3-4, needs cross-functional alignment, approval workflow |

## Key Personas

### François - SMB CEO
- Pain: Revenue predictability, invisible marketing ROI
- Trigger: Investor pressure, competitive threat
- Cycle: 2-3 months, committee decision

### Martin - VP Sales
- Pain: Chaotic pipeline, underperforming team
- Trigger: Missed quarter, lost top performer
- Cycle: 2-4 weeks, needs CEO approval

## Qualification Signals

### Great Fit
- HubSpot active with data
- Leadership convinced on revenue architecture
- Marketing + Sales alignment
- Clear growth targets with timeline
- 2-3+ stakeholders engaged

### Poor Fit
- NOT convinced on CRM value
- NO marketing role/function
- NO clear vision or targets
- Single decision maker resistant to change
- Looking for "just a tool"
"""


def get_resource(name: str) -> str:
    """Get a methodology resource by name."""
    resources = {
        "scoring-model": SCORING_MODEL,
        "tier-definitions": TIER_DEFINITIONS,
        "rfm-segments": RFM_SEGMENTS,
        "spiced-framework": SPICED_FRAMEWORK,
    }
    return resources.get(name, f"Unknown resource: {name}")


def list_resources() -> list[dict]:
    """List all available methodology resources."""
    return [
        {"uri": "methodology://scoring-model", "name": "ICP Scoring Model", "description": "14.5-point ICP scoring model reference"},
        {"uri": "methodology://tier-definitions", "name": "Tier Definitions", "description": "4-tier classification system"},
        {"uri": "methodology://rfm-segments", "name": "RFM Segments", "description": "11 RFM segment definitions"},
        {"uri": "methodology://spiced-framework", "name": "SPICED Framework", "description": "SPICED discovery extraction reference"},
    ]
