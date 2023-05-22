import streamlit as st
from ..functions import create_markdown_link, create_st_button
from ..constants import PROJECT_RESOURCES_LINKS

import pandas as pd
import altair as alt
import json
def home_page():
    # Load the data
    with open('./utils/data/mastodon.json') as f:
        json_data = json.load(f)

    # Convert the JSON data into a Pandas DataFrame
    data_dict = {date: {**value, 'Date': date} for date, value in json_data.items()}
    data = pd.DataFrame(data_dict.values())
    data['Date'] = pd.to_datetime(data['Date']).dt.date  # Convert to just date

    # Create Altair chart
    bar = alt.Chart(data).mark_bar().encode(
        x=alt.X('Date:O', axis=alt.Axis(title='Date')),  # :O specifies the type as ordinal
        y='count:Q',
        tooltip=['Date:O', 'count:Q', 'cumulative_count:Q']
    )

    line = alt.Chart(data).mark_line(color='red').encode(
        x='Date:O',
        y='cumulative_count:Q'
    )

    # Compute the count delta
    latest_count = data.iloc[-1]['count']
    previous_count = data.iloc[-2]['count']
    delta = (latest_count - previous_count) / previous_count

    # Streamlit application
    st.title("📊 Mastodon Activity Analysis")
    st.markdown("### An analysis tool for observing daily and accumulated Mastodon activity 📈")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Daily Post Count and Accumulated Post Count Over Time")
        st.altair_chart(bar + line, use_container_width=True)

    with col2:
        st.markdown("### Most Recent Daily Post Count")
        st.metric(label="Count", value=int(latest_count), delta=f"{delta:.2%}")

    st.sidebar.markdown("## Database-Related Links")
    for link_text, link_url in PROJECT_RESOURCES_LINKS.items():
        create_st_button(link_text, link_url, st_col=st.sidebar)
