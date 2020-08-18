import pandas as pd
import numpy as np
from planets import Planet

import plotly.express as px

import sys
import logging
log_format = '%(asctime)s|%(levelname)s| %(message)s'
logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.INFO)

def create_dataframe():
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
                        orbital_period=row['period_years'])
    
        logging.info("Calculating coordinates")
        planet_coordinates = planet.get_coordinates(time=10)
        planet_coordinates['time'] = pd.Series([time for time in range(len(planet_coordinates))])

        planet_coordinates['Planet'] = row['name']
        planet_coordinates['size'] = row.diameter_earths/10.0

        dataframes.append(planet_coordinates)

    all_planet_coordinates = pd.concat(dataframes)

    return all_planet_coordinates

if __name__ == '__main__':
    all_planet_coordinates = create_dataframe()
    fig = px.scatter(all_planet_coordinates, x="x", y="y", animation_frame="time", animation_group="Planet",
           color="Planet", hover_name="Planet",
           size_max=55, template='plotly_dark', range_x=[-12, 12], range_y=[-12, 12], width=1000, height=1000)
    fig.show()
