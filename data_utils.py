#
# Utils for data management
#
import pandas as pd

from astropy.constants import au, M_sun

def convert_rho_units(rhos):
    """
    Converts density from machine units to g/cm3
    In:
        > rhos (arr) - array-like of rhos in machine units
    Out:
        > rho_conv (arr) - array-like of rhos in g/cm3 units
    """
    solarm_g = M_sun.value * 10**3 # Convert from kg to g
    au_cm = au.value * 10**2 # Convert from m to cm
    return rhos * solarm_g / au_cm**3