import reflex as rx
from app.state import AppState
from app.components.card import CLUSTER_COLORS

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "border_color": "#E4E4E7",
        "border_radius": "0.5rem",
        "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    },
    "label_style": {"color": "#18181B", "font_weight": "500"},
}


def variance_chart(data: rx.Var[list[dict]]) -> rx.Component:
    return rx.recharts.composed_chart(
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3", horizontal=True, vertical=False
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.x_axis(data_key="component", tick_line=False, axis_line=False),
        rx.recharts.y_axis(
            y_axis_id="left",
            orientation="left",
            label={
                "value": "Variance (%)",
                "angle": -90,
                "position": "insideLeft",
                "style": {"textAnchor": "middle"},
            },
            tick_line=False,
            axis_line=False,
        ),
        rx.recharts.y_axis(
            y_axis_id="right",
            orientation="right",
            label={
                "value": "Cumulative (%)",
                "angle": 90,
                "position": "insideRight",
                "style": {"textAnchor": "middle"},
            },
            tick_line=False,
            axis_line=False,
        ),
        rx.recharts.legend(),
        rx.recharts.bar(
            data_key="variance",
            y_axis_id="left",
            fill="#8884d8",
            name="Individual Variance",
        ),
        rx.recharts.line(
            data_key="cumulative",
            y_axis_id="right",
            stroke="#82ca9d",
            type_="monotone",
            name="Cumulative Variance",
        ),
        data=data,
        height=400,
        width="100%",
        margin={"top": 20, "right": 30, "left": 20, "bottom": 5},
    )


def scatter_chart(data: rx.Var[list[dict]], x_key: str, y_key: str) -> rx.Component:
    return rx.recharts.scatter_chart(
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
        rx.recharts.graphing_tooltip(
            **TOOLTIP_PROPS, cursor={"stroke_dasharray": "3 3"}
        ),
        rx.recharts.x_axis(
            type_="number", data_key=x_key, name="PC1", tick_line=False, axis_line=False
        ),
        rx.recharts.y_axis(
            type_="number", data_key=y_key, name="PC2", tick_line=False, axis_line=False
        ),
        rx.recharts.scatter(name="Customers", data=data, fill="#6366F1"),
        height=400,
        width="100%",
        margin={"top": 20, "right": 20, "bottom": 20, "left": 20},
    )


def elbow_chart(data: rx.Var[list[dict]]) -> rx.Component:
    return rx.recharts.composed_chart(
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.x_axis(data_key="k", name="Clusters (k)"),
        rx.recharts.y_axis(y_axis_id="left", orientation="left", name="Inertia"),
        rx.recharts.y_axis(y_axis_id="right", orientation="right", name="Silhouette"),
        rx.recharts.legend(),
        rx.recharts.bar(
            data_key="inertia", y_axis_id="left", name="Inertia", fill="#8884d8"
        ),
        rx.recharts.line(
            data_key="silhouette",
            y_axis_id="right",
            name="Silhouette Score",
            stroke="#82ca9d",
        ),
        data=data,
        height=400,
        width="100%",
    )


def pie_chart(data: rx.Var[list[dict]], name_key: str, value_key: str) -> rx.Component:
    return rx.recharts.pie_chart(
        rx.recharts.graphing_tooltip(
            **TOOLTIP_PROPS, formatter="(value) => `${value.toFixed(1)}%`"
        ),
        rx.recharts.pie(
            rx.foreach(
                data,
                lambda item, i: rx.recharts.cell(
                    fill=rx.Var.create(CLUSTER_COLORS)[i % len(CLUSTER_COLORS)]
                ),
            ),
            data=data,
            data_key=value_key,
            name_key=name_key,
            cx="50%",
            cy="50%",
            outer_radius=120,
            label_line=False,
        ),
        rx.recharts.legend(),
        height=400,
        width="100%",
    )


def colored_scatter_chart(
    data: rx.Var[dict[int, list[dict]]], num_clusters: rx.Var[int]
) -> rx.Component:
    color_map = rx.Var.create(CLUSTER_COLORS)
    return rx.recharts.scatter_chart(
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.x_axis(
            type_="number", data_key="PC1", name="Principal Component 1"
        ),
        rx.recharts.y_axis(
            type_="number", data_key="PC2", name="Principal Component 2"
        ),
        rx.recharts.legend(),
        rx.foreach(
            data.keys(),
            lambda i: rx.recharts.scatter(
                name=f"Customer {i}",
                data=data[i],
                fill=color_map[i.to(int) % len(CLUSTER_COLORS)],
            ),
        ),
        height=500,
        width="100%",
    )


def radar_chart(data: rx.Var[list[dict]]) -> rx.Component:
    cluster_colors_var = rx.Var.create(CLUSTER_COLORS)
    return rx.recharts.radar_chart(
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.polar_grid(),
        rx.recharts.polar_angle_axis(data_key="metric"),
        rx.recharts.legend(),
        rx.foreach(
            AppState.cluster_profiles,
            lambda profile, i: rx.recharts.radar(
                name=f"Customer {profile['cluster_id']}",
                data_key=f"c{profile['cluster_id']}",
                stroke=cluster_colors_var[i % len(cluster_colors_var)],
                fill=cluster_colors_var[i % len(cluster_colors_var)],
                fill_opacity=0.6,
            ),
        ),
        data=data,
        height=400,
        width="100%",
    )


def dendrogram_chart() -> rx.Component:
    """Custom dendrogram visualization using SVG."""
    return rx.el.div(
        rx.el.h4(
            "Hierarchical Clustering Dendrogram",
            class_name="text-lg font-semibold text-gray-800 mb-4",
        ),
        rx.el.div(
            rx.el.p(
                "Dendrogram shows the hierarchical clustering structure. " +
                "The height of branches indicates the distance between clusters. " +
                "Use this to understand how data points are grouped together.",
                class_name="text-sm text-gray-600 mb-4",
            ),
            rx.el.div(
                rx.el.p(
                    "Dendrogram visualization will be displayed here. " +
                    "The dendrogram shows the hierarchical structure of your data clustering.",
                    class_name="text-center text-gray-500 py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300",
                ),
                class_name="min-h-96",
            ),
            class_name="bg-white p-4 rounded-lg border border-gray-200",
        ),
        class_name="w-full",
    )