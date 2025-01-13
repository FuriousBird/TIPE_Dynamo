import numpy as np
from math import atan, pi, sqrt
#get the magnetic field of a paralelepiped magnet with it's axis facing vertically (H) (Nord au dessus, Sud en dessous)
#we'll assume a physically representative decrease of the magnetic field with the distance
#r being the distance from the center of the magnet
#we can deduce a coefficient of decrease k = B0/(2*sqrt(4*z**2 + L**2 + W**2))
Br = 1.4 #Tesla
B0 = Br/pi

def B1(W,L,D,z):
    a1 = np.arctan((L*W)/(2*z*np.sqrt(4*z**2 + L**2 + W**2)))
    a2 = -np.arctan((L*W)/(2*(D+z)*np.sqrt(4*(D+z)**2 + L**2 + W**2)))
    B = B0*(a1 + a2)
    return B

def B2(W,L,D,z, r):
    B = B1(W,L,D,z)*((D+z)/r)**3
    return B