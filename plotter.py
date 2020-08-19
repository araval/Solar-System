import pandas as pd
import numpy as np
from planets import Planet

import plotly.express as px

import matplotlib.pyplot as plt
import matplotlib.animation as animation
# from IPython.display import HTML    # for use in a jupyter notebook

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
    df1 = pd.read_csv('data/planet_orbital_elements.csv')
    df2 = pd.read_csv('data/planet_elements.csv')

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

def plot_with_matplotlib(coordinate_df):

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8))

    a=5.4
    ax = plt.axis([-a, a, -a, a])

    planet_point, = plt.plot([], [], 'wo', markersize=7)

    planets = coordinate_df.Planet.unique()
    colors = ['#40ff00', '#ff33ff', '#1affff', '#ffad33', '#ffff4d'] # only five for inner planets

    x_list = []
    y_list = []
    for color, name in zip(colors, planets):
        df_planet = coordinate_df[coordinate_df.Planet == name]
        x = df_planet['x'].values
        y = df_planet['y'].values
        x_list.append(x)
        y_list.append(y)
        plt.plot(x, y, color, alpha=0.3, label=name)
    
    plt.axis('off')
    plt.legend(loc='upper right')
    plt.title("Inner planets, 12 years")

    def animate(i):
        planet_point.set_data([x[i] for x in x_list], [y[i] for y in y_list])
        return planet_point,

    num_frames = df_planet.shape[0]
    anim = animation.FuncAnimation(fig, animate, frames=np.arange(0, num_frames, 1), \
                                      interval=100, blit=True, repeat=True)

    anim.save('inner_planets.gif', writer='imagemagick', fps=15)
    plt.show()
    
    #if using this function in a notebook, uncomment lines below, and remove plt.show() above
    #plt.close(anim._fig)
    #HTML(anim.to_html5_video())

if __name__ == '__main__':
    all_planet_coordinates = create_dataframe(time=12)
    #plot_with_plotly(all_planet_coordinates)
    plot_with_matplotlib(all_planet_coordinates)
