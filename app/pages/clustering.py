import reflex as rx
from app.state import AppState
from app.components.charts import elbow_chart, colored_scatter_chart, dendrogram_chart
from app.components.card import metric_card


def cluster_selection_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "1. Select Number of Clusters (k)",
            class_name="text-xl font-semibold text-gray-800 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Select k:", class_name="font-medium text-gray-700"),
                rx.el.input(
                    default_value=AppState.num_clusters.to_string(),
                    on_change=AppState.set_num_clusters,
                    type="number",
                    min=2,
                    max=10,
                    class_name="w-20 px-2 py-1 border border-gray-300 rounded-md",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Compute Elbow Method",
                    on_click=AppState.compute_elbow_method,
                    is_loading=AppState.current_stage == "Computing Elbow...",
                    class_name="px-4 py-2 bg-gray-200 text-gray-800 font-semibold rounded-lg shadow-sm hover:bg-gray-300 transition-colors",
                ),
                rx.el.button(
                    f"Run K-Means with k={AppState.num_clusters}",
                    on_click=lambda: AppState.run_clustering(AppState.num_clusters),
                    is_loading=AppState.current_stage == "Clustering...",
                    class_name="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                ),
                class_name="flex gap-4",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.cond(
            AppState.elbow_data.length() > 0,
            elbow_chart(data=AppState.elbow_data),
            rx.el.div(
                rx.icon("chart-line", class_name="w-12 h-12 text-gray-300"),
                rx.el.p(
                    "Click 'Compute Elbow Method' to see optimal k analysis.",
                    class_name="text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center h-96 bg-gray-50 rounded-lg",
            ),
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8",
    )
def hierarchical_clustering_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "2. Hierarchical Clustering",
            class_name="text-xl font-semibold text-gray-800 mb-4",
        ),
        rx.el.div(
            rx.el.button(
                "Run Hierarchical Clustering",
                on_click=AppState.run_hierarchical_clustering,
                is_loading=AppState.current_stage == "Hierarchical Clustering...",
                class_name="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
            ),
            class_name="flex justify-end mt-4",
        ),
        rx.cond(
            AppState.dendrogram_data,
            rx.el.div(
                rx.el.h4(
                    "Dendrogram",
                    class_name="text-lg font-semibold text-gray-800 mb-4",
                ),
                dendrogram_chart(),
                class_name="mt-6",
            ),
            rx.el.div(),
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
    )



def clustering_results() -> rx.Component:
    return rx.cond(
        (AppState.clustered_data.length() > 0) | (AppState.hierarchical_clustered_data.length() > 0),
        rx.el.div(
            rx.el.h3(
                "3. Clustering Results",
                class_name="text-xl font-semibold text-gray-800 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4("K-Means", class_name="font-semibold mb-2"),
                    colored_scatter_chart(
                        data=AppState.cluster_scatter_data, num_clusters=AppState.num_clusters
                    ),
                    class_name="bg-gray-50 p-4 rounded-lg border border-gray-100",
                ),
                rx.el.div(
                    rx.el.h4("Hierarchical", class_name="font-semibold mb-2"),
                    colored_scatter_chart(
                        data=AppState.hierarchical_cluster_scatter_data, num_clusters=AppState.num_clusters
                    ),
                    class_name="bg-gray-50 p-4 rounded-lg border border-gray-100",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
            ),
            rx.el.div(
                rx.el.button(
                    "View Customer Profiles",
                    on_click=AppState.generate_profiles,
                    class_name="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                ),
                class_name="flex justify-end mt-4",
            ),
            class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
        ),
        rx.el.div(),
    )


def comparison_section() -> rx.Component:
    return rx.cond(
        AppState.cluster_comparison_data.length() > 0,
        rx.el.div(
            rx.el.h3(
                "4. Algorithm Comparison",
                class_name="text-xl font-semibold text-gray-800 mb-4",
            ),
            rx.el.div(
                rx.foreach(
                    AppState.cluster_comparison_data,
                    lambda row: rx.el.div(
                        rx.el.div(
                            rx.el.span(row.get("algorithm", row.get("metric", "")), class_name="font-medium text-gray-800"),
                            rx.el.span(
                                rx.cond(
                                    row.get("silhouette") != None,
                                    rx.el.span(f"Silhouette: {row['silhouette']}"),
                                    rx.el.span(f"ARI: {row['value']}")
                                ),
                                class_name="text-gray-600"
                            ),
                            class_name="flex items-center justify-between"
                        ),
                        class_name="px-4 py-2 bg-gray-50 rounded border border-gray-100"
                    ),
                ),
                class_name="space-y-2",
            ),
            class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
        ),
        rx.el.div(),
    )


def clustering_page() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Clustering Analysis", class_name="text-3xl font-bold text-gray-800 mb-2"
        ),
        rx.el.p(
            "Determine the optimal number of clusters and segment customers.",
            class_name="text-gray-600 mb-8",
        ),
        rx.cond(
            AppState.pca_data.length() > 0,
            rx.el.div(
                cluster_selection_card(),
                hierarchical_clustering_card(),
                clustering_results(),
                comparison_section(),
                class_name="space-y-8"
            ),
            rx.el.div(
                rx.icon("git-branch", class_name="w-12 h-12 text-gray-400 mb-4"),
                rx.el.h3(
                    "PCA Data Required",
                    class_name="text-xl font-semibold text-gray-700",
                ),
                rx.el.p(
                    "Please run PCA analysis first to enable clustering.",
                    class_name="text-gray-500 mt-2",
                ),
                rx.el.button(
                    "Go to PCA Analysis",
                    on_click=rx.redirect("/pca-analysis"),
                    class_name="mt-6 px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                ),
                class_name="text-center p-12 bg-white rounded-xl shadow-sm border border-gray-200",
            ),
        ),
    )