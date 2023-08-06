import altair as alt
import pandas as pd
import streamlit as st

import encord_active_app.common.state as state

from . import ModelAssertionsPage


class PerformanceIndex(ModelAssertionsPage):
    title = "⚡️ Performance by Indexer"

    @staticmethod
    def build_bar_chart(sorted_predictions: pd.DataFrame, index_name: str, show_decomposition: bool) -> alt.Chart:
        largest_bin_count = sorted_predictions["bin"].value_counts().max()
        chart_title = f"True Positive Rate - {st.session_state.get(state.PREDICTIONS_INDEX, '')}"
        if show_decomposition:
            # Aggregate over each class
            return (
                alt.Chart(sorted_predictions, title=chart_title)
                .transform_joinaggregate(total="count(*)")
                .transform_calculate(
                    pctf=f"1 / {largest_bin_count}",
                    pct="100 / datum.total",
                )
                .mark_bar(align="center", opacity=0.2)
                .encode(
                    alt.X("bin:Q"),
                    alt.Y("sum(pctf):Q", stack="zero"),
                    alt.Color("class_name:N"),
                    tooltip=[
                        alt.Tooltip("bin", title=index_name, format=",.4f"),
                        alt.Tooltip("count():Q", title="Num predictions", format=",d"),
                        alt.Tooltip("sum(pct):Q", title="% of total predictions", format=",.2f"),
                        alt.Tooltip("class_name:N", title="Class name"),
                    ],
                )
            )
        else:
            # Only use aggregate over all classes
            return (
                alt.Chart(sorted_predictions, title=chart_title)
                .transform_joinaggregate(total="count(*)")
                .transform_calculate(
                    pctf=f"1 / {largest_bin_count}",
                    pct="100 / datum.total",
                )
                .mark_bar(align="center", opacity=0.2)
                .encode(
                    alt.X("bin:Q"),
                    alt.Y("sum(pctf):Q", stack="zero"),
                    tooltip=[
                        alt.Tooltip("bin", title=index_name, format=",.4f"),
                        alt.Tooltip("count():Q", title="Num predictions", format=",d"),
                        alt.Tooltip("sum(pct):Q", title="% of total predictions", format=",.2f"),
                    ],
                )
            )

    @staticmethod
    def build_line_chart(bar_chart: alt.Chart, index_name: str, show_decomposition: bool) -> alt.Chart:
        legend = alt.Legend(title="class name".title())
        line_chart = (
            bar_chart.mark_line(point=True, opacity=0.5 if show_decomposition else 1.0)
            .encode(
                alt.X("bin:Q"),
                alt.Y("mean(tps):Q"),
                alt.Color("average:N", legend=legend),
                tooltip=[
                    alt.Tooltip("bin", title=index_name, format=",.4f"),
                    alt.Tooltip("mean(tps):Q", title="TPR", format=",.4f"),
                    alt.Tooltip("average:N", title="Class name"),
                ],
                strokeDash=alt.value([5, 5]),
            )
            .properties(height=500)
        )

        if show_decomposition:
            line_chart += line_chart.mark_line(point=True).encode(
                alt.Color("class_name:N", legend=legend),
                tooltip=[
                    alt.Tooltip("bin", title=index_name, format=",.4f"),
                    alt.Tooltip("mean(tps):Q", title="TPR", format=",.4f"),
                    alt.Tooltip("class_name:N", title="Class name"),
                ],
                strokeDash=alt.value([10, 0]),
            )
        return line_chart

    @staticmethod
    def build_average_rule(tps_mean):
        return (
            alt.Chart(pd.DataFrame({"y": [tps_mean], "average": ["average"]}))
            .mark_rule()
            .encode(
                alt.Y("y"),
                alt.Color("average:N"),
                strokeDash=alt.value([5, 5]),
                tooltip=[alt.Tooltip("y", title="Average tps", format=",.4f")],
            )
        )

    def sidebar_options(self):
        c1, c2, c3 = st.columns([4, 4, 3])
        with c1:
            self.prediction_index_in_sidebar()

        with c2:
            st.number_input(
                "Number of buckets (n)",
                min_value=5,
                max_value=200,
                value=50,
                help="Choose the number of bins to discritize the prediction index values into.",
                key=state.PREDICTIONS_NBINS,
            )
        with c3:
            st.write("")  # Make some spacing.
            st.write("")
            st.checkbox("Show class decomposition", key=state.PREDICTIONS_DECOMPOSE_CLASSES)

    def build(
        self,
        model_predictions: pd.DataFrame,
        labels: pd.DataFrame,
        metrics: pd.DataFrame,
        precisions: pd.DataFrame,
    ):
        st.markdown(f"# {self.title}")

        if model_predictions.shape[0] == 0:
            st.write("No predictions of the given class(es).")
        elif state.PREDICTIONS_INDEX not in st.session_state:
            st.write("No indices computed")
        else:
            with st.expander("Details", expanded=False):
                st.markdown(
                    """### The view

On this page, your model scores are displayed as a function of the indexer that you selected in the sidebar.
Samples are discritized into $n$ equally sized buckets and the middle point of each bucket is displayed as the x-value in the plots.
Bars indicate the number of samples in each bucket, while lines indicate the true positive rate of each bucket.

Indexers marked with (P) are tests performed on your predictions.
Indexers marked with (F) are frame level indices, which depends on the frame that each prediction is associated
with.""",
                    unsafe_allow_html=True,
                )
                self.indexer_details_description()

            index_name = st.session_state[state.PREDICTIONS_INDEX]
            num_unique_values = model_predictions[index_name].unique().shape[0]
            n_bins = min(st.session_state.get(state.PREDICTIONS_NBINS, 100), num_unique_values)
            sorted_predictions = model_predictions[[index_name, "tps", "class_name"]].copy().dropna(subset=[index_name])
            sorted_predictions["bin"] = pd.qcut(sorted_predictions[index_name], q=n_bins, duplicates="drop").map(
                lambda x: x.mid
            )
            sorted_predictions["average"] = "average"

            show_decomposition = st.session_state[state.PREDICTIONS_DECOMPOSE_CLASSES]
            bar_chart = self.build_bar_chart(sorted_predictions, index_name, show_decomposition)
            line_chart = self.build_line_chart(bar_chart, index_name, show_decomposition)
            mean_rule = self.build_average_rule(model_predictions["tps"].mean())

            chart_composition = bar_chart + line_chart + mean_rule
            chart_composition = chart_composition.encode(
                alt.X(title=index_name.title()), alt.Y(title="true positive rate".title())
            ).interactive()

            st.altair_chart(chart_composition, use_container_width=True)
