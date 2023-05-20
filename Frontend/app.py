import streamlit as st

st.set_page_config(layout="wide", page_title="Aussie Happiness Tweets", page_icon="🐨")

# 导入页面函数
from utils.pages.home_page import home_page
from utils.pages.BloggerAnalysis import Blogger_Analysis
from utils.pages.pdb_page import pdb_page
from utils.pages.MapAnalysis import Map_Analysis
from utils.pages.SevenAspects import Seven_Aspects
from utils.pages.testpage import testpage
# from utils.pages.search_table import search_table
# 从提供的文件结构中导入其他页面函数，如需要

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

# 将页面添加到应用程序中
app.add_app("Home Page", home_page)
app.add_app("Blogger Analysis", Blogger_Analysis)
app.add_app("SevenAspects", Seven_Aspects) # 添加新页面
app.add_app("MapAnalysis", Map_Analysis)
app.add_app("Search PDB", pdb_page)
app.add_app("testpage", testpage)
# app.add_app("search_table",search_table)
# 添加其他页面，如需要

app.run()
