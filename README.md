# Supplychain Visualization Node

## Overview

This is a custom node for KNIME designed to visualize supply chain data on a choropleth map using Plotly and geospatial data. It takes an input table with supply chain information and creates an interactive map displaying the flow of goods between countries.

## Features

- Input supply chain data with columns for origin, destination, and value.
- Visualization of the supply chain on an interactive choropleth map.
- Custom color-coding of countries to distinguish them.
- Arrow visualization to represent the flow of goods.
- Integration with geospatial data to obtain latitude and longitude coordinates of countries.

## Dependencies

- KNIME: Ensure you have KNIME installed.
- Python Libraries: Make sure the required Python libraries are installed. You can install them using pip:
pip install pandas knime-extension numpy plotly pycountry geopy

## Usage

1. Open KNIME and create a workflow.

2. Add the "Supplychain Visualization Node" to your workflow.

3. Configure the node by connecting it to your input data table.

4. Run the workflow.

5. The node will generate an interactive choropleth map showing the supply chain data.

## Configuration

- **Input Data**: Connect the node to your supply chain data table.

- **Output Data**: The node outputs the supply chain data with additional columns for visualization.

- **Output View**: View the visualization on the node's output view.

## Troubleshooting

- If the input table has zero columns, a warning message will be displayed, and no visualization will be generated.

## License

This code is provided under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

## Author

Octavio Mesa-Varona, Luka Filipovic and Lars Valentin

## Contact

For questions or issues, please contact 4sz@bfr.bund.de.
