import reflex as rx
from typing import Any
import pandas as pd
import io
import logging
import numpy as np
from app.utils.cleaning_pipeline import clean_data
from app.utils.pca_utils import perform_pca
from app.utils.clustering_utils import (
    compute_elbow_data,
    perform_clustering,
    generate_cluster_profiles,
)
from app.utils.insights_utils import generate_marketing_insights


class AppState(rx.State):
    """Global app logic and state management."""

    raw_data: list[dict[str, str | int | float]] = []
    raw_data_columns: list[str] = []
    cleaned_data: list[dict[str, str | int | float]] = []
    cleaned_data_columns: list[str] = []
    pca_data: list[dict[str, str | int | float]] = []
    clustered_data: list[dict[str, str | int | float]] = []
    profiles: list[dict[str, str | int | float]] = []
    insights_data: list[dict[str, str | int | float | list[dict[str, str]]]] = []
    distribution_pie_data: list[dict[str, str | int | float]] = []
    kpi_summary: dict[str, str | int | float] = {}
    selected_insight_cluster: int = -1
    cleaning_log: list[str] = []
    current_stage: str = "Upload"
    uploaded_files: list[str] = []
    num_clusters: int = 3
    is_uploading: bool = False
    cleaning_summary: dict[str, int] = {
        "total_rows": 0,
        "missing_values": 0,
        "outliers_detected": 0,
        "duplicates_removed": 0,
    }
    pca_results: dict[str, list[float]] = {}
    pca_variance_data: list[dict[str, str | float]] = []
    pca_scatter_data: list[dict[str, float]] = []
    pca_components_data: list[dict[str, str | float]] = []
    elbow_data: list[dict[str, float]] = []
    cluster_scatter_data: dict[int, list[dict[str, str | int | float]]] = {}
    cluster_profiles: list[dict[str, str | int | float]] = []
    selected_cluster_filter: int = -1
    cluster_comparison_data: list[dict[str, str | int | float]] = []

    @rx.var
    def filtered_cluster_profiles(self) -> list[dict[str, str | int | float]]:
        """Return cluster profiles based on the selected filter."""
        if self.selected_cluster_filter == -1:
            return self.cluster_profiles
        return [
            p
            for p in self.cluster_profiles
            if p["cluster_id"] == self.selected_cluster_filter
        ]

    @rx.var
    def pca_components_columns(self) -> list[str]:
        """Return columns for the PCA components table."""
        if not self.cleaned_data_columns:
            return ["component"]
        return ["component"] + self.cleaned_data_columns

    @rx.var
    def raw_data_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.raw_data) if self.raw_data else pd.DataFrame()

    @rx.var
    def uploaded_filename(self) -> str:
        return self.uploaded_files[0] if self.uploaded_files else ""

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Process uploaded CSV file."""
        self.is_uploading = True
        yield
        if not files:
            self.is_uploading = False
            yield rx.toast.error("No file selected.")
            return
        file = files[0]
        try:
            upload_data = await file.read()
            df = pd.read_csv(io.BytesIO(upload_data))
            self.raw_data = df.head(200).to_dict("records")
            self.raw_data_columns = df.columns.to_list()
            self.uploaded_files = [file.name]
            self.current_stage = "Uploaded"
        except Exception as e:
            logging.exception(f"Error processing file: {e}")
            self.raw_data = []
            self.raw_data_columns = []
            self.uploaded_files = []
            self.current_stage = "Upload"
            yield rx.toast.error(f"Error processing file: {e}")
        finally:
            self.is_uploading = False

    @rx.event
    def run_cleaning(self):
        """Runs the data cleaning pipeline."""
        if not self.raw_data:
            yield rx.toast.error("No data to clean. Please upload a file first.")
            return
        self.current_stage = "Cleaning..."
        yield
        try:
            df = pd.DataFrame(self.raw_data)
            cleaned_df, log, summary = clean_data(df)
            self.cleaned_data = cleaned_df.to_dict("records")
            self.cleaned_data_columns = cleaned_df.columns.to_list()
            self.cleaning_log = log
            self.cleaning_summary = summary
            self.current_stage = "Cleaned"
            yield rx.toast.success("Data cleaning complete!")
            yield rx.redirect("/data-cleaning")
        except Exception as e:
            logging.exception(f"Error during cleaning: {e}")
            self.current_stage = "Upload Failed"
            yield rx.toast.error(f"Cleaning failed: {e}")

    @rx.event
    def run_pca(self):
        """Runs the PCA analysis on cleaned data."""
        if not self.cleaned_data:
            yield rx.toast.error("No cleaned data available for PCA.")
            return
        self.current_stage = "PCA Analysis..."
        yield
        try:
            df = pd.DataFrame(self.cleaned_data)
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            results = perform_pca(df)
            self.pca_results = {
                "explained_variance": results["explained_variance"].tolist(),
                "cumulative_variance": results["cumulative_variance"].tolist(),
                "eigenvalues": results["eigenvalues"].tolist(),
            }
            self.pca_variance_data = [
                {"component": f"PC{i + 1}", "variance": v * 100, "cumulative": c * 100}
                for i, (v, c) in enumerate(
                    zip(results["explained_variance"], results["cumulative_variance"])
                )
            ]
            pca_df = pd.DataFrame(
                results["pca_result"],
                columns=[f"PC{i + 1}" for i in range(results["pca_result"].shape[1])],
            )
            self.pca_scatter_data = pca_df[["PC1", "PC2"]].to_dict("records")
            components_df = pd.DataFrame(
                results["components"],
                columns=numeric_cols,
                index=[f"PC{i + 1}" for i in range(results["components"].shape[0])],
            )
            self.pca_components_data = (
                components_df.reset_index()
                .rename(columns={"index": "component"})
                .to_dict("records")
            )
            self.pca_data = pca_df.to_dict("records")
            self.current_stage = "PCA Complete"
            yield rx.toast.success("PCA analysis complete!")
            yield rx.redirect("/pca-analysis")
        except Exception as e:
            logging.exception(f"Error during PCA: {e}")
            self.current_stage = "PCA Failed"
            yield rx.toast.error(f"PCA failed: {e}")

    @rx.event
    def compute_elbow_method(self):
        if not self.pca_data:
            yield rx.toast.error("PCA data not available. Please run PCA first.")
            return
        self.current_stage = "Computing Elbow..."
        yield
        try:
            pca_df = pd.DataFrame(self.pca_data)
            self.elbow_data = compute_elbow_data(pca_df)
            self.current_stage = "PCA Complete"
            yield rx.toast.success("Elbow method data computed.")
        except Exception as e:
            logging.exception(f"Elbow method failed: {e}")
            yield rx.toast.error(f"Failed to compute elbow data: {e}")

    @rx.event
    def run_clustering(self, k: int):
        if not self.pca_data:
            yield rx.toast.error("No PCA data available for clustering.")
            return
        self.num_clusters = int(k)
        self.current_stage = "Clustering..."
        yield
        try:
            pca_df = pd.DataFrame(self.pca_data)
            original_df = pd.DataFrame(self.cleaned_data)
            clusters = perform_clustering(pca_df, self.num_clusters)
            clustered_df = pca_df.copy()
            clustered_df["cluster"] = clusters
            self.clustered_data = clustered_df.to_dict("records")
            scatter_data_by_cluster = {}
            for i in range(self.num_clusters):
                cluster_data = clustered_df[clustered_df["cluster"] == i]
                scatter_data_by_cluster[i] = cluster_data.to_dict("records")
            self.cluster_scatter_data = scatter_data_by_cluster
            self.cluster_profiles = generate_cluster_profiles(original_df, clusters)
            self.current_stage = "Clustered"
            yield rx.toast.success(f"Clustering complete with {k} clusters.")
            yield rx.redirect("/clustering")
        except Exception as e:
            logging.exception(f"Clustering failed: {e}")
            self.current_stage = "Clustering Failed"
            yield rx.toast.error(f"Clustering failed: {e}")

    @rx.event
    def generate_profiles(self):
        """Generates data for comparison charts and navigates to the profiles page."""
        if not self.cluster_profiles:
            yield rx.toast.error("No cluster profiles to display.")
            return
        self.current_stage = "Profiling"
        yield rx.redirect("/customer-profiles")

    @rx.event
    def filter_by_cluster(self, cluster_id: int):
        self.selected_cluster_filter = int(cluster_id)

    @rx.event
    def generate_insights(self):
        if not self.cluster_profiles:
            yield rx.toast.error("No cluster profiles available to generate insights.")
            return
        self.current_stage = "Generating Insights..."
        yield
        try:
            self.insights_data = generate_marketing_insights(self.cluster_profiles)
            total_customers = sum((p["size"] for p in self.cluster_profiles))
            self.distribution_pie_data = [
                {
                    "name": insight["segment_name"],
                    "value": insight["size"],
                    "percentage": insight["size"] / total_customers * 100,
                }
                for insight in self.insights_data
            ]
            self.kpi_summary = {
                "total_customers": total_customers,
                "num_segments": len(self.cluster_profiles),
                "avg_segment_size": int(
                    total_customers / len(self.cluster_profiles)
                    if self.cluster_profiles
                    else 0
                ),
            }
            self.current_stage = "Insights Generated"
            yield rx.toast.success("Marketing insights generated!")
            yield rx.redirect("/insights")
        except Exception as e:
            logging.exception(f"Error generating insights: {e}")
            self.current_stage = "Insights Failed"
            yield rx.toast.error(f"Failed to generate insights: {e}")

    @rx.event
    def download_cleaning_log(self):
        """Downloads the cleaning log as a CSV file."""
        log_content = """
