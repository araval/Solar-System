import logging
import numpy as np
from math import pi

import sys
import logging
log_format = '%(asctime)s|%(levelname)s| %(message)s'
logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.INFO)

ASTRONOMICAL_UNIT = 1.495978707*10**11
SECONDS_IN_A_YEAR = 365.25*86400

class Planet(object):	
    def __init__(self, aphelion, perihelion, orbital_velocity, diameter):
        """
        Parameters
        ----------
        aphelion: float (AU)
        perihelion: float (AU)
        orbital_velocity: float (km/s)
        diameter: float (in earth-diameters)
        """
        self.aphelion = aphelion
        self.perihelion = perihelion
        self.diameter = diameter

        # story orbital velocity in AU/earth_year
        self.orbital_velocity = orbital_velocity*1000/ASTRONOMICAL_UNIT*SECONDS_IN_A_YEAR
        self.set_ellipse_params()
        
    def set_ellipse_params(self):
        logging.info("Calculating ellipse parameters")
        self.a = (self.aphelion + self.perihelion)/2  # semi-major axis
        self.c = self.a - self.perihelion             # foci at +/- c
        self.b = np.sqrt(self.a**2 - self.c**2)       # semi-minor axis
        self.eccentricity = self.c/self.a

    def get_coordinates(self, time=1.0):
        """
        Generate coordinates for the planet for a period of <time> earth years.
        In its current state, this assumes that the inclination to ecliptic is 0 for all planets.
        This also assumes all major axis are aligned, and that in the initial position, all planets
        are collinear. This will be modified soon.

        Parameters
        ----------
        time (in earth years): float
        """

        mean_radius = (self.a + self.b)/2  # AUs
        angular_velocity = self.orbital_velocity/mean_radius # radians / earth-year
        angular_distance = angular_velocity * time        
        
        logging.info("Angular distance traversed in {} Earth Years = {:.3f} radians".format(time, angular_distance)) 

        # Use the parametric equation of ellipse to generate x, y
        n = 50*time  # using 50 points per earth-year. Increasing this number results in very slow animation.
        t = np.linspace(0, angular_distance, n)
        x = self.a*np.sin(t)
        y = self.b*np.cos(t)
        return x, y
