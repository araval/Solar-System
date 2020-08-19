import logging
import numpy as np
from math import pi
import pandas as pd

import sys
import logging
log_format = '%(asctime)s|%(levelname)s| %(message)s'
logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.INFO)

ASTRONOMICAL_UNIT = 1.495978707*10**11

radians = lambda theta_deg: theta_deg*pi/180

class Planet(object):
    def __init__(self, aphelion, perihelion, Omega, w, i, orbital_period, time):
        """
        Parameters
        ----------
        aphelion/perihelion: float
            longest/shortest distance from the sun in Astronomical Units (AU)
        Omega: float
            longitude of the ascending node in degrees
        w: float
            argument of periapsis in degrees
        i: float
            inclination to ecliptic in degrees
        orbital_period: float
            time to traverse 2pi radians, in earth-years

        time: float
            number of years to generate coordinates for
        """
        self.aphelion = aphelion
        self.perihelion = perihelion
        self.Omega = radians(Omega)
        self.w = radians(w)
        self.i = radians(i)

        self.period = orbital_period
        self.time = time
        self.set_ellipse_params()

    def set_ellipse_params(self):
        logging.info("Calculating ellipse parameters")
        self.a = (self.aphelion + self.perihelion)/2  # semi-major axis
        self.c = self.a - self.perihelion             # foci at +/- c
        self.b = np.sqrt(self.a**2 - self.c**2)       # semi-minor axis
        self.eccentricity = self.c/self.a

    def get_coordinates(self):
        """
        Generate coordinates for the planet for a period of <time> earth years.

        """
        num_revolutions = self.time/self.period
        angular_distance = 2*pi*num_revolutions
        msg = "Angular distance traversed in {} Earth Years = {:.3f} radians"\
                                            .format(self.time, angular_distance)
        logging.info(msg)

        n = int(50*num_revolutions) + 1  # we will generate 50 points per revolution 

        # Use the parametric equation of ellipse to generate x, y
        # This is planet's orbit's frame of reference, hence z = 0
        theta = np.linspace(0, angular_distance, n)
        x = self.a*np.sin(theta)
        y = self.b*np.cos(theta)
        z = np.zeros(len(x))

        R = self.get_rotation_matrix(self.Omega, self.w, self.i)
        ecliptic_position = []
        for point in zip(x, y, z):
            ecliptic_position.append(R.dot(point))

        ecliptic_coordinates = pd.DataFrame(ecliptic_position, columns=['x', 'y', 'z'])
        return ecliptic_coordinates

    def get_rotation_matrix(self, Omega, w, i):
        """
        Returns transformation matrix for coordinate transform from the planet's xy plane to the ecliptic

        Arguments are the standard orbital elements in radians:
        Omega: longitude of the ascending node
        w: argument of periapsis
        i: inclination to ecliptic
        """
        c = np.cos
        s = np.sin

        R1 = np.array([[c(w), s(w), 0], [-1*s(w), c(w), 0], [0, 0, 1]])
        R2 = np.array([[1, 0, 0],       [0, c(i), s(i)], [0, -1*s(i), c(i)]])
        R3 = np.array([[c(Omega), s(Omega), 0], [-1*s(Omega), c(Omega), 0], [0, 0, 1]])

        R = R1.dot(R2.dot(R3))

        return R
