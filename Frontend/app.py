import streamlit as st

st.set_page_config(layout="wide", page_title="Your App Title", page_icon=":emoji:")

# 导入页面函数
from utils.pages.home_page import home_page
from utils.pages.overview_page import overview_page
from utils.pages.pdb_page import pdb_page
from utils.pages.map import streamlit_app
from utils.pages.new_page import new_page
from utils.pages.search_table import search_table
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
app.add_app("Database Overview", overview_page)
app.add_app("Search PDB", pdb_page)
app.add_app("map", streamlit_app)
app.add_app("New Page", new_page) # 添加新页面
app.add_app("search_table",search_table)
# 添加其他页面，如需要

app.run()
