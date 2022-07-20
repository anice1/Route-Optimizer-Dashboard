import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from import_data import load_data
import plotly.express as px
import plotly.figure_factory as ff
import pydeck as pdk

st.cache()
df = load_data()

def load_dashobard():

    # Project Heading
    st.title('Delivery Route Dashboard')
    st.header('')
    st.header('')

    # Get metrics
    get_metrics()

    # Plot the areas covered
    plot_area_covered()

    # visualize vehicle movement
    visualize_vehicle_movement()

def get_metrics():
    on_time = round(df[df['actual_eta'] < df['planned_eta']].shape[0]/df.shape[0], 4)*100
    
    # metrics
    met1, met2, met3 = st.columns(3)
    met1.metric('Total Number of Rides', str(df.shape[0]))
    met2.metric('Early Completion Rate', str(on_time)+'%', 0)
    met3.metric('Most Distance Covered', str(df['transportation_distance_in_km'].max())+'km')


def plot_area_covered():
    # Create columns
    st.write("Areas Covered")
    dest = df[['des_lon', 'des_lat']]
    dest.columns = ['lon', 'lat']
    st.map(dest)

    
def get_vehicle_no():
    vehicle_nos = st.multiselect('Vehicle Number', df['vehicle_no'].unique())
    vehicles_df = pd.DataFrame()
    for vehicle_no in vehicle_nos:
        vdf = df[df['vehicle_no'] == vehicle_no]
        vehicles_df = pd.concat([vehicles_df, vdf], axis=0)
    return vehicles_df

def visualize_vehicle_movement():

    vehicle_nos = get_vehicle_no()
    st.selectbox('Trip Start Date', vehicle_nos['trip_start_date'])
    # Define a layer to display on a map
    layer = pdk.Layer(
        "GreatCircleLayer",
        vehicle_nos,
        pickable=True,
        get_stroke_width=12,
        get_source_position=['org_lon', 'org_lat'],
        get_target_position=['des_lon', 'des_lat'],
        get_source_color=[168, 66, 50],
        get_target_color=[95, 168, 50],
        auto_highlight=True,
    )

    # Set the viewport location
    view_state = pdk.ViewState(latitude=18.75, longitude=78.3, zoom=4, bearing=10)

    # Render
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))


    # ddf = pd.DataFrame(
    # np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    # columns=['lat', 'lon'])

    # st.pydeck_chart(pdk.Deck(
    #     map_style='mapbox://styles/mapbox/light-v9',
    #     initial_view_state=pdk.ViewState(
    #         latitude=37.76,
    #         longitude=-122.4,
    #         zoom=11,
    #         pitch=50,
    #     ),
    #     layers=[
    #         pdk.Layer(
    #             'HexagonLayer',
    #             data=ddf,
    #             get_position='[lon, lat]',
    #             radius=200,
    #             elevation_scale=4,
    #             elevation_range=[0, 1000],
    #             pickable=True,
    #             extruded=True,
    #         ),
    #         pdk.Layer(
    #             'ScatterplotLayer',
    #             data=ddf,
    #             get_position='[lon, lat]',
    #             get_color='[200, 30, 0, 160]',
    #             get_radius=200,
    #         ),
    #     ],
    # ))