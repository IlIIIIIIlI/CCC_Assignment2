import streamlit as st
from ..functions import create_markdown_link, create_st_button
from ..constants import DATABASE_LINKS, COMMUNITY_LINKS, SOFTWARE_LINKS

def home_page():
    st.title("Rascore")
    st.markdown("### A tool for analyzing RAS protein structures")
    st.markdown("**Created by Mitchell Parker and Roland Dunbrack**")
    st.markdown("**Fox Chase Cancer Center**")

    st.sidebar.markdown("## Database-Related Links")
    for link_text, link_url in DATABASE_LINKS.items():
        create_st_button(link_text, link_url, st_col=st.sidebar)

    st.sidebar.markdown("## Community-Related Links")
    for link_text, link_url in COMMUNITY_LINKS.items():
        create_st_button(link_text, link_url, st_col=st.sidebar)

    st.sidebar.markdown("## Software-Related Links")
    for link_text, link_url in SOFTWARE_LINKS.items():
        create_st_button(link_text, link_url, st_col=st.sidebar)
