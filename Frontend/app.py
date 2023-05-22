import streamlit as st

st.set_page_config(layout="wide", page_title="Aussie Happiness Tweets", page_icon="🐨")

from utils.pages.home_page import home_page
from utils.pages.BloggerAnalysis import Blogger_Analysis
from utils.pages.official import official
from utils.pages.MapAnalysis import Map_Analysis
from utils.pages.SevenAspects import Seven_Aspects
from utils.pages.About import About

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        st.sidebar.markdown("## Main Menu")
        app = st.sidebar.selectbox(
            "Select Page", self.apps, format_func=lambda app: app["title"]
        )
        st.sidebar.markdown("---")
        app["function"]()

app = MultiApp()

app.add_app("Home Page", home_page)
# Now add the rest of the apps
app.add_app("Map Analysis", Map_Analysis)
app.add_app("Blogger Analysis", Blogger_Analysis)
app.add_app("Seven-Aspects Analysis", Seven_Aspects) # 添加新页面
app.add_app("Official Data Implication", official)
app.add_app("About Us", About)
# app.add_app("search_table",search_table)

app.run()
