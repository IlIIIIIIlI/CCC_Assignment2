# -----------------------------
# !/usr/bin/env Python3      --
# -*- coding: utf-8 -*-      --
# @Author   : Quechen YANG   --
# @FILE     : testpage.py     
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


def testpage():
    # Download stopwords
    nltk.download("stopwords")
    stop = stopwords.words('english')

    def standardize(text):
        text = re.sub('[^a-zA-Z\d\s]', '', text)
        text = text.lower()
        return text

    def word_cloud(content, title):
        wc = WordCloud(background_color="white", max_words=200, contour_width=3,
                       stopwords=STOPWORDS, max_font_size=50)
        wc.generate(" ".join(content.index.values))
        fig, ax = plt.subplots(figsize=(15, 15), dpi=100)
        ax.set_title(title, fontsize=20)
        ax.imshow(wc.recolor(colormap='magma', random_state=42), cmap=plt.cm.gray, interpolation="bilinear",
                  alpha=0.98)
        ax.axis('off')
        st.pyplot(fig)

    def main():
        st.title("Word Cloud Generator")

        # Load your dataset here
        dataset = load_dataset("merve/poetry", streaming=True)
        df = pd.DataFrame.from_dict(dataset["train"])

        # Clean the text data
        df.content = df.content.apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
        df.content = df.content.apply(standardize)

        # Generate word clouds
        content = df.content.str.split(expand=True).unstack().value_counts()
        word_cloud(content, "Word Cloud")

    main()


