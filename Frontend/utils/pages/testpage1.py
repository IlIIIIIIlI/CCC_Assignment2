import folium
from folium import plugins
from folium.plugins import Draw, Fullscreen
import streamlit as st
import streamlit_folium as sf
from streamlit_folium import folium_static

# def testpage1():
#     st.title('Side-by-Side Map Comparison')

#     # Create a map with two side-by-side layers
#     def create_side_by_side_map():
#         m = folium.Map(location=(30, 20), zoom_start=4)
#
#         layer_right = folium.TileLayer('openstreetmap', name='OpenStreetMap', control=False)
#         layer_left = folium.TileLayer('cartodbpositron', name='CartoDB Positron', control=False)
#
#         # Instantiate the SideBySideLayers class
#         sbs = folium.plugins.SideBySideLayers(layer_left=layer_left, layer_right=layer_right)
#
#         layer_left.add_to(m)
#         layer_right.add_to(m)
#         sbs.add_to(m)
#
#         # Add a mouse position control
#         mouse_position = plugins.MousePosition()
#         mouse_position.add_to(m)
#
#         # Add a draw control with polygon mode to disable map dragging
#         draw_control = Draw(draw_options={'polygon': {'allowIntersection': False, 'drawError': {'color': '#e1e100', 'message': 'Invalid polygon shape'}}}, edit_options={'polygon': {'allowIntersection': False}})
#         draw_control.add_to(m)
#
#         # Add map dragging functionality to the left control
#         left_control = plugins.Fullscreen(position='topleft')
#         left_control.add_to(m)
#
#         return m
#
#     # Create the side-by-side map and display it using Streamlit
#     side_by_side_map = create_side_by_side_map()
#     folium_static(side_by_side_map)


# -*- coding: utf-8 -*-

