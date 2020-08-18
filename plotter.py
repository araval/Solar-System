import pandas as pd
import numpy as np
from planets import Planet

import plotly.express as px

import sys
import logging
log_format = '%(asctime)s|%(levelname)s| %(message)s'
logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.INFO)

def create_dataframe(time):
    """
    time: animation time in years (float)

    Returns 
    Dataframe with planet coordinates in reference frame of the ecliptic
    for <time> years. Dataframe columns include: 
    x, y, z: coordinates
    time: timestamp (integers for now, that are used to generate animation frames)
    Planet: name of the planet
    """
    df1 = pd.read_csv('planet_orbital_elements.csv')
    df2 = pd.read_csv('planet_elements.csv')

    df = df1.merge(df2, on='name')    

    dataframes = []
    for _, row in df.iterrows():
        logging.info("Creating dataframe for Planet {}".format(row['name']))
        planet = Planet(aphelion=row['aphelion_AU'], 
                        perihelion=row['perihelion_AU'], 
                        Omega = row['Omega_deg'],
                        i = row['inclination_deg'],
                        w = row['arg_periapsis_deg'],
                        orbital_period=row['period_years'],
                        time=time)
    
        logging.info("Calculating coordinates")
        planet_coordinates = planet.get_coordinates()
        planet_coordinates['timestamp'] = pd.Series([time for time in range(len(planet_coordinates))])

        planet_coordinates['Planet'] = row['name']
        #planet_coordinates['size'] = row.diameter_earths/10.0

        dataframes.append(planet_coordinates)

    all_planet_coordinates = pd.concat(dataframes)

    return all_planet_coordinates

def plot_with_plotly(coordinate_df):
    fig = px.scatter(coordinate_df, x="x", y="y", animation_frame="timestamp", animation_group="Planet",
           color="Planet", hover_name="Planet",
           size_max=55, template='plotly_dark', range_x=[-12, 12], range_y=[-12, 12], width=1000, height=1000)
    fig.show()

if __name__ == '__main__':
    all_planet_coordinates = create_dataframe(time=10)
    plot_with_plotly(all_planet_coordinates)
