
import time
import pandas as pd
import knime.extension as knext
import numpy as np
import logging
import plotly.graph_objects as go
import pycountry
from geopy.geocoders import Nominatim
LOGGER = logging.getLogger(__name__)


category = knext.category("/community", "Supply_chain_visualization_node", "Supplychain visualization node", "Supplychain visualization node for KNIME",icon="icons/icon.png")		
@knext.node(name="Supplychain visualization node", node_type=knext.NodeType.LEARNER, category=category, icon_path="icons/icon.png")	
@knext.input_table(name="Input Data 1",description="Input data")
@knext.output_table(name="Output Data",  description="Output data")
@knext.output_view(name="Output view", description="Output view")

class TemplateNode:
    def configure(self, configure_context, input_schema_1):
        return input_schema_1

    def execute(self, exec_context, input_1):
        df = input_1.to_pandas() # Transform the input table to some processable format (pandas or pyarrow)

        df = df.rename(columns={'Country (from)': 'C_From', 'Country (to)': 'C_To', 'Value (thousands of €)' : 'Value' })

        countries = pd.concat([df['C_From'], df['C_To']], axis=0, ignore_index=True)
        countries = pd.DataFrame(countries)
        countries.columns = ['Name']
        
        countries.drop_duplicates(inplace=True)





        # Apply function to DataFrame to get latitude and longitude for each country
        countries['Latitude'], countries['Longitude'] = zip(*countries['Name'].apply(get_lat_long))

        countries['Country_Code'] = countries['Name'].apply(get_country_code)

        country_code_array = np.array(countries['Country_Code'])
        country_name_array = np.array(countries['Name'])


        country_colour=[]
        broj_drzava = len(country_code_array)
        for i in range(0,broj_drzava):
            country_colour.append(i)




        countries = countries.set_index('Name')
        df['Value_Normalized']=round(df['Value']*10/max(df['Value']))+1



        import plotly.graph_objects as go

        # Define your data for the choropleth map
        data = [
            go.Choropleth(
                locations=country_code_array,  # Country codes or names
                z=country_colour,  # Values for coloring the map
                text=country_name_array,  # Country names
                # colorscale='Blues',  # Color scale for the map
                autocolorscale=False,  # Disable automatic scaling of colors
                showscale=False,  # Hide the color scale legend
                # geojson='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'  # GeoJSON file URL
            )
        ]

        # Define the layout of the figure
        layout = go.Layout(
            title='Supplychain visualization',
            geo=dict(
                showframe=True,  # Show the frame around the map
                showcoastlines=True,  # Show coastlines
                projection_type='natural earth'  # Set the projection type
            )
        )

        # Create the figure
        fig = go.Figure(data=data, layout=layout)

        # Display the figure
        # fig.show()


        for index, row in df.iterrows():
            c_from = row['C_From']
            c_to = row['C_To']
            c_th = row['Value_Normalized']
           
            # Introduce a delay between geocoding requests
            time.sleep(1)  # Wait for a second before each geocoding request
    
            nacrtaj_arrow(fig, countries, c_from, c_to, c_th)

        fig.update_layout(
            # width=900, height=650,
                showlegend = False,
                geo = dict(
                    scope = 'world',
                    
                    # landcolor = 'rgb(217, 217, 217)'
                    )
                    )





        # x = input_1_pandas.to_html()

        x = countries.to_html()

        # return knext.Table.from_pandas(input_1_pandas), knext.view(input_1_pandas) ### Tutorial step 13: Uncomment
        # return knext.Table.from_pandas(df), knext.view_html(x) ### Tutorial step 13: Uncomment
        return knext.Table.from_pandas(df), knext.view(fig)  ### Tutorial step 13: Uncomment
        


# Define function to get latitude and longitude for a country

def _code(country_name):
    country = pycountry.countries.get(name=country_name.upper())
    if country:
        return country.alpha_3
    else:
        LOGGER.warning(f"Country code not found for {country_name}. Skipping this country.")
        return None

   

# Define function to get latitude and longitude for a country
# Modify get_lat_long function
def get_lat_long(country):
    geolocator = Nominatim(user_agent="my_app")
    try:
        location = geolocator.geocode(country, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            LOGGER.warning(f"Location not found for country: {country}")
            return (None, None)
    except GeocoderTimedOut:
        LOGGER.warning(f"Geocoding request timed out for country: {country}")
        return (None, None)


# Modify get_country_code function
def get_country_code(country_name):
    country = pycountry.countries.get(name=country_name.upper())
    if country:
        return country.alpha_3
    else:
        LOGGER.warning(f"Country code not found for: {country_name}. Skipping this country.")
        return None


def nacrtaj_arrow(fig, countries, c1, c2, thickness):
    fig.add_trace(go.Scattergeo(
        lat = [countries.loc[c1][0], countries.loc[c2][0]], 
        lon = [countries.loc[c1][1], countries.loc[c2][1]],
        mode = 'lines',
        
        line = dict(width = thickness, color = 'blue'),
    ))

    #Workaround to get the arrow at the end of an edge AB

    l = 1.1  # the arrow length
    widh =  0.035  #2*widh is the width of the arrow base as triangle

    B = np.array([countries.loc[c2][1], countries.loc[c2][0]])
    A = np.array([countries.loc[c1][1], countries.loc[c1][0]])
    # A = np.array([locations['lon'][4], locations['lat'][4]])
    # B = np.array([locations['lon'][0], locations['lat'][0]])
    v = B-A
    w = v/np.linalg.norm(v)  
    # u = np.array([-v[1], v[0]])  #u orthogonal on  w
    u = np.array([-w[1], w[0]])*10
            
    P = B-l*w
    S = P - widh*u
    T = P + widh*u

    fig.add_trace(go.Scattergeo(lon = [S[0], T[0], B[0], S[0]], 
                                lat =[S[1], T[1], B[1], S[1]], 
                                mode='lines', 
                                fill='toself', 
                                fillcolor='blue', 
                                line_color='blue'))
    # #------Display your text at the middle of the segment AB
    # fig.add_trace(go.Scattergeo(lon =[0.5*(A+B)[0]], lat = [0.5*(A+B)[1]], mode='text', text='Your text'))
    
