import reflex as rx
from app.state import AppState
from app.components.card import metric_card, insight_card
from app.components.charts import pie_chart


def overview_metrics() -> rx.Component:
    return rx.el.div(
        metric_card(
            "Total Customers",
            AppState.kpi_summary.get("total_customers", 0),
            "users",
            "text-blue-500",
        ),
        metric_card(
            "Segments Identified",
            AppState.kpi_summary.get("num_segments", 0),
            "git-branch",
            "text-green-500",
        ),
        metric_card(
            "Avg. Segment Size",
            AppState.kpi_summary.get("avg_segment_size", 0),
            "user-cog",
            "text-orange-500",
        ),
        class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
    )


def insights_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Segment Distribution",
                class_name="text-xl font-semibold text-gray-800 mb-4",
            ),
            pie_chart(
                data=AppState.distribution_pie_data, name_key="name", value_key="value"
            ),
            class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
        ),
        rx.el.div(
            rx.foreach(AppState.insights_data, lambda insight: insight_card(insight)),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8",
        ),
        rx.el.div(
            rx.el.button(
                "Download Full Report",
                on_click=AppState.download_insights_report,
                class_name="mt-8 px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
            ),
            class_name="flex justify-end",
        ),
        class_name="mt-8",
    )


def insights_page() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Marketing Insights Dashboard",
            class_name="text-3xl font-bold text-gray-800 mb-2",
        ),
        rx.el.p(
            "Actionable recommendations for each customer segment.",
            class_name="text-gray-600 mb-8",
        ),
        rx.cond(
            AppState.insights_data.length() > 0,
            rx.el.div(overview_metrics(), insights_dashboard()),
            rx.el.div(
                rx.icon("lightbulb", class_name="w-12 h-12 text-gray-400 mb-4"),
                rx.el.h3(
                    "No Insights Generated",
                    class_name="text-xl font-semibold text-gray-700",
                ),
                rx.el.p(
                    "Please generate customer profiles first to create insights.",
                    class_name="text-gray-500 mt-2",
                ),
                rx.el.button(
                    "Go to Customer Profiles",
                    on_click=rx.redirect("/customer-profiles"),
                    class_name="mt-6 px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                ),
                class_name="text-center p-12 bg-white rounded-xl shadow-sm border border-gray-200",
            ),
        ),
    )