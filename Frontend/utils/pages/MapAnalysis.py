import os
from streamlit import sidebar
import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import json
import requests
import folium
from folium import plugins
from folium.plugins import Draw, Fullscreen
import streamlit as st
import streamlit_folium as sf
from streamlit_folium import folium_static


def MapAnalysis():
    import numpy as np
    from collections import Counter
    def find_outliers(data):
        # count the number of occurrences for each coordinate
        coord_counts = Counter(zip(data['lon'], data['lat']))
        # outlier threshold
        counts = list(coord_counts.values())
        q75, q25 = np.percentile(counts, [75, 25])
        iqr = q75 - q25
        threshold = q75 + 1.5 * iqr
        # outliers lon and lat
        outlier_coords = [coord for coord, count in coord_counts.items() if count > threshold]
        # ex outliers
        filtered_data = data[~data.apply(lambda row: (row['lon'], row['lat']) in outlier_coords, axis=1)]
        print('filter data {} rows'.format(filtered_data.shape[0]))
        print('data {} rows'.format(data.shape[0]))
        return filtered_data

    @st.cache_resource
    def load_data():
        # Load IP address
        with open('config.json') as f:
            localhost = json.load(f)['IP']

        # Fetch data from server
        r = requests.get(f'http://{localhost}:8000/page1data', timeout=200)
        # parse json
        data = r.json()

        # parse dataframe
        data = pd.DataFrame(data)
        data["datetime"] = pd.to_datetime(data["datetime"])
        data[["lon", "lat"]] = pd.DataFrame(data["loc"].to_list(), index=data.index)
        data = data.drop(columns=["loc"])
        data['count'] = data.groupby(['lat', 'lon']).transform('count')['datetime']
        filtered_data = find_outliers(data)
        return filtered_data


    # 生成地图
    def map(data, lat, lon, zoom):
        print('数据有 {} 行'.format(data.shape[0]))
        data = data.drop(columns=["city"])
        st.write(
            pdk.Deck(
                map_style="mapbox://styles/chenoi/cl9hsjbv0000614p8dberfesh",
                initial_view_state={
                    "latitude": lat,
                    "longitude": lon,
                    "zoom": zoom,
                    "pitch": 25,
                },
                layers=[
                    pdk.Layer(
                        "HeatmapLayer",
                        data=data,
                        get_position=["lon", "lat"],
                        get_weight="count*50",
                        opacity=0.5,
                        # radius of bubble
                        radiusPixels=70,
                        # the heatmap bubble
                        colorRange=[
                            [250, 224, 228],
                            [247, 202, 208],
                            [249, 190, 199],
                            [251, 177, 189],
                            [255, 153, 172],
                            [255, 133, 161],
                            [255, 112, 150],
                            [255, 92, 138],
                            [255, 71, 126],
                            [255, 10, 84]
                        ],
                        # heat map's color intensity
                        intensity=10,
                    ),
                ],
            )
        )

    # FILTER DATA FOR A SPECIFIC HOUR, CACHE
    @st.cache_data
    def filterdata(df, hour_selected):
        return df[df["datetime"].dt.hour == hour_selected]

    # STREAMLIT APP LAYOUT
    data = load_data()

    # LAYING OUT THE TOP SECTION OF THE APP
    row1_1, row1_2 = st.columns((2, 3))

    # A STATEFUL URL WITH A SPECIFIC HOUR SELECTED,
    if not st.session_state.get("url_synced", False):
        try:
            tweets = int(st.experimental_get_query_params()["tweets"][0])
            st.session_state["tweets"] = tweets
            st.session_state["url_synced"] = True
        except KeyError:
            pass

    # IF THE SLIDER CHANGES, UPDATE THE QUERY PARAM
    def update_query_params():
        hour_selected = st.session_state["tweets"]
        st.experimental_set_query_params(tweets=hour_selected)

    with st.sidebar:
        st.title("Drag the slider to display data within different hour ranges (in 24-hour format).")
        hour_selected = st.slider(
            "Select hour of pickup", 0, 23, key="tweets", on_change=update_query_params
        )
        st.write(
            f"""<div style='text-align: center; font-size: 24px'><b>Selected Hour</b></div>
                <div style='text-align: center; font-size: 48px'>{hour_selected}:00</div>""",
            unsafe_allow_html=True,
        )

    with row1_1:
        st.title("🐨📈 Aussie Tweets & Happiness: Mapping the Emotional Landscape of Australia")

    with row1_2:
        st.write(
            """
        ##
        On this page, we take a deep dive into the emotional landscape of Australia by analyzing tweets from different regions and performing sentiment analysis. 
        By examining the language used in tweets related to happiness and well-being, we aim to map out how different areas of Australia fare in terms of overall happiness. 
        Our interactive dashboard allows users to explore these findings in real-time, with the ability to filter by region and time period. 
        With this data, we hope to gain a better understanding of what contributes to the overall happiness of Australians and shed light on potential areas for improvement.
        """
        )

    # LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
    row2_1, row2_2, row2_3, row2_4 = st.columns((1, 1, 1, 1))

    # SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
    melbourne = [-37.871, 145.011]
    sydney = [-33.879, 151.214]
    brisbane = [-27.479, 153.028]
    adelaide = [-34.935, 138.601]
    zoom_level = 8

    with row2_1:
        st.write(
            f"""**Melbourne tweets from {hour_selected}:00 to {(hour_selected + 1) % 24}:00**"""
        )
        map(filterdata(data, hour_selected), melbourne[0], melbourne[1], zoom_level)

    with row2_2:
        st.write(
            f"""**Sydney tweets from {hour_selected}:00 to {(hour_selected + 1) % 24}:00**"""
        )
        map(filterdata(data, hour_selected), sydney[0], sydney[1], zoom_level)

    with row2_3:
        st.write(
            f"""**Brisbane tweets from {hour_selected}:00 to {(hour_selected + 1) % 24}:00**"""
        )
        map(filterdata(data, hour_selected), brisbane[0], brisbane[1], zoom_level)

    with row2_4:
        st.write(
            f"""**Adelaide tweets from {hour_selected}:00 to {(hour_selected + 1) % 24}:00**"""
        )
        map(filterdata(data, hour_selected), adelaide[0], adelaide[1], zoom_level)

    # another row
    row3_1, row3_2, row3_3, row3_4 = st.columns((1, 1, 1, 1))

    # SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
    perth = [-31.996, 115.872]
    hobart = [-42.906, 147.343]
    darwin = [-12.433, 130.875]
    canberra = [-35.359, 149.116]
    zoom_level = 8

    with row3_1:
        st.write(
            f"""**Perth tweets from {hour_selected}:00 to {(hour_selected + 1) % 24}:00**"""
        )
        map(filterdata(data, hour_selected), perth[0], perth[1], zoom_level)

    with row3_2:
        st.write(
            f"""**Hobart tweets from {hour_selected}:00 to {(hour_selected + 1) % 24}:00**"""
        )
        map(filterdata(data, hour_selected), hobart[0], hobart[1], zoom_level)

    with row3_3:
        st.write(
            f"""**Darwin tweets from {hour_selected}:00 to {(hour_selected + 1) % 24}:00**"""
        )
        map(filterdata(data, hour_selected), darwin[0], darwin[1], zoom_level)

    with row3_4:
        st.write(
            f"""**ACT(canberra) tweets from {hour_selected}:00 to {(hour_selected + 1) % 24}:00**"""
        )
        map(filterdata(data, hour_selected), canberra[0], canberra[1], zoom_level)


    st.title("Sentiment Analysis")
    row5_1, row5_2 = st.columns((1, 1))

    # sentiment data loading
    sentiment_data = filterdata(data, hour_selected).groupby(["sentiment", "city"])
    def add_markers_to_map(grouped_data, sentiment, city, map_object):
        data_to_plot = grouped_data.get_group((sentiment, city))
        for _, row in data_to_plot.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                icon=None,
                popup=f"Sentiment: {sentiment}<br>Time: {row['datetime']}",
            ).add_to(map_object)

    with row5_1:
        # Create a map with two side-by-side layers
        def create_side_by_side_map(grouped_data, sentiment, city):
            # '1gsyd', '2gmel', '3gbri', '4gade', '5gper', '6ghob', '7gdar', '8acte'
            # melbourne = [-37.871, 145.011]
            # sydney = [-33.879, 151.214]
            # brisbane = [-27.479, 153.028]
            # adelaide = [-34.935, 138.601]
            # perth = [-31.996, 115.872]
            # hobart = [-42.906, 147.343]
            # darwin = [-12.433, 130.875]
            # canberra = [-35.359, 149.116]
            if city == "1gsyd":
                m = folium.Map(location=(-33.879, 151.214), zoom_start=10, dragging=False)
            elif city == "2gmel":
                m = folium.Map(location=(-37.871, 145.011), zoom_start=10, dragging=False)
            elif city == "3gbri":
                m = folium.Map(location=(-27.479, 153.028), zoom_start=10, dragging=False)
            elif city == "4gade":
                m = folium.Map(location=(-34.935, 138.601), zoom_start=10, dragging=False)
            elif city == "5gper":
                m = folium.Map(location=(-31.996, 115.872), zoom_start=10, dragging=False)
            elif city == "6ghob":
                m = folium.Map(location=(-42.906, 147.343), zoom_start=10, dragging=False)
            elif city == "7gdar":
                m = folium.Map(location=(-12.433, 130.875), zoom_start=10, dragging=False)
            elif city == "8acte":
                m = folium.Map(location=(-35.359, 149.116), zoom_start=10, dragging=False)


            layer_left = folium.TileLayer(
                tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.{ext}',
                attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                subdomains='abcd',
                min_zoom=0,
                max_zoom=18,
                ext='png',
                name='Stamen Terrain',
                control=False
            )

            layer_right= folium.TileLayer(
                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
                name='Esri World Imagery',
                control=False
            )

            # Instantiate the SideBySideLayers class
            sbs = folium.plugins.SideBySideLayers(layer_left=layer_left, layer_right=layer_right)

            layer_left.add_to(m)
            layer_right.add_to(m)
            sbs.add_to(m)

            # Add a mouse position control
            mouse_position = plugins.MousePosition()
            mouse_position.add_to(m)

            # Add a draw control with polygon mode to disable map dragging
            draw_control = Draw(draw_options={'polygon': {'allowIntersection': False, 'drawError': {'color': '#e1e100',
                                                                                                    'message': 'Invalid polygon shape'}}},
                                edit_options={'polygon': {'allowIntersection': False}})
            draw_control.add_to(m)

            # Add map dragging functionality to the left control
            left_control = plugins.Fullscreen(position='topleft')
            left_control.add_to(m)

            add_markers_to_map(grouped_data, sentiment, city, m)
            return m

        sentiment_options = ["positive", "negative"]
        selected_sentiment = st.selectbox("Choose Sentiment:", sentiment_options)
        city_options = {
            '1gsyd': 'Sydney🌉',
            '2gmel': 'Melbourne🎨',
            '3gbri': 'Brisbane☀️',
            '4gade': 'Adelaide🍷',
            '5gper': 'Perth🏖️',
            '6ghob': 'Hobart⛵',
            '7gdar': 'Darwin🌴',
            '8acte': 'Canberra🏛️'
        }
        selected_city = st.selectbox("Choose City:", list(city_options.keys()), format_func=lambda x: city_options[x])

        side_by_side_map = create_side_by_side_map(sentiment_data, selected_sentiment, selected_city)
        folium_static(side_by_side_map)


    # FILTER DATA BY HOUR
    @st.cache_data
    def histdata(df, hr, sentiment):
        filtered = df[
            (df["sentiment"] == sentiment) &
            (df["datetime"].dt.hour >= hr) &
            (df["datetime"].dt.hour < (hr + 1))
            ]

        hist = np.histogram(filtered["datetime"].dt.minute, bins=60, range=(0, 60))[0]

        hist_data = pd.DataFrame({"minute": range(60), "tweets": hist})
        return hist_data

    # 根据所选城市过滤数据
    def filter_data_by_city(grouped_data, city):
        return grouped_data.filter(lambda x: x.name[1] == city)

    with row5_2:
        # 计算柱状图数据
        chart_data_positive = histdata(filter_data_by_city(sentiment_data, selected_city), hour_selected,
                                       sentiment='positive')
        chart_data_negative = histdata(filter_data_by_city(sentiment_data, selected_city), hour_selected,
                                       sentiment='negative')

        # 显示负向情感柱状图
        city_name = city_options[selected_city]

        # 显示正向情感柱状图
        st.write(
            f"""<div style='text-align: center'><b>{city_name}'s {hour_selected}:00 to {(hour_selected + 1) % 24}:00 - 😃 - POSITIVE tweets distribution (minutes)</b></div>""",
            unsafe_allow_html=True,
        )

        st.altair_chart(
            alt.Chart(chart_data_positive)
            .mark_area(
                interpolate="step-after",
            )
            .encode(
                x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
                y=alt.Y("tweets:Q"),
                tooltip=["minute", "tweets"],
            )
            .configure_mark(opacity=0.2, color="pink"),
            use_container_width=True,
        )

        st.write(
            f"""<div style='text-align: center'><b>{city_name} {hour_selected}:00 to {(hour_selected + 1) % 24}:00 - 😔 - NEGATIVE tweets distribution (minutes)</b></div>""",
            unsafe_allow_html=True,
        )

        st.altair_chart(
            alt.Chart(chart_data_negative)
            .mark_area(
                interpolate="step-after",
            )
            .encode(
                x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
                y=alt.Y("tweets:Q"),
                tooltip=["minute", "tweets"],
            )
            .configure_mark(opacity=0.2, color="green"),
            use_container_width=True,
        )