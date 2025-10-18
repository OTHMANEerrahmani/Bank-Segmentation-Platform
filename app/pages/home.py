import reflex as rx
from app.state import AppState
from app.components.datatable import data_table


def upload_area() -> rx.Component:
    return rx.upload.root(
        rx.el.div(
            rx.el.div(
                rx.icon("cloud_upload", class_name="w-12 h-12 text-gray-400"),
                rx.el.h3(
                    "Upload CSV File",
                    class_name="mt-4 text-lg font-semibold text-gray-800",
                ),
                rx.el.p(
                    "Drag and drop or click to select a file.",
                    class_name="mt-1 text-sm text-gray-500",
                ),
                rx.el.p("Max file size: 5MB", class_name="text-xs text-gray-400 mt-2"),
                class_name="text-center",
            ),
            class_name="flex items-center justify-center w-full h-64 p-6 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors",
        ),
        id="upload_csv",
        on_drop=AppState.handle_upload(rx.upload_files(upload_id="upload_csv")),
        border="none",
        padding="0",
        background="transparent",
    )


def home_page() -> rx.Component:
    """Landing page with file upload."""
    return rx.el.div(
        rx.el.h2(
            "1. Upload Customer Data",
            class_name="text-2xl font-bold text-gray-800 mb-2",
        ),
        rx.el.p(
            "Begin by uploading your bank customer dataset in CSV format.",
            class_name="text-gray-600 mb-6",
        ),
        rx.el.div(
            rx.cond(
                AppState.is_uploading,
                rx.el.div(
                    rx.spinner(class_name="w-12 h-12 text-indigo-500"),
                    rx.el.p("Processing file...", class_name="mt-4 text-gray-600"),
                    class_name="flex flex-col items-center justify-center w-full h-64 bg-gray-50 rounded-xl",
                ),
                rx.cond(
                    AppState.raw_data.length() > 0,
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "file-check-2", class_name="w-8 h-8 text-green-500"
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "File Uploaded:",
                                    class_name="font-semibold text-gray-800",
                                ),
                                rx.el.p(
                                    AppState.uploaded_filename,
                                    class_name="text-sm text-gray-600 truncate",
                                ),
                                class_name="flex-1",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    "Load New File",
                                    on_click=AppState.reset_application,
                                    class_name="px-3 py-2 bg-gray-600 text-white font-medium rounded-lg shadow-sm hover:bg-gray-700 transition-colors text-sm mr-2",
                                ),
                                rx.el.button(
                                    "Start Cleaning",
                                    on_click=AppState.run_cleaning,
                                    class_name="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 transition-colors",
                                ),
                                class_name="flex items-center gap-2",
                            ),
                            class_name="flex items-center gap-4 w-full p-4 bg-green-50 border border-green-200 rounded-xl mb-4",
                        ),
                        data_table(
                            data=AppState.raw_data, columns=AppState.raw_data_columns
                        ),
                        class_name="w-full",
                    ),
                    upload_area(),
                ),
            ),
            class_name="w-full max-w-4xl mx-auto",
        ),
        class_name="p-8",
    )