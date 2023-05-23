import streamlit as st
from ..functions import create_markdown_link, create_st_button
from ..constants import PROJECT_RESOURCES_LINKS
import requests
import pandas as pd
import altair as alt
import json
def home_page():
    # Load the data
    # with open('./utils/data/mastodon.json') as f:
    #     json_data = json.load(f)

    #----------------------------------------------------------------
    with open('config.json') as f:
        localhost = json.load(f)['IP']

    # Fetch data from server
    r = requests.get(f'http://{localhost}:8000/homepage', timeout=200)
    # parse json
    json_data = r.json()
    # ----------------------------------------------------------------

    # Convert the JSON data into a Pandas DataFrame
    data_dict = {date: {**value, 'Date': date} for date, value in json_data.items()}
    data = pd.DataFrame(data_dict.values())
    data['Date'] = pd.to_datetime(data['Date']).dt.date  # Convert to just date

    # Create Altair chart
    bar = alt.Chart(data).mark_bar().encode(
        x=alt.X('Date:O', axis=alt.Axis(title='Date', labelAngle=-45)),  # :O specifies the type as ordinal
        y='count:Q',
        tooltip=['Date:O', 'count:Q', 'cumulative_count:Q']
    )

    line = alt.Chart(data).mark_line(color='red').encode(
        x=alt.X('Date:O', axis=alt.Axis(title='Date', labelAngle=-45)),
        y='cumulative_count:Q'
    )

    # Compute the count delta
    latest_count = data.iloc[-1]['count']
    latest_cumulative_count = data.iloc[-1]['cumulative_count']
    previous_count = data.iloc[-2]['count']
    delta = (latest_count - previous_count) / previous_count

    # Streamlit application
    st.markdown("<h1 style='text-align: center; color: #aaf683;'>📊 Australia Social Media Analytics on the Cloud</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: pink;'>Happiness of Australian</h2>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns((5,3))

    with col1:
        st.markdown("##### This project aims to develop a cloud-based system that harnesses social media data, specifically from Twitter and Mastodon, alongside official data from the SUDO to conduct targeted analytics and visualizations. The theme is happiness aspects of life in Australia.")
        st.markdown("Our analysis is based on geolocated tweet data, textual information, typical happiness content from bloggers on both platforms, and official data revelations about the happiness of the Australian people.")
        st.markdown(">**The webpage consists of six main parts:**")

        st.markdown("""
        <style>
        .text-grey-background {
            background-color: #caf0f8;
        }
        .text-blue-black {
            color: #0077b6 !important;  /* 蓝黑色的RGB代码 */
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="text-grey-background text-blue-black">🏠 <strong>Homepage:</strong> Introducing the project and displaying on-site data. \n\n</div>',
            unsafe_allow_html=True)
        st.markdown("\n")
        st.markdown(
            '<div class="text-grey-background text-blue-black">🌐 <strong>Map Analysis:</strong> Visualizing and analyzing tweets\' distribution, indicating patterns of happiness. \n\n</div>',
            unsafe_allow_html=True)
        st.markdown("\n")
        st.markdown(
            '<div class="text-grey-background text-blue-black">🐦 <strong>Blogger Analysis:</strong> Analyzing tweets from active Twitter and Mastodon bloggers. \n\n</div>',
            unsafe_allow_html=True)
        st.markdown("\n")
        st.markdown(
            '<div class="text-grey-background text-blue-black">🔎 <strong>Seven-Aspects Analysis:</strong> Interactive exploration of conversations about happiness aspects. \n\n</div>',
            unsafe_allow_html=True)
        st.markdown("\n")
        st.markdown(
            '<div class="text-grey-background text-blue-black">📈 <strong>Official Data Implication:</strong> Revealing consistencies or discrepancies between Twitter and SUDO data. \n\n</div>',
            unsafe_allow_html=True)
        st.markdown("\n")
        st.markdown(
            '<div class="text-grey-background text-blue-black">👥 <strong>About Us:</strong> Introduction to the team.</div>',
            unsafe_allow_html=True)

    with col2:
        st.markdown("#### Real-time Mastodon data crawler log")
        st.altair_chart(bar + line, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="Today's data inflow", value=int(latest_count), delta=f"{delta:.2%}")
        with c2:
            st.metric(label="Total data inflow", value=int(latest_cumulative_count))

    st.sidebar.image("https://photosavercn.oss-cn-guangzhou.aliyuncs.com/img/202305231320347.jpg")
    st.sidebar.caption("Cluster and Cloud Computing (COMP90024_2023_SM1)")
    st.sidebar.caption("Group33")
    st.sidebar.markdown("## Database-Related Links")
    for link_text, link_url in PROJECT_RESOURCES_LINKS.items():
        create_st_button(link_text, link_url, st_col=st.sidebar)
