import reflex as rx
from app.state import AppState


def navbar() -> rx.Component:
    """Top navigation bar component."""
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Client-Segment", class_name="text-xl font-bold text-gray-800"),
            rx.el.div(
                rx.el.span("Stage: ", class_name="text-sm font-medium text-gray-500"),
                rx.el.span(
                    AppState.current_stage,
                    class_name="px-2 py-1 text-xs font-semibold text-indigo-700 bg-indigo-100 rounded-md",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name="h-16 px-6 flex items-center bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50",
    )