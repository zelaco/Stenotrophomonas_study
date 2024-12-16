import pandas as pd
import plotly.express as px
import argparse

def generate_map(metadata_file, output_file):
    # Load the updated metadata
    metadata = pd.read_excel(metadata_file)

    # Count isolates by country for map shading
    isolates_by_country = metadata.groupby('Country')['Final Id'].count().reset_index()
    isolates_by_country.columns = ['Country', 'Isolate_Count']

    # Create the map using Plotly Express
    map_fig = px.choropleth(
        isolates_by_country,
        locations="Country",
        locationmode="country names",
        color="Isolate_Count",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Greens
    )

    # Save the map
    map_fig.write_html(output_file)
    print(f"Map saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a choropleth map of isolates by country.")
    parser.add_argument("--metadata", required=True, help="Path to the metadata Excel file.")
    parser.add_argument("--output", required=True, help="Path to save the HTML map.")
    args = parser.parse_args()

    generate_map(args.metadata, args.output)
