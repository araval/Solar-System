import logging
import numpy as np
from math import pi
import pandas as pd

import sys
import logging
log_format = '%(asctime)s|%(levelname)s| %(message)s'
logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.INFO)

ASTRONOMICAL_UNIT = 1.495978707*10**11
SECONDS_IN_A_YEAR = 365.25*86400

radians = lambda theta_deg: theta_deg*pi/180

class Planet(object):	
    def __init__(self, aphelion, perihelion, Omega, w, i, orbital_period):
        """
        Parameters
        ----------
        aphelion: float (AU)
        perihelion: float (AU)
        orbital_velocity: float (km/s)
        """
        self.aphelion = aphelion
        self.perihelion = perihelion
        self.Omega = radians(Omega)
        self.w = radians(w)
        self.i = radians(i)

        self.period = orbital_period
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

        Parameters
        ----------
        time (in earth years): float
        """

        angular_distance = 2*pi*time/self.period        
        logging.info("Angular distance traversed in {} Earth Years = {:.3f} radians".format(time, angular_distance)) 

        # Use the parametric equation of ellipse to generate x, y
        n = 50*time  # using 50 points per earth-year. Increasing this number results in very slow animation.
        t = np.linspace(0, angular_distance, n)
        x = self.a*np.sin(t)
        y = self.b*np.cos(t)
        z = np.zeros(len(x))

        R = self.get_rotation_matrix(self.Omega, self.w, self.i)
        ecliptic_position = []
        for point in zip(x, y, z):
            ecliptic_position.append(R.dot(point))

        return pd.DataFrame(ecliptic_position, columns=['x', 'y', 'z'])

    def get_rotation_matrix(self, Omega, w, i):

        c = np.cos
        s = np.sin        

        R1 = np.array([[c(w), s(w), 0], [-1*s(w), c(w), 0], [0, 0, 1]])
        R2 = np.array([[1, 0, 0],       [0, c(i), s(i)], [0, -1*s(i), c(i)]])
        R3 = np.array([[c(Omega), s(Omega), 0], [-1*s(Omega), c(Omega), 0], [0, 0, 1]])

        R = R1.dot(R2.dot(R3))

        return R
