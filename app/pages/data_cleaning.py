import reflex as rx
from app.state import AppState
from app.components.card import metric_card
from app.components.datatable import data_table


def data_cleaning_page() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Data Cleaning Results", class_name="text-3xl font-bold text-gray-800 mb-2"
        ),
        rx.el.p(
            "The raw data has been processed. Here is a summary of the cleaning operations.",
            class_name="text-gray-600 mb-8",
        ),
        rx.cond(
            AppState.cleaned_data.length() > 0,
            rx.el.div(
                rx.el.div(
                    metric_card(
                        "Total Rows",
                        AppState.cleaning_summary["total_rows"],
                        "align-justify",
                        "text-blue-500",
                    ),
                    metric_card(
                        "Missing Values Handled",
                        AppState.cleaning_summary["missing_values"],
                        "trash-2",
                        "text-orange-500",
                    ),
                    metric_card(
                        "Outliers Corrected",
                        AppState.cleaning_summary["outliers_detected"],
                        "trending-down",
                        "text-red-500",
                    ),
                    metric_card(
                        "Duplicates Removed",
                        AppState.cleaning_summary["duplicates_removed"],
                        "copy-x",
                        "text-purple-500",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Cleaning Log",
                        class_name="text-xl font-semibold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            AppState.cleaning_log,
                            lambda log: rx.el.div(
                                rx.icon(
                                    "square_check",
                                    class_name="w-5 h-5 text-green-500 mr-3",
                                ),
                                rx.el.p(log, class_name="text-sm text-gray-700"),
                                class_name="flex items-center p-3 bg-gray-50 rounded-lg mb-2",
                            ),
                        ),
                        class_name="p-4 border border-gray-200 rounded-xl max-h-96 overflow-y-auto mb-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("download", class_name="w-4 h-4 mr-2"),
                            "Download Log",
                            on_click=AppState.download_cleaning_log,
                            class_name="flex items-center px-4 py-2 bg-gray-200 text-gray-800 font-semibold rounded-lg shadow-sm hover:bg-gray-300 transition-colors",
                        ),
                        rx.el.button(
                            "Run PCA Analysis",
                            rx.icon("arrow-right", class_name="w-4 h-4 ml-2"),
                            on_click=AppState.run_pca,
                            is_loading=AppState.current_stage == "PCA Analysis...",
                            class_name="flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-4",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8",
                ),
                rx.el.h3(
                    "Cleaned Data Preview (First 100 Rows)",
                    class_name="text-xl font-semibold text-gray-800 mb-4",
                ),
                data_table(
                    data=AppState.cleaned_data[:100],
                    columns=AppState.cleaned_data_columns,
                ),
                class_name="space-y-8",
            ),
            rx.el.div(
                rx.icon("info", class_name="w-12 h-12 text-gray-400 mb-4"),
                rx.el.h3(
                    "No Cleaned Data", class_name="text-xl font-semibold text-gray-700"
                ),
                rx.el.p(
                    "Please upload a file and run the cleaning pipeline from the Home page first.",
                    class_name="text-gray-500 mt-2",
                ),
                rx.el.button(
                    "Go to Home",
                    on_click=rx.redirect("/"),
                    class_name="mt-6 px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                ),
                class_name="text-center p-12 bg-white rounded-xl shadow-sm border border-gray-200",
            ),
        ),
    )