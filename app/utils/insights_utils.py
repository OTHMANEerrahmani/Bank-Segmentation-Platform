import pandas as pd
from typing import Any


def create_segment_name(profile: dict[str, str | int | float]) -> str:
    """Generates a descriptive name for a customer segment."""
    income = float(profile["avg_income"])
    savings = float(profile["avg_savings"])
    spend = float(profile["avg_spend"])
    age = float(profile["avg_age"])
    seniority = float(profile["avg_seniority"])
    if income > 4000 and savings > 20000:
        return "Premium Savers"
    if spend > 1000 and savings < 5000:
        return "Active Spenders"
    if age < 35 and seniority < 5:
        return "Young Professionals"
    if age > 55 and seniority > 15:
        return "Loyal Veterans"
    if income < 2500 and float(profile["avg_credit"]) > 7000:
        return "Credit Dependent"
    if income > 3500:
        return "High-Income Earners"
    if savings > 15000:
        return "Diligent Savers"
    return f"Standard Segment {profile['cluster_id']}"


def generate_kpis(profile: dict[str, str | int | float]) -> list[dict[str, str]]:
    """Identifies top 3 KPIs for a segment."""
    kpis = [
        {
            "name": "Avg. Income",
            "value": f"€{profile['avg_income']}",
            "icon": "wallet",
        },
        {
            "name": "Avg. Savings",
            "value": f"€{profile['avg_savings']}",
            "icon": "piggy-bank",
        },
        {
            "name": "Avg. Spend",
            "value": f"€{profile['avg_spend']}",
            "icon": "shopping-cart",
        },
    ]
    return kpis


def generate_marketing_insights(
    cluster_profiles: list[dict[str, str | int | float]],
) -> list[dict[str, str | int | float | list[dict[str, str]]]]:
    """Analyzes cluster profiles and generates marketing recommendations."""
    insights = []
    for profile in cluster_profiles:
        segment_name = create_segment_name(profile)
        kpis = generate_kpis(profile)
        recommendations = []
        if segment_name == "Premium Savers":
            recommendations.extend(
                [
                    {
                        "icon": "trending-up",
                        "text": "Recommend wealth management services.",
                    },
                    {"icon": "gem", "text": "Promote exclusive investment products."},
                    {
                        "icon": "award",
                        "text": "Offer premium rewards and loyalty programs.",
                    },
                ]
            )
        elif segment_name == "Active Spenders":
            recommendations.extend(
                [
                    {"icon": "save", "text": "Suggest automated savings plans."},
                    {
                        "icon": "credit-card",
                        "text": "Promote high-reward cashback credit cards.",
                    },
                    {
                        "icon": "user-cog",
                        "text": "Offer financial planning consultations.",
                    },
                ]
            )
        elif segment_name == "Young Professionals":
            recommendations.extend(
                [
                    {
                        "icon": "smartphone",
                        "text": "Market advanced digital banking features.",
                    },
                    {
                        "icon": "graduation-cap",
                        "text": "Promote starter and student accounts.",
                    },
                    {
                        "icon": "line-chart",
                        "text": "Offer credit-building loans and products.",
                    },
                ]
            )
        elif segment_name == "Loyal Veterans":
            recommendations.extend(
                [
                    {
                        "icon": "gift",
                        "text": "Provide exclusive loyalty and anniversary rewards.",
                    },
                    {
                        "icon": "home",
                        "text": "Offer retirement planning and estate services.",
                    },
                    {
                        "icon": "headphones",
                        "text": "Ensure access to premium customer service channels.",
                    },
                ]
            )
        elif segment_name == "Credit Dependent":
            recommendations.extend(
                [
                    {
                        "icon": "refresh-cw",
                        "text": "Suggest debt consolidation loan options.",
                    },
                    {
                        "icon": "book-open",
                        "text": "Promote financial literacy workshops.",
                    },
                    {
                        "icon": "clipboard-list",
                        "text": "Offer personalized budget management tools.",
                    },
                ]
            )
        else:
            recommendations.extend(
                [
                    {
                        "icon": "mail",
                        "text": "Send targeted email campaigns for savings products.",
                    },
                    {
                        "icon": "percent",
                        "text": "Offer promotional interest rates on loans.",
                    },
                ]
            )
        total_customers = sum((p["size"] for p in cluster_profiles))
        insights.append(
            {
                "cluster_id": profile["cluster_id"],
                "segment_name": segment_name,
                "size": profile["size"],
                "percentage": profile["size"] / total_customers * 100
                if total_customers > 0
                else 0,
                "kpis": kpis,
                "recommendations": recommendations,
            }
        )
    return insights