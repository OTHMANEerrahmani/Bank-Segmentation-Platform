import reflex as rx
from app.state import AppState
from app.components.card import (
    cluster_profile_card,
    CLUSTER_TEXT_COLORS,
    CLUSTER_BG_COLORS,
    CLUSTER_COLORS,
    CLUSTER_BORDER_COLORS,
)


def profile_filters() -> rx.Component:
    def filter_button(profile: rx.Var[dict]) -> rx.Component:
        cluster_id = profile["cluster_id"].to(int)
        is_active = AppState.selected_cluster_filter == cluster_id
        color = rx.Var.create(CLUSTER_COLORS)[cluster_id]
        text_color = rx.Var.create(CLUSTER_TEXT_COLORS)[cluster_id]
        bg_color = rx.Var.create(CLUSTER_BG_COLORS)[cluster_id]
        border_color = rx.Var.create(CLUSTER_BORDER_COLORS)[cluster_id]
        return rx.el.button(
            rx.el.div(
                class_name=f"w-6 h-6 rounded-full", style={"background_color": color}
            ),
            rx.el.span(
                f"Customer {profile['cluster_id']}",
                class_name="text-lg font-bold text-gray-800 mx-auto",
            ),
            rx.el.span(
                profile["size"],
                class_name=f"text-sm font-semibold px-3 py-1.5 rounded-full {bg_color} {text_color}",
            ),
            on_click=lambda: AppState.filter_by_cluster(cluster_id),
            class_name=rx.cond(
                is_active,
                f"flex items-center w-full text-left p-4 rounded-xl transition-all duration-300 transform shadow-lg {bg_color} border-2 {border_color}",
                "flex items-center w-full text-left p-4 rounded-xl transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm hover:shadow-md",
            ),
            style={"min_height": "70px"},
        )

    return rx.el.div(
        rx.el.h3("Filter Profiles", class_name="text-2xl font-bold text-gray-800 mb-6"),
        rx.el.div(
            rx.el.button(
                rx.el.div(class_name="w-6 h-6 rounded-full bg-gray-400"),
                rx.el.span(
                    "All Segments", class_name="text-lg font-bold text-gray-800 mx-auto"
                ),
                rx.el.span(
                    AppState.total_customers_in_profiles.to_string(),
                    class_name="text-sm font-semibold px-3 py-1.5 rounded-full bg-gray-200 text-gray-700",
                ),
                on_click=lambda: AppState.filter_by_cluster(-1),
                class_name=rx.cond(
                    AppState.selected_cluster_filter == -1,
                    "flex items-center w-full text-left p-4 rounded-xl transition-all duration-300 transform shadow-lg bg-gray-100 border-2 border-gray-400",
                    "flex items-center w-full text-left p-4 rounded-xl transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm hover:shadow-md",
                ),
                style={"min_height": "70px"},
            ),
            rx.foreach(AppState.cluster_profiles, filter_button),
            class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6",
        ),
        class_name="mb-10",
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
                class_name="text-lg text-gray-600 mt-2",
            ),
            class_name="mb-10",
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
                    class_name="grid grid-cols-1 xl:grid-cols-2 gap-10",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("download", class_name="w-5 h-5 mr-2"),
                        "Download Summary",
                        on_click=AppState.download_cluster_summary,
                        class_name="flex items-center px-8 py-4 bg-gray-200 text-gray-800 font-semibold rounded-xl shadow-md hover:bg-gray-300 transition-all text-lg",
                    ),
                    rx.el.button(
                        "Generate Marketing Insights",
                        rx.icon("arrow-right", class_name="w-5 h-5 ml-2"),
                        on_click=AppState.generate_insights,
                        is_loading=AppState.current_stage == "Generating Insights...",
                        class_name="flex items-center px-8 py-4 bg-indigo-600 text-white font-semibold rounded-xl shadow-md hover:bg-indigo-700 transition-all text-lg transform hover:scale-105",
                    ),
                    class_name="flex justify-end items-center gap-6 mt-16",
                ),
            ),
            rx.el.div(
                rx.icon("users", class_name="w-20 h-20 text-gray-300 mb-6"),
                rx.el.h3(
                    "No Profiles Generated",
                    class_name="text-3xl font-semibold text-gray-700",
                ),
                rx.el.p(
                    "Please run clustering to generate customer profiles.",
                    class_name="text-lg text-gray-500 mt-3",
                ),
                rx.el.button(
                    "Go to Clustering",
                    on_click=rx.redirect("/clustering"),
                    class_name="mt-10 px-8 py-4 bg-indigo-600 text-white text-xl font-semibold rounded-xl shadow-lg hover:bg-indigo-700 transition-transform hover:scale-105 duration-300",
                ),
                class_name="flex flex-col items-center justify-center text-center p-24 bg-white rounded-2xl shadow-sm border border-gray-200",
            ),
        ),
    )