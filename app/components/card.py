import reflex as rx
from typing import Union, Any


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


CLUSTER_COLORS = [
    "text-indigo-500",
    "text-emerald-500",
    "text-rose-500",
    "text-amber-500",
    "text-purple-500",
    "text-cyan-500",
    "text-pink-500",
    "text-lime-500",
    "text-sky-500",
]
CLUSTER_BG_COLORS = [
    "bg-indigo-50",
    "bg-emerald-50",
    "bg-rose-50",
    "bg-amber-50",
    "bg-purple-50",
    "bg-cyan-50",
    "bg-pink-50",
    "bg-lime-50",
    "bg-sky-50",
]
CLUSTER_BORDER_COLORS = [
    "border-indigo-200",
    "border-emerald-200",
    "border-rose-200",
    "border-amber-200",
    "border-purple-200",
    "border-cyan-200",
    "border-pink-200",
    "border-lime-200",
    "border-sky-200",
]


def profile_metric(icon: str, label: str, value: rx.Var, unit: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="w-4 h-4 text-gray-400"),
        rx.el.span(f"{label}: ", class_name="text-sm text-gray-500"),
        rx.el.span(value.to_string(), class_name="text-sm font-semibold text-gray-800"),
        rx.el.span(unit, class_name="text-sm text-gray-500 ml-1"),
        class_name="flex items-center gap-2",
    )


def cluster_profile_card(profile: rx.Var[dict[str, str | int | float]]) -> rx.Component:
    cluster_id = profile["cluster_id"]
    color_class = rx.Var.create(CLUSTER_COLORS)[
        cluster_id.to(int) % len(CLUSTER_COLORS)
    ]
    bg_class = rx.Var.create(CLUSTER_BG_COLORS)[
        cluster_id.to(int) % len(CLUSTER_BG_COLORS)
    ]
    border_class = rx.Var.create(CLUSTER_BORDER_COLORS)[
        cluster_id.to(int) % len(CLUSTER_BORDER_COLORS)
    ]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    f"Cluster {cluster_id.to_string()}",
                    class_name="text-lg font-bold",
                    color=color_class,
                ),
                rx.el.div(
                    rx.icon("users", class_name="w-4 h-4"),
                    rx.el.p(f"{profile['size']} Customers"),
                    class_name="flex items-center gap-2 text-sm font-medium text-gray-600",
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.div(
                profile_metric("wallet", "Income", profile["avg_income"], "€"),
                profile_metric("piggy-bank", "Savings", profile["avg_savings"], "€"),
                profile_metric("credit-card", "Credit", profile["avg_credit"], "€"),
                profile_metric(
                    "shopping-cart", "Spending", profile["avg_spending"], "€"
                ),
                profile_metric("cake", "Age", profile["avg_age"], "yrs"),
                profile_metric("shield", "Seniority", profile["avg_seniority"], "yrs"),
                class_name="grid grid-cols-2 gap-x-4 gap-y-3 mt-4",
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-xl shadow-sm hover:shadow-lg transition-all border",
        border_color=border_class,
    )


def insight_card(
    insight: rx.Var[dict[str, str | int | float | list[dict[str, str]]]],
) -> rx.Component:
    cluster_id = insight["cluster_id"]
    color_class = rx.Var.create(CLUSTER_COLORS)[
        cluster_id.to(int) % len(CLUSTER_COLORS)
    ]
    border_class = rx.Var.create(CLUSTER_BORDER_COLORS)[
        cluster_id.to(int) % len(CLUSTER_BORDER_COLORS)
    ]

    def recommendation_item(rec: rx.Var[dict[str, str]]) -> rx.Component:
        return rx.el.div(
            rx.icon(rec["icon"], class_name=f"w-5 h-5 {color_class.to(str)} mr-3"),
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
                insight["segment_name"],
                class_name="text-xl font-bold",
                color=color_class,
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
        class_name="p-6 bg-white rounded-xl shadow-sm hover:shadow-lg transition-all border",
        border_color=border_class,
    )