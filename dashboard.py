'''Script creates examples of visualisations for dashboard.'''
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from earthquakes import get_eq_data_for_country, get_eq_json

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

def create_overall_eq_map(df):
    '''Creates a map which shows all points where earthquakes have occured with magnitude.'''
    dark_color_scale = px.colors.sequential.YlOrRd
    midpoint_value = df['mag'].max()
    fig = px.density_mapbox(df, lat='lat', lon='lng', z='mag', radius=10,
                            center=dict(lat=0, lon=180), zoom=0,
                            mapbox_style="carto-positron", hover_name=df['title'], color_continuous_scale=dark_color_scale, color_continuous_midpoint=midpoint_value)
    return fig

def air_reading_time():
    fig = px.histogram(df, x="Timestamp", y="AQI", color="Pollutant", title="Air Reading vs. Time",
                   labels={'AQI': 'Air Quality Index (AQI)', 'Timestamp': 'Timestamp'})
    return fig

def pollutant_count_by_country():
    fig = px.pie(pollutant_counts, names=pollutant_counts.index, values=pollutant_counts.values,
                title=f'Pollutant distribution in {selected_country}', color_discrete_sequence=['#0000FF', '#0072BD', '#4DBEEE'])
    return fig



if __name__ == "__main__":
    #------------------ API EQ DATA-----------------------

    #MAKES API REQUEST FOR JAPAN 
    country_searched = "Japan"
    json_data = get_eq_json(country_searched)
    df = get_eq_data_for_country(country_searched, json_data)
    
    #------------------ END EQ DATA-----------------------
    eq_map = create_overall_eq_map(df)

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

    st.plotly_chart(create_pollutants_map())
    st.subheader('Earthquake Distribution and Magnitude', divider='rainbow')
    st.plotly_chart(eq_map)
    st.subheader('Air quality vs. Time.', divider='rainbow')
    st.plotly_chart(air_reading_time())

    st.subheader('Pollutants by Country.', divider='rainbow')
    selected_country = st.selectbox("Select a country:", countries, index=1)
    filtered_df = df[df['Country'] == selected_country]
    pollutant_counts = filtered_df['Pollutant'].value_counts()
    st.plotly_chart(pollutant_count_by_country())
