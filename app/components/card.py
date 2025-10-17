import reflex as rx
from typing import Union


def metric_card(
    title: str, value: rx.Var[Union[str, int, float]], icon: str, color: str
) -> rx.Component:
    """A reusable card to display a key metric."""
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-8 h-8 {color}"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(
                value.to_string(),
                class_name="text-2xl font-semibold text-gray-800 tracking-tight",
            ),
            class_name="flex-1",
        ),
        class_name="flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow",
    )


CLUSTER_COLORS = ["#6366F1", "#10B981", "#8B5CF6", "#F59E0B"]
CLUSTER_TEXT_COLORS = [
    "text-indigo-600",
    "text-emerald-600",
    "text-violet-600",
    "text-amber-600",
]
CLUSTER_BG_COLORS = ["bg-indigo-100", "bg-emerald-100", "bg-violet-100", "bg-amber-100"]
CLUSTER_BORDER_COLORS = [
    "border-indigo-500",
    "border-emerald-500",
    "border-violet-500",
    "border-amber-500",
]


def profile_metric(
    icon: str, label: str, value: rx.Var, unit: str, color: str
) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name=f"w-6 h-6 {color}"),
        rx.el.div(
            rx.el.p(label, class_name="text-md font-medium text-gray-500"),
            rx.el.div(
                rx.el.p(
                    value.to_string(), class_name="text-xl font-bold text-gray-800"
                ),
                rx.el.span(unit, class_name="text-md text-gray-500 ml-1.5"),
                class_name="flex items-baseline",
            ),
        ),
        class_name="flex items-center gap-4",
    )


def cluster_profile_card(profile: rx.Var[dict[str, str | int | float]]) -> rx.Component:
    cluster_id = profile["cluster_id"].to(int)
    text_color = rx.Var.create(CLUSTER_TEXT_COLORS)[cluster_id]
    bg_color = rx.Var.create(CLUSTER_BG_COLORS)[cluster_id]
    border_color = rx.Var.create(CLUSTER_BORDER_COLORS)[cluster_id]
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                f"Customer {profile['cluster_id']}",
                class_name=f"text-2xl font-bold {text_color}",
            ),
            rx.el.div(
                rx.icon("users", class_name="w-5 h-5"),
                rx.el.p(profile["size"].to_string(), " Customers"),
                class_name=f"flex items-center gap-2 text-md font-semibold px-4 py-2 rounded-full {bg_color} {text_color}",
            ),
            class_name="flex items-center justify-between pb-6 border-b border-gray-100",
        ),
        rx.el.div(
            profile_metric(
                "wallet", "Avg. Income", profile["avg_income"], "€", color=text_color
            ),
            profile_metric(
                "piggy-bank",
                "Avg. Savings",
                profile["avg_savings"],
                "€",
                color=text_color,
            ),
            profile_metric(
                "credit-card",
                "Avg. Credit",
                profile["avg_credit"],
                "€",
                color=text_color,
            ),
            profile_metric(
                "shopping-cart",
                "Avg. Spending",
                profile["avg_spending"],
                "€",
                color=text_color,
            ),
            profile_metric(
                "cake", "Avg. Age", profile["avg_age"], "yrs", color=text_color
            ),
            profile_metric(
                "shield-check",
                "Avg. Seniority",
                profile["avg_seniority"],
                "yrs",
                color=text_color,
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-10 pt-8",
        ),
        class_name=f"bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border-l-[10px] p-8 overflow-hidden {border_color}",
    )


def insight_card(
    insight: rx.Var[dict[str, str | int | float | list[dict[str, str]]]],
) -> rx.Component:
    cluster_id = insight["cluster_id"]
    color_class = rx.Var.create(CLUSTER_TEXT_COLORS)[
        cluster_id.to(int) % len(CLUSTER_TEXT_COLORS)
    ]
    border_class = rx.Var.create(CLUSTER_BORDER_COLORS)[
        cluster_id.to(int) % len(CLUSTER_BORDER_COLORS)
    ]

    def recommendation_item(rec: rx.Var[dict[str, str]]) -> rx.Component:
        return rx.el.div(
            rx.icon(rec["icon"], class_name=f"w-5 h-5 {color_class} mr-3"),
            rx.el.p(rec["text"], class_name="text-sm text-gray-700"),
            class_name="flex items-center",
        )

    def kpi_item(kpi: rx.Var[dict[str, str]]) -> rx.Component:
        return rx.el.div(
            rx.icon(kpi["icon"], class_name="w-4 h-4 text-gray-400"),
            rx.el.span(f"{kpi['name']}:", class_name="text-sm text-gray-500"),
            rx.el.span(kpi["value"], class_name="text-sm font-semibold text-gray-800"),
            class_name="flex items-center gap-2 bg-gray-50 px-2 py-1 rounded-md",
        )

    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                insight["segment_name"], class_name=f"text-xl font-bold {color_class}"
            ),
            rx.el.div(
                rx.el.p(f"{insight['size']} Customers ({insight['percentage']:.1f}%) "),
                class_name="text-sm font-medium text-gray-600",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.div(
            rx.el.h4("Top KPIs", class_name="text-md font-semibold text-gray-700 mb-2"),
            rx.el.div(
                rx.foreach(insight["kpis"].to(list[dict[str, str]]), kpi_item),
                class_name="flex flex-wrap gap-2 mb-4",
            ),
            rx.el.h4(
                "Marketing Recommendations",
                class_name="text-md font-semibold text-gray-700 mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    insight["recommendations"].to(list[dict[str, str]]),
                    recommendation_item,
                ),
                class_name="space-y-2",
            ),
            class_name="mt-4",
        ),
        class_name=f"p-6 bg-white rounded-xl shadow-sm hover:shadow-lg transition-all {border_class} border-l-4",
    )