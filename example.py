'''Script creates examples of visualisations for dashboard.'''
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import random
from datetime import datetime, timedelta, timezone

def create_pollutants_map():
    '''Creates a map which shows pollutant level by country.'''
    fig = px.choropleth(
        filtered_df, locations='Country', color='AQI',
        locationmode='country names',
        projection='orthographic', range_color=[0, 200],
        title=f'AQI Distribution for {selected_pollutant}',
        scope='world'
    )

    return fig

def create_overall_eq_map():
    '''Creates a map which shows all points where earthquakes have occured with magnitude.'''
    df = pd.DataFrame(data)
    fig = px.density_mapbox(df, lat='lat', lon='lon', z='Magnitude', radius=10,
                            center=dict(lat=0, lon=180), zoom=0,
                            mapbox_style="open-street-map")
    return fig

def air_reading_time():
    fig = px.histogram(df, x="Timestamp", y="AQI", color="Pollutant", title="Air Reading vs. Time",
                   labels={'AQI': 'Air Quality Index (AQI)', 'Timestamp': 'Timestamp'})
    return fig

if __name__ == "__main__":
    #------------------ SIMULATED DATA-----------------------
    data = {'lat': [37.7749, 40.7128, 34.0522],
        'lon': [-122.4194, -74.0060, -118.2437],
        'Magnitude': [1, 2, 3]}

    df = pd.DataFrame(data)
    
    #------------------ END SIMULATED DATA-----------------------
    eq_map = create_overall_eq_map()

    #------------------ SIMULATED DATA-----------------------
    np.random.seed(42)

    pollutants = ['Carbon Monoxide', 'Sulfur Dioxide', 'Nitrogen Dioxide', 'Ozone', 'Particulate Matter (PM2.5)', 'Lead']
    symbols = ['CO', 'SO2', 'NO2', 'O3', 'PM2.5', 'Pb']
    countries = ['USA', 'China', 'India', 'Brazil', 'Germany', 'Australia']

    # Generating random AQI values for each pollutant in each country
    data = {'Pollutant': [], 'Symbol': [], 'AQI': [], 'Country': []}

    for country in countries:
        for pollutant, symbol in zip(pollutants, symbols):
            aqi_values = np.random.randint(0, 200, size=1)[0] 
            data['Pollutant'].append(pollutant)
            data['Symbol'].append(symbol)
            data['AQI'].append(aqi_values)
            data['Country'].append(country)


    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime('now') - pd.to_timedelta(np.random.randint(1, 365, size=len(df)), 'D')
    
    #------------------ END SIMULATED DATA-----------------------


    st.title('Chemical Pollutant AQI Analysis')
    selected_pollutant = st.selectbox("Select a pollutant:", pollutants, index=1)

    filtered_df = df[df['Pollutant'] == selected_pollutant]

    pollutants_map = create_pollutants_map()
    air_qual_map = air_reading_time()

    
    st.plotly_chart(pollutants_map)
    st.title('Earthquake Magnitude.')
    st.plotly_chart(eq_map)
    st.title('Air reading by time.')
    st.plotly_chart(air_qual_map)
    
    