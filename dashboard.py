from turtle import color, heading
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from import_data import load_data
import plotly.express as px
import plotly.figure_factory as ff

st.cache
df = load_data()

def load_dashobard():

    # Project Heading
    st.title('Delivery Route Dashboard')
    st.header('')
    st.header('')

    on_time = round(df[df['actual_eta'] < df['planned_eta']].shape[0]/df.shape[0], 4)*100

    # metrics
    met1, met2, met3 = st.columns(3)
    met1.metric('Total Number of Rides', str(df.shape[0]))
    met2.metric('Early Completion Rate', str(on_time)+'%', 0)
    met3.metric('Most Distance Covered', str(df['transportation_distance_in_km'].max())+'km')



    # Create columns
    st.write("Areas Covered")
    dest = df[['des_lon', 'des_lat']]
    dest.columns = ['lon', 'lat']
    st.map(dest)

    st.write("Requests by Location")
    dev_request = df.groupby(['des_lon','des_lat'])['bookingid'].count()
    # st.dataframe(dev_request)

    dev_request = alt.Chart(dev_request.reset_index()).mark_circle().encode(
        x='des_lon', y='des_lat', size='bookingid')

    st.altair_chart(dev_request, use_container_width=True)
    px.scatter_mapbox(df, lat='des_lat', lon='des_lon')