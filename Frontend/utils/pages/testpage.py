# -----------------------------
# !/usr/bin/env Python3      --
# -*- coding: utf-8 -*-      --
# @Author   : Quechen YANG   --
# @FILE     : testpage.py     
# @Time     : 30/04/2023 3:26 pm
# -----------------------------
import streamlit as st
import numpy as np
from PIL import ImageDraw, Image
from wordcloud import WordCloud
import random
import time


def testpage():
    # Function to generate a wordcloud
    # Define the data for your wordcloud
    text = "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10"

    st.title("Dynamic Clickable Wordcloud")

    canvas_size = (800, 600)
    speed = st.slider("Speed", 1, 20, 10)

    wc = WordCloud(background_color="white", width=canvas_size[0], height=canvas_size[1], prefer_horizontal=1)
    wc.generate(text)

    from PIL import ImageDraw, ImageFont

    def create_moving_wordcloud_image():
        image = Image.new("RGB", canvas_size, "white")
        draw = ImageDraw.Draw(image)

        for word, freq in wc.words_.items():
            position = random.randint(0, canvas_size[0] - 50), random.randint(0, canvas_size[1] - 50)
            size = random.randint(15, 50)
            font_path, font_size = wc.font_path, size
            font = ImageFont.truetype(font_path, font_size)
            draw.text(position, word, font=font, fill="black")

        return image

    def check_click(click_position, image):
        for word, freq in wc.words_.items():
            position = random.randint(0, canvas_size[0] - 50), random.randint(0, canvas_size[1] - 50)
            size = random.randint(15, 50)
            font = wc.font_path, size
            draw = ImageDraw.Draw(image)
            w, h = draw.textsize(word, font=font)

            x, y = position
            if x < click_position[0] < x + w and y < click_position[1] < y + h:
                return word

        return None

    words_clicked = []

    while True:
        image = create_moving_wordcloud_image()
        image_placeholder = st.empty()
        click_position = image_placeholder.image(image, use_column_width=True, output_format="PNG", channels="RGB",
                                                 clamp=True).clicks
        if click_position:
            clicked_word = check_click(click_position, image)
            if clicked_word:
                words_clicked.append(clicked_word)
                st.write(f"Clicked word: {clicked_word}")

        time.sleep(1 / speed)

