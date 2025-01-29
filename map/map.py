import pandas as pd
import plotly.express as px

# Load the metadata
metadata = pd.read_excel('Data/Metadata.xlsx')

# Count isolates by country for map shading
isolates_by_country = metadata.groupby('Country')['Final Id'].count().reset_index()
isolates_by_country.columns = ['Country', 'Isolate_Count']

# Create the map
map_fig = px.choropleth(
    isolates_by_country,
    locations="Country",
    locationmode="country names",
    color="Isolate_Count",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Greens
)

# Show the map
map_fig.show()

#Save the map
map_fig.write_html('Outputs/map.html')
