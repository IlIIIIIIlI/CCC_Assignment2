from datetime import date, datetime
import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

import random
def pdb_page():
    def icon(emoji: str):
        """Shows an emoji as a Notion-style page icon."""
        st.write(
            f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
            unsafe_allow_html=True,
        )

    # Generate fake data
    def generate_fake_data(start_date):
        start_date = pd.to_datetime(start_date)
        date_range = pd.date_range(start=start_date, end=pd.to_datetime("now"), freq='M')
        projects = ['pandas', 'keras', 'torch', 'tensorflow', 'numpy', 'sci-kit learn']
        data = []

        for project in projects:
            for date in date_range:
                data.append({
                    'date': date,
                    'project': project,
                    'downloads': max(1, int(abs(100000 * np.random.randn())))
                })

        df = pd.DataFrame(data)
        df['delta'] = (df.groupby(["project"])["downloads"].pct_change()).fillna(0)
        df["date"] = df["date"].astype("datetime64")

        return df

    df_fake = generate_fake_data('2020-01-01')

    # Use the same functions from your code but replace the real data with the fake data

    def monthly_downloads(start_date):
        return df_fake

    def weekly_downloads(start_date):
        return df_fake

    def plot_all_downloads(
            source, x="date", y="downloads", group="project", axis_scale="linear"
    ):

        if st.checkbox("View logarithmic scale"):
            axis_scale = "log"

        brush = alt.selection_interval(encodings=["x"], empty="all")

        click = alt.selection_multi(encodings=["color"])

        lines = (
            (
                alt.Chart(source)
                .mark_line(point=True)
                .encode(
                    x=x,
                    y=alt.Y("downloads", scale=alt.Scale(type=f"{axis_scale}")),
                    color=group,
                    tooltip=[
                        "date",
                        "project",
                        "downloads",
                        alt.Tooltip("delta", format=".2%"),
                    ],
                )
            )
            .add_selection(brush)
            .properties(width=550)
            .transform_filter(click)
        )

        bars = (
            alt.Chart(source)
            .mark_bar()
            .encode(
                y=group,
                color=group,
                x=alt.X("downloads:Q", scale=alt.Scale(type=f"{axis_scale}")),
                tooltip=["date", "downloads", alt.Tooltip("delta", format=".2%")],
            )
            .transform_filter(brush)
            .properties(width=550)
            .add_selection(click)
        )

        return lines & bars

    def pandasamlit_downloads(source, x="date", y="downloads"):
        # Create a selection that chooses the nearest point & selects based on x-value
        hover = alt.selection_single(
            fields=[x],
            nearest=True,
            on="mouseover",
            empty="none",
        )

        lines = (
            alt.Chart(source)
            .mark_line(point="transparent")
            .encode(x=x, y=y)
            .transform_calculate(color='datum.delta < 0 ? "red" : "green"')
        )

        # Draw points on the line, highlight based on selection, color based on delta
        points = (
            lines.transform_filter(hover)
            .mark_circle(size=65)
            .encode(color=alt.Color("color:N", scale=None))
        )

        # Draw an invisible rule at the location of the selection
        tooltips = (
            alt.Chart(source)
            .mark_rule(opacity=0)
            .encode(
                x=x,
                y=y,
                tooltip=[x, y, alt.Tooltip("delta", format=".2%")],
            )
            .add_selection(hover)
        )

        return (lines + points + tooltips).interactive()

    def main():

        # Note that page title/favicon are set in the __main__ clause below,
        # so they can also be set through the mega multipage app (see ../pandas_app.py).

        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Select start date",
                date(2020, 1, 1),
                min_value=datetime.strptime("2020-01-01", "%Y-%m-%d"),
                max_value=datetime.now(),
            )

        with col2:
            time_frame = st.selectbox(
                "Select weekly or monthly downloads", ("weekly", "monthly")
            )

        # PREPARING DATA FOR WEEKLY AND MONTHLY

        df_monthly = monthly_downloads(start_date)
        df_weekly = weekly_downloads(start_date)

        pandas_data_monthly = df_monthly[df_monthly["project"] == "pandas"]
        pandas_data_weekly = df_weekly[df_weekly["project"] == "pandas"]

        package_names = df_monthly["project"].unique()

        if time_frame == "weekly":
            selected_data_streamlit = pandas_data_weekly
            selected_data_all = df_weekly
        else:
            selected_data_streamlit = pandas_data_monthly
            selected_data_all = df_monthly

        ## PANDAS DOWNLOADS

        st.header("Pandas downloads")

        st.altair_chart(
            pandasamlit_downloads(selected_data_streamlit), use_container_width=True
        )

        # OTHER DOWNLOADS

        st.header("Compare other package downloads")

        instructions = """
        Click and drag line chart to select and pan date interval\n
        Hover over bar chart to view downloads\n
        Click on a bar to highlight that package
        """
        select_packages = st.multiselect(
            "Select Python packages to compare",
            package_names,
            default=[
                "pandas",
                "keras",
            ],
            help=instructions,
        )

        select_packages_df = pd.DataFrame(select_packages).rename(columns={0: "project"})

        if not select_packages:
            st.stop()

        filtered_df = selected_data_all[
            selected_data_all["project"].isin(select_packages_df["project"])
        ]

        st.altair_chart(plot_all_downloads(filtered_df), use_container_width=True)

    st.title("Downloads")
    st.write(
        "Metrics on how often Pandas is being downloaded from PyPI (Python's main "
        "package repository, i.e. where `pip install pandas` downloads the package from)."
    )
    main()

    # TODO:
    @st.cache_data
    def get_data():
        source = data.stocks()
        source = source[source.date.gt("2004-01-01")]
        return source

    @st.cache_data(ttl=60 * 60 * 24)
    def get_chart(data):
        hover = alt.selection_single(
            fields=["date"],
            nearest=True,
            on="mouseover",
            empty="none",
        )

        lines = (
            alt.Chart(data, height=500, title="Evolution of stock prices")
            .mark_line()
            .encode(
                x=alt.X("date", title="Date"),
                y=alt.Y("price", title="Price"),
                color="symbol",
            )
        )

        # Draw points on the line, and highlight based on selection
        points = lines.transform_filter(hover).mark_circle(size=65)

        # Draw a rule at the location of the selection
        tooltips = (
            alt.Chart(data)
            .mark_rule()
            .encode(
                x="yearmonthdate(date)",
                y="price",
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("date", title="Date"),
                    alt.Tooltip("price", title="Price (USD)"),
                ],
            )
            .add_selection(hover)
        )

        return (lines + points + tooltips).interactive()

    st.title("⬇ Time series annotations")

    st.write("Give more context to your time series using annotations!")

    col1, col2, col3 = st.columns(3)
    with col1:
        ticker = st.text_input("Choose a ticker (⬇💬👇ℹ️ ...)", value="⬇")
    with col2:
        ticker_dx = st.slider(
            "Horizontal offset", min_value=-30, max_value=30, step=1, value=0
        )
    with col3:
        ticker_dy = st.slider(
            "Vertical offset", min_value=-30, max_value=30, step=1, value=-10
        )

    # Original time series chart. Omitted `get_chart` for clarity
    source = get_data()
    chart = get_chart(source)

    # Input annotations
    ANNOTATIONS = [
        ("Mar 01, 2008", "Pretty good day for GOOG"),
        ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
        ("Nov 01, 2008", "Market starts again thanks to..."),
        ("Dec 01, 2009", "Small crash for GOOG after..."),
    ]

    # Create a chart with annotations
    annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
    annotations_df.date = pd.to_datetime(annotations_df.date)
    annotations_df["y"] = 0
    annotation_layer = (
        alt.Chart(annotations_df)
        .mark_text(size=15, text=ticker, dx=ticker_dx, dy=ticker_dy, align="center")
        .encode(
            x="date:T",
            y=alt.Y("y:Q"),
            tooltip=["event"],
        )
        .interactive()
    )

    # Display both charts together
    st.altair_chart((chart + annotation_layer).interactive(), use_container_width=True)

    st.write("## Code")

    st.write(
        "See more in our public [GitHub"
        " repository](https://github.com/streamlit/example-app-time-series-annotation)"
    )