""".join(self.cleaning_log)
        return rx.download(data=log_content, filename="cleaning_log.txt")

    @rx.event
    def download_cluster_summary(self):
        if not self.cluster_profiles:
            return rx.toast.error("No cluster summary to download.")
        try:
            df = pd.DataFrame(self.cluster_profiles)
            csv_string = df.to_csv(index=False)
            return rx.download(data=csv_string, filename="cluster_summary.csv")
        except Exception as e:
            logging.exception(f"Error creating CSV for download: {e}")
            return rx.toast.error("Failed to prepare download.")

    @rx.event
    def download_insights_report(self):
        if not self.insights_data:
            return rx.toast.error("No insights to download.")
        try:
            df = pd.DataFrame(self.insights_data)
            df["recommendations"] = df["recommendations"].apply(
                lambda recs: " | ".join([r["text"] for r in recs])
            )
            df["kpis"] = df["kpis"].apply(
                lambda kpis: " | ".join([f"{k['name']}: {k['value']}" for k in kpis])
            )
            csv_string = df.to_csv(index=False)
            return rx.download(
                data=csv_string, filename="marketing_insights_report.csv"
            )
        except Exception as e:
            logging.exception(f"Error creating insights CSV: {e}")
            return rx.toast.error("Failed to prepare insights report.")