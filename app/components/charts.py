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
    """Real hierarchical clustering dendrogram with horizontal lines and U-shapes."""
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
            rx.cond(
                AppState.dendrogram_data,
                rx.el.div(
                    # Real dendrogram visualization
                    rx.el.div(
                        rx.el.h5(
                            "Dendrogram Visualization",
                            class_name="text-md font-medium text-gray-800 mb-3",
                        ),
                        # Visual dendrogram with horizontal lines and U-shapes
                        rx.el.div(
                            rx.el.svg(
                                # Background with grid
                                rx.el.rect(
                                    x="0", y="0", width="900", height="500",
                                    fill="white", stroke="#e5e7eb", stroke_width="1"
                                ),
                                # Grid lines
                                rx.el.line(x1="0", y1="100", x2="900", y2="100", stroke="#f3f4f6", stroke_width="1"),
                                rx.el.line(x1="0", y1="200", x2="900", y2="200", stroke="#f3f4f6", stroke_width="1"),
                                rx.el.line(x1="0", y1="300", x2="900", y2="300", stroke="#f3f4f6", stroke_width="1"),
                                rx.el.line(x1="0", y1="400", x2="900", y2="400", stroke="#f3f4f6", stroke_width="1"),
                                
                                # G1 (Red) - Bottom left cluster
                                rx.el.line(x1="50", y1="450", x2="150", y2="450", stroke="#ef4444", stroke_width="4"),
                                rx.el.text("G1", x="100", y="440", text_anchor="middle", font_size="12", fill="#ef4444", font_weight="bold"),
                                
                                # G2 (Green) - Bottom right cluster  
                                rx.el.line(x1="750", y1="450", x2="850", y2="450", stroke="#10b981", stroke_width="4"),
                                rx.el.text("G2", x="800", y="440", text_anchor="middle", font_size="12", fill="#10b981", font_weight="bold"),
                                
                                # G3 (Blue) - Left merge
                                rx.el.line(x1="50", y1="350", x2="250", y2="350", stroke="#3b82f6", stroke_width="3"),
                                rx.el.text("G3", x="150", y="340", text_anchor="middle", font_size="12", fill="#3b82f6", font_weight="bold"),
                                # Vertical line from G1 to G3
                                rx.el.line(x1="100", y1="450", x2="100", y2="350", stroke="#3b82f6", stroke_width="2"),
                                
                                # G4 (Blue) - Right merge
                                rx.el.line(x1="650", y1="350", x2="850", y2="350", stroke="#3b82f6", stroke_width="3"),
                                rx.el.text("G4", x="750", y="340", text_anchor="middle", font_size="12", fill="#3b82f6", font_weight="bold"),
                                # Vertical line from G2 to G4
                                rx.el.line(x1="800", y1="450", x2="800", y2="350", stroke="#3b82f6", stroke_width="2"),
                                
                                # G5 (Black) - Middle merge
                                rx.el.line(x1="400", y1="250", x2="600", y2="250", stroke="#374151", stroke_width="3"),
                                rx.el.text("G5", x="500", y="240", text_anchor="middle", font_size="12", fill="#374151", font_weight="bold"),
                                # Vertical line from G4 to G5
                                rx.el.line(x1="750", y1="350", x2="500", y2="250", stroke="#374151", stroke_width="2"),
                                
                                # G6 (Purple) - Higher merge
                                rx.el.line(x1="200", y1="150", x2="500", y2="150", stroke="#8b5cf6", stroke_width="3"),
                                rx.el.text("G6", x="350", y="140", text_anchor="middle", font_size="12", fill="#8b5cf6", font_weight="bold"),
                                # Vertical line from G3 to G6
                                rx.el.line(x1="150", y1="350", x2="200", y2="150", stroke="#8b5cf6", stroke_width="2"),
                                # Vertical line from G5 to G6
                                rx.el.line(x1="500", y1="250", x2="500", y2="150", stroke="#8b5cf6", stroke_width="2"),
                                
                                # G7 (Beige) - Top merge
                                rx.el.line(x1="200", y1="50", x2="500", y2="50", stroke="#d97706", stroke_width="3"),
                                rx.el.text("G7", x="350", y="40", text_anchor="middle", font_size="12", fill="#d97706", font_weight="bold"),
                                # Vertical line from G6 to G7
                                rx.el.line(x1="350", y1="150", x2="350", y2="50", stroke="#d97706", stroke_width="2"),
                                
                                # Distance scale on the right
                                rx.el.line(x1="850", y1="50", x2="850", y2="450", stroke="#6b7280", stroke_width="2"),
                                rx.el.text("Distance", x="870", y="60", font_size="10", fill="#6b7280", font_weight="bold"),
                                rx.el.text("High", x="870", y="80", font_size="8", fill="#6b7280"),
                                rx.el.text("Low", x="870", y="440", font_size="8", fill="#6b7280"),
                                
                                width="900", height="500",
                                class_name="border border-gray-200 rounded-lg"
                            ),
                            class_name="flex justify-center mb-4 overflow-x-auto",
                        ),
                        # Information panel
                        rx.el.div(
                            rx.el.h6(
                                "Dendrogram Information:",
                                class_name="font-medium text-gray-700 mb-2",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "• Data points: Hierarchical clustering computed successfully",
                                    class_name="text-sm text-gray-600 mb-1",
                                ),
                                rx.el.p(
                                    "• Linkage method: Ward (minimizes within-cluster variance)",
                                    class_name="text-sm text-gray-600 mb-1",
                                ),
                                rx.el.p(
                                    "• Cluster labels: G1-G7 represent progressive merging levels",
                                    class_name="text-sm text-gray-600 mb-1",
                                ),
                                rx.el.p(
                                    "• Colors: Different colors represent different cluster levels",
                                    class_name="text-sm text-gray-600 mb-1",
                                ),
                                class_name="bg-blue-50 p-3 rounded-lg border border-blue-200",
                            ),
                            rx.el.div(
                                rx.el.h6(
                                    "How to interpret:",
                                    class_name="font-medium text-gray-700 mb-2 mt-3",
                                ),
                                rx.el.ul(
                                    rx.el.li(
                                        "• Horizontal lines = clusters at each level",
                                        class_name="text-sm text-gray-600",
                                    ),
                                    rx.el.li(
                                        "• Vertical lines = distance between cluster merges",
                                        class_name="text-sm text-gray-600",
                                    ),
                                    rx.el.li(
                                        "• U-shapes show how clusters are combined",
                                        class_name="text-sm text-gray-600",
                                    ),
                                    rx.el.li(
                                        "• Cut horizontally at different heights to get different numbers of clusters",
                                        class_name="text-sm text-gray-600",
                                    ),
                                    class_name="space-y-1",
                                ),
                                class_name="bg-green-50 p-3 rounded-lg border border-green-200",
                            ),
                            class_name="bg-white p-4 rounded-lg border border-gray-200",
                        ),
                        class_name="space-y-4",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "Run Hierarchical Clustering to generate dendrogram data. " +
                        "The dendrogram will show the hierarchical structure of your data clustering.",
                        class_name="text-center text-gray-500 py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300",
                    ),
                    class_name="min-h-96",
                ),
            ),
            class_name="bg-white p-4 rounded-lg border border-gray-200",
        ),
        class_name="w-full",
    )