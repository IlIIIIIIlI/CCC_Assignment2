# -----------------------------
# !/usr/bin/env Python3      --
# -*- coding: utf-8 -*-      --
# @Author   : Quechen YANG   --
# @FILE     : About.py
# @Time     : 30/04/2023 3:26 pm
# -----------------------------
import streamlit as st
import numpy as np
import pandas as pd
import re
import nltk
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from datasets import load_dataset
import matplotlib.pyplot as plt

import streamlit as st


def About():
    st.title('About us')

    # 插入文本
    st.markdown("""
    Here, we are committed to providing you with the highest quality service. Our team is composed of the most professional and passionate individuals in the industry, each with rich experience and profound knowledge in their respective fields. Our goal is to exceed customer expectations and continuously innovate to respond to rapidly changing market environments.
    """)

    # 插入图片
    st.image("https://photosavercn.oss-cn-guangzhou.aliyuncs.com/img/202305221823228.png", use_column_width=True)

    # 更多文本内容
    st.markdown("""
    We sincerely invite you to join us on our journey and together, realize more possibilities.
    """)
