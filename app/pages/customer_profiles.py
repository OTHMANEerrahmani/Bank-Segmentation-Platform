import reflex as rx
from app.state import AppState
from app.components.card import cluster_profile_card
from app.components.charts import radar_chart


def profile_filters() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Filter Profiles", class_name="text-lg font-semibold text-gray-800"),
        rx.el.div(
            rx.el.button(
                "All Clusters",
                on_click=lambda: AppState.filter_by_cluster(-1),
                class_name=rx.cond(
                    AppState.selected_cluster_filter == -1,
                    "bg-indigo-600 text-white",
                    "bg-white text-gray-700 hover:bg-gray-100",
                ),
                size="2",
            ),
            rx.foreach(
                AppState.cluster_profiles,
                lambda profile: rx.el.button(
                    f"Cluster {profile['cluster_id']}",
                    on_click=lambda: AppState.filter_by_cluster(profile["cluster_id"]),
                    class_name=rx.cond(
                        AppState.selected_cluster_filter == profile["cluster_id"],
                        "bg-indigo-600 text-white",
                        "bg-white text-gray-700 hover:bg-gray-100",
                    ),
                    size="2",
                ),
            ),
            class_name="flex flex-wrap gap-2",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex items-center justify-between",
    )


def customer_profiles_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Customer Segment Profiles",
                class_name="text-3xl font-bold text-gray-800",
            ),
            rx.el.p(
                "Detailed breakdown of each customer segment based on their characteristics.",
                class_name="text-gray-600",
            ),
            class_name="mb-8",
        ),
        rx.cond(
            AppState.cluster_profiles.length() > 0,
            rx.el.div(
                profile_filters(),
                rx.el.div(
                    rx.foreach(
                        AppState.filtered_cluster_profiles,
                        lambda profile: cluster_profile_card(profile),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mt-8",
                ),
                rx.el.div(
                    rx.el.button(
                        "Download Summary",
                        on_click=AppState.download_cluster_summary,
                        class_name="flex items-center px-4 py-2 bg-gray-200 text-gray-800 font-semibold rounded-lg shadow-sm hover:bg-gray-300 transition-colors",
                    ),
                    rx.el.button(
                        "Generate Marketing Insights",
                        on_click=AppState.generate_insights,
                        is_loading=AppState.current_stage == "Generating Insights...",
                        class_name="flex items-center px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex justify-end gap-4 mt-8",
                ),
            ),
            rx.el.div(
                rx.icon("users", class_name="w-12 h-12 text-gray-400 mb-4"),
                rx.el.h3(
                    "No Profiles Generated",
                    class_name="text-xl font-semibold text-gray-700",
                ),
                rx.el.p(
                    "Please run clustering to generate customer profiles.",
                    class_name="text-gray-500 mt-2",
                ),
                rx.el.button(
                    "Go to Clustering",
                    on_click=rx.redirect("/clustering"),
                    class_name="mt-6 px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                ),
                class_name="text-center p-12 bg-white rounded-xl shadow-sm border border-gray-200",
            ),
        ),
    )