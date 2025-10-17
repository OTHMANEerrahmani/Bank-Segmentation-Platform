import reflex as rx
from app.state import AppState
import pandas as pd


def data_table(data: rx.Var[list[dict]], columns: rx.Var[list[str]]) -> rx.Component:
    """Data table component for displaying dataframes."""
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.foreach(
                        columns,
                        lambda col: rx.el.th(
                            col,
                            class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600 bg-gray-50",
                        ),
                    )
                )
            ),
            rx.el.tbody(
                rx.cond(
                    data.length() > 0,
                    rx.foreach(
                        data,
                        lambda row, index: rx.el.tr(
                            rx.foreach(
                                columns,
                                lambda col: rx.el.td(
                                    row[col].to_string(),
                                    class_name="px-4 py-2 text-sm text-gray-700",
                                ),
                            ),
                            class_name="border-t border-gray-200 hover:bg-gray-50",
                        ),
                    ),
                    rx.el.tr(
                        rx.el.td(
                            "No data available.",
                            col_span=columns.length(),
                            class_name="text-center py-10 text-gray-500",
                        )
                    ),
                )
            ),
            class_name="w-full",
        ),
        class_name="overflow-x-auto bg-white border border-gray-200 rounded-xl shadow-sm",
    )