import pandas as pd
import numpy as np
from planets import Planet

import plotly.express as px

import sys
import logging
log_format = '%(asctime)s|%(levelname)s| %(message)s'
logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.INFO)

def create_dataframe():
    df = pd.read_csv('planet_data.csv')
    
    dataframes = []
    for _, row in df.iterrows():
        logging.info("Creating dataframe for Planet {}".format(row['name']))
        planet = Planet(aphelion=row['aphelion_AU'], 
                        perihelion=row['perihelion_AU'], 
                        diameter=row['diameter_earths'], 
                        orbital_velocity=row['orbital_velocity_kmps'])
    
        logging.info("Calculating coordinates")
        x, y = planet.get_coordinates(time=10)
        time = np.array([i for i in range(len(x))])
        values_to_insert = [i for i in zip(time, x, y)]

        df1 = pd.DataFrame(values_to_insert)
        df1['name'] = row['name']
        df1['diameter_earths'] = row.diameter_earths

        dataframes.append(df1)

    df1 = pd.concat(dataframes)
    df1.columns = ['time', 'x', 'y', 'Planet', 'diameter_earths']

    return df1

if __name__ == '__main__':
    df = create_dataframe()
    fig = px.scatter(df, x="x", y="y", animation_frame="time", animation_group="Planet",
           size="diameter_earths", color="Planet", hover_name="Planet",
           size_max=55, template='plotly_dark', range_x=[-12, 12], range_y=[-12, 12], width=1000, height=1000)
    fig.show()
