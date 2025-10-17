import reflex as rx
from app.state import AppState
from app.components.navbar import navbar
from app.pages.home import home_page
from app.pages.data_cleaning import data_cleaning_page
from app.pages.pca_analysis import pca_analysis_page
from app.pages.clustering import clustering_page
from app.pages.customer_profiles import customer_profiles_page
from app.pages.insights import insights_page


def sidebar_link(text: str, href: str, icon: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-5 h-5"),
            rx.el.span(text),
            class_name="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 font-medium transition-colors",
        ),
        href=href,
        class_name=rx.cond(AppState.router.page.path == str(href), "bg-gray-100", ""),
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("bar-chart-3", class_name="w-8 h-8 text-indigo-600"),
            class_name="p-4 mb-4",
        ),
        rx.el.div(
            sidebar_link("Home", "/", "home"),
            sidebar_link("Data Cleaning", "/data-cleaning", "database"),
            sidebar_link("PCA Analysis", "/pca-analysis", "bar-chart-2"),
            sidebar_link("Clustering", "/clustering", "git-branch"),
            sidebar_link("Customer Profiles", "/customer-profiles", "users"),
            sidebar_link("Insights", "/insights", "lightbulb"),
            class_name="flex flex-col gap-1 p-2",
        ),
        class_name="w-64 h-full bg-white border-r border-gray-200 fixed top-0 left-0",
    )


def template(page: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(page, class_name="p-4 sm:p-6 lg:p-8"),
            class_name="ml-64",
        ),
        class_name="font-['Lora'] bg-gray-50 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(template(home_page()), route="/")
app.add_page(template(data_cleaning_page()), route="/data-cleaning")
app.add_page(template(pca_analysis_page()), route="/pca-analysis")
app.add_page(template(clustering_page()), route="/clustering")
app.add_page(template(customer_profiles_page()), route="/customer-profiles")
app.add_page(template(insights_page()), route="/insights")