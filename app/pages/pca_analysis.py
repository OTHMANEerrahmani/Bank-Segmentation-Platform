import reflex as rx
from app.state import AppState
from app.components.charts import variance_chart, scatter_chart
from app.components.datatable import data_table


def pca_analysis_page() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "PCA Analysis Results", class_name="text-3xl font-bold text-gray-800 mb-2"
        ),
        rx.el.p(
            "Principal Component Analysis has been performed to reduce dimensionality.",
            class_name="text-gray-600 mb-8",
        ),
        rx.cond(
            AppState.pca_data.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Explained Variance per Component",
                            class_name="text-xl font-semibold text-gray-800 mb-4",
                        ),
                        variance_chart(data=AppState.pca_variance_data),
                        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 lg:col-span-2",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Customer Distribution (PC1 vs PC2)",
                            class_name="text-xl font-semibold text-gray-800 mb-4",
                        ),
                        scatter_chart(
                            data=AppState.pca_scatter_data, x_key="PC1", y_key="PC2"
                        ),
                        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 lg:col-span-1",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Component Contributions",
                        class_name="text-xl font-semibold text-gray-800 mb-4",
                    ),
                    rx.el.p(
                        "This table shows how original features contribute to the principal components.",
                        class_name="text-sm text-gray-500 mb-4",
                    ),
                    data_table(
                        data=AppState.pca_components_data,
                        columns=AppState.pca_components_columns,
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8",
                ),
                rx.el.div(
                    rx.el.button(
                        "Go to Clustering",
                        rx.icon("arrow-right", class_name="ml-2 w-4 h-4"),
                        on_click=rx.redirect("/clustering"),
                        class_name="flex items-center px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex justify-end",
                ),
                class_name="space-y-8",
            ),
            rx.el.div(
                rx.icon("bar-chart-2", class_name="w-12 h-12 text-gray-400 mb-4"),
                rx.el.h3(
                    "No PCA Data", class_name="text-xl font-semibold text-gray-700"
                ),
                rx.el.p(
                    "Please run the PCA analysis from the Data Cleaning page first.",
                    class_name="text-gray-500 mt-2",
                ),
                rx.el.button(
                    "Go to Data Cleaning",
                    on_click=rx.redirect("/data-cleaning"),
                    class_name="mt-6 px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                ),
                class_name="text-center p-12 bg-white rounded-xl shadow-sm border border-gray-200",
            ),
        ),
    )