"""An example of showing geographic data."""
import os
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MousePosition, Draw, Fullscreen
def testpage1():
    # LOAD DATA ONCE
    @st.cache_resource
    def load_data():
        path = "./utils/data/uber-raw-data-sep14.csv.gz"
        if not os.path.isfile(path):
            path = f"https://github.com/streamlit/demo-uber-nyc-pickups/raw/main/{path}"

        data = pd.read_csv(
            path,
            nrows=100000,  # approx. 10% of data
            names=[
                "date/time",
                "lat",
                "lon",
            ],  # specify names directly since they don't change
            skiprows=1,  # don't read header since names specified directly
            usecols=[0, 1, 2],  # doesn't load last column, constant value "B02512"
            parse_dates=[
                "date/time"
            ],  # set as datetime instead of converting after the fact
        )

        return data


    # FUNCTION FOR AIRPORT MAPS
    # FUNCTION FOR AIRPORT MAPS
        def map(data, lat, lon, zoom):
            m = folium.Map(location=[lat, lon], zoom_start=zoom)

            folium.plugins.Fullscreen(position='topleft').add_to(m)
            folium.TileLayer('cartodbpositron').add_to(m)
            folium.TileLayer('openstreetmap').add_to(m)

            folium.plugins.MousePosition(
                position='bottomleft',
                separator=' | ',
                empty_string='NaN',
                lng_first=True,
                num_digits=20,
                prefix='Coordinates:'
            ).add_to(m)

            folium.plugins.Draw(
                export=True,
                filename='draw_data',
                position='topleft',
                draw_options={
                    'polygon': {
                        'allowIntersection': False,
                        'drawError': {
                            'color': '#e1e100',
                            'message': 'Invalid polygon shape'
                        }
                    },
                    'polyline': False,
                    'circle': False,
                    'rectangle': False,
                    'marker': False,
                    'circlemarker': False
                },
                edit_options={
                    'poly': {
                        'allowIntersection': False
                    }
                }
            ).add_to(m)

            folium.plugins.SideBySideLayers(
                position='topleft',
                layer_left=folium.FeatureGroup(name='Mapbox Satellite Streets V12').add_to(m),
                layer_right=folium.FeatureGroup(name='Mapbox Dark').add_to(m)
            ).add_to(m)

            hexagon_layer = folium.plugins.HeatMap(
                data=data[['lat', 'lon']].values,
                name='Hexagon Layer',
                control=True,
                show=True,
                radius=100,
                min_opacity=0.2,
                max_zoom=10,
                blur=50,
                gradient=None,
                overlay=True,
                control_opacity=True,
                control_radius=True,
                fill_color='red',
                line_color='red',
                popup=None,
                tooltip=None,
                weight=1
            ).add_to(m)

            return m



    # FILTER DATA FOR A SPECIFIC HOUR, CACHE
    @st.cache_data
    def filterdata(df, hour_selected):
        return df[df["date/time"].dt.hour == hour_selected]


    # CALCULATE MIDPOINT FOR GIVEN SET OF DATA
    @st.cache_data
    def mpoint(lat, lon):
        return (np.average(lat), np.average(lon))


    # FILTER DATA BY HOUR
    @st.cache_data
    def histdata(df, hr):
        filtered = data[
            (df["date/time"].dt.hour >= hr) & (df["date/time"].dt.hour < (hr + 1))
        ]

        hist = np.histogram(filtered["date/time"].dt.minute, bins=60, range=(0, 60))[0]

        return pd.DataFrame({"minute": range(60), "pickups": hist})


    # STREAMLIT APP LAYOUT
    data = load_data()

    # LAYING OUT THE TOP SECTION OF THE APP
    row1_1, row1_2 = st.columns((2, 3))

    # SEE IF THERE'S A QUERY PARAM IN THE URL (e.g. ?pickup_hour=2)
    # THIS ALLOWS YOU TO PASS A STATEFUL URL TO SOMEONE WITH A SPECIFIC HOUR SELECTED,
    # E.G. https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/main?pickup_hour=2
    if not st.session_state.get("url_synced", False):
        try:
            pickup_hour = int(st.experimental_get_query_params()["pickup_hour"][0])
            st.session_state["pickup_hour"] = pickup_hour
            st.session_state["url_synced"] = True
        except KeyError:
            pass


    # IF THE SLIDER CHANGES, UPDATE THE QUERY PARAM
    def update_query_params():
        hour_selected = st.session_state["pickup_hour"]
        st.experimental_set_query_params(pickup_hour=hour_selected)


    with row1_1:
        st.title("NYC Uber Ridesharing Data")
        hour_selected = st.slider(
            "Select hour of pickup", 0, 23, key="pickup_hour", on_change=update_query_params
        )


    with row1_2:
        st.write(
            """
        ##
        Examining how Uber pickups vary over time in New York City's and at its major regional airports.
        By sliding the slider on the left you can view different slices of time and explore different transportation trends.
        """
        )

    # LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
    row2_1, row2_2, row2_3, row2_4 = st.columns((2, 1, 1, 1))

    # SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
    la_guardia = [40.7900, -73.8700]
    jfk = [40.6650, -73.7821]
    newark = [40.7090, -74.1805]
    zoom_level = 12
    midpoint = mpoint(data["lat"], data["lon"])

    with row2_1:
        st.write(
            f"""**All New York City from {hour_selected}:00 and {(hour_selected + 1) % 24}:00**"""
        )
        map(filterdata(data, hour_selected), midpoint[0], midpoint[1], 11)

    with row2_2:
        st.write("**La Guardia Airport**")
        map(filterdata(data, hour_selected), la_guardia[0], la_guardia[1], zoom_level)

    with row2_3:
        st.write("**JFK Airport**")
        map(filterdata(data, hour_selected), jfk[0], jfk[1], zoom_level)

    with row2_4:
        st.write("**Newark Airport**")
        map(filterdata(data, hour_selected), newark[0], newark[1], zoom_level)

    # CALCULATING DATA FOR THE HISTOGRAM
    chart_data = histdata(data, hour_selected)

    # LAYING OUT THE HISTOGRAM SECTION
    st.write(
        f"""**Breakdown of rides per minute between {hour_selected}:00 and {(hour_selected + 1) % 24}:00**"""
    )

    st.altair_chart(
        alt.Chart(chart_data)
        .mark_area(
            interpolate="step-after",
        )
        .encode(
            x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
            y=alt.Y("pickups:Q"),
            tooltip=["minute", "pickups"],
        )
        .configure_mark(opacity=0.2, color="red"),
        use_container_width=True,
    )
