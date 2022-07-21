import matplotlib.patches as patches
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from import_data import load_data
import plotly.express as px
import plotly.figure_factory as ff
import pydeck as pdk
from geopy.geocoders import Nominatim
from datetime import timedelta
import time

st.cache()
df = load_data()

def load_dashobard():

    # Project Heading
    st.title('Delivery Route Dashboard')
    st.header('')
    st.header('')

    with st.spinner('processing...'):
        time.sleep(5)
    # st.success('Done!')

    # Get metrics
    get_metrics()
    

    dashboard = st.radio('Select Dashboard', ['Areas Covered','Analysis Dashboard','Vehicle Movement'], horizontal=True)

    if dashboard == 'Areas Covered':
        # st.info('Visualize the all delivery areas covered')

        # Plot the areas covered
        plot_area_covered()

    elif dashboard == 'Vehicle Movement':
        # visualize vehicle movement
        st.header('')
        # st.info('Plot pretty visuals of vehicle movements from pickup to delivery')
        visualize_vehicle_movement()

    elif dashboard == 'Analysis Dashboard':
        analysis_dashboard()

def get_metrics():
    on_time = round(df[df['actual_eta'] < df['planned_eta']].shape[0]/df.shape[0], 4)*100
    
    # metrics
    met1, met2, met3 = st.columns(3)
    met1.metric('Total Number of Rides', str(df.shape[0]))
    met2.metric('Early Completion Rate', str(on_time)+'%', 0)
    met3.metric('Most Distance Covered', str(df['transportation_distance_in_km'].max())+'km')


def plot_area_covered():
    # Create columns
    dest = df[['des_lon', 'des_lat']]
    dest.columns = ['lon', 'lat']
    st.map(dest)


# vehicles_df = pd.DataFrame()
# for vehicle_no in vehicle_nos:
#     vdf = df[df['vehicle_no'] == vehicle_no]
#     vehicles_df = pd.concat([vehicles_df, vdf], axis=0)

def get_vehicle_no():
    col1, col2  = st.columns(2)
    with col1:
        vehicle_no = st.selectbox('Vehicle Number', df['vehicle_no'].unique())
    
    # find data with vehicle no
    with col2:
        vehicles_df = df[df['vehicle_no'] == vehicle_no].sort_values(by='trip_start_date')
        min_value = list(pd.to_datetime(vehicles_df.iloc[:1]['trip_start_date']))[0]
        max_value =  pd.to_datetime(vehicles_df.iloc[-1]['trip_start_date'])

        trip_dates = st.date_input('Trip Dates',\
                                    value = min_value,\
                                    max_value = max_value,
                                    min_value=min_value)

        vehicles_dfs = vehicles_df[vehicles_df['trip_start_date'] == str(min_value)]

    return vehicles_dfs


def visualize_vehicle_movement():

    vehicle_nos = get_vehicle_no()
    st.dataframe(vehicle_nos)
    # Define a layer to display on a map
    layer = pdk.Layer(
        "GreatCircleLayer",
        vehicle_nos,
        get_stroke_width=12,
        get_source_position=['org_lon', 'org_lat'],
        get_target_position=['des_lon', 'des_lat'],
        get_source_color=[168, 66, 50],
        get_target_color=[95, 168, 50],
        
        elevation_scale=500,
        pickable=False,
        elevation_range=[0, 3000],
        extruded=True,
        coverage=1,
    )

    # Set the viewport location
    zoom = 4 
    view_state = pdk.ViewState(latitude=18.75, longitude=78.3, zoom=zoom, bearing=10, pitch=10)

    # Render
    geolocator = Nominatim(user_agent="Route Optimizer")
    # location = geolocator.reverse(f"{vehicle_nos['curr_lon']}, {vehicle_nos['curr_lat']}")
    # # st.write(f'**Current Location:** {location.address}')

    deck = pdk.Deck(layers=[layer], 
                    initial_view_state=view_state, 
                    )
    st.pydeck_chart(deck)


    if vehicle_nos.shape[0]>0:
        st.write('###### vehicle details')
        st.dataframe(vehicle_nos, height=100)

def feature_engine():
    df['bookingid_month'] = pd.to_datetime(df['bookingid_date']).dt.month
    df['bookingid_day'] = pd.to_datetime(df['bookingid_date']).dt.day
    df['bookingid_weekday'] = pd.to_datetime(df['bookingid_date']).dt.weekday
    df['bookingid_year'] = pd.to_datetime(df['bookingid_date']).dt.year


    
def analysis_dashboard():
    feature_engine()
    
    col1, col2 = st.columns(2)

    with col1:
        weekly_request = df.groupby('bookingid_day')['bookingid'].count()
        weekly_request = weekly_request.reset_index()
        weekly_request_fig = px.line(data_frame=weekly_request, x='bookingid_day', y='bookingid', \
                                    title='Daily Delivery', 
                                    range_x=[1,31])
        st.plotly_chart(weekly_request_fig)

    with col2:

        week_day_request = df.groupby('bookingid_weekday')['bookingid'].count()
        week_day_request_fig = px.area(x=['Mon','Tue','Wed','Thur','Fri','Sat','Sun'],\
                                    y= week_day_request, title='Weekday Delivery')
        st.plotly_chart(week_day_request_fig)


    col3, col4 = st.columns(2)

    with col3:
        monthly_request = df.groupby('bookingid_month')['bookingid'].count()
        monthly_request_fig = px.bar(x=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec'], 
                                    y=monthly_request, title='Monthly Delivery Request')

        st.plotly_chart(monthly_request_fig)

    with col4:
        yearly_request = df.groupby('bookingid_year')['bookingid'].count()
        yearly_request_fig = px.bar(data_frame=yearly_request.reset_index(), \
                                    x=yearly_request.reset_index().bookingid_year, \
                                    y=yearly_request.reset_index().bookingid, \
                                    title='Yearly Requests')
        st.plotly_chart(yearly_request_fig)


