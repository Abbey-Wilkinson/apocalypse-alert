import pandas as pd
import plotly.express as px

# Create a DataFrame with latitude, longitude, and magnitude columns
data = {'lat': [37.7749, 40.7128, 34.0522],
        'lon': [-122.4194, -74.0060, -118.2437],
        'Magnitude': [1, 2, 3]}

df = pd.DataFrame(data)

# Create a density map using Plotly Express
fig = px.density_mapbox(df, lat='lat', lon='lon', z='Magnitude', radius=10,
                        center=dict(lat=0, lon=180), zoom=0,
                        mapbox_style="open-street-map")

# Show the figure
fig.show()