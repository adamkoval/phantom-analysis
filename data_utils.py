#
# Utils for data management
#
import numpy as np
import pandas as pd
import sarracen

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


def get_densest(sdf, N):
	"""
	sdf - dataframe with sim data
	N - number of densest
	"""
	return sdf.sort_values(by='rho', ascending=False).head(N)


def parse_with_SARRACEN(data_dir, fins, save_path, N_densest, store_data):
    temps_max = []
    rhos_max = []
    temps_avg = []
    rhos_avg = []
    for fin in fins:
        print("Working on file {}".format(fin))
        fin = data_dir + fin
        sdf = sarracen.read_phantom(fin) # Read in using Sarracen
        sdf.calc_density() # Calculate density using Sarracen

        # Append to lists
        temps_max.append(np.max(sdf['temperature']))
        rhos_max.append(np.max(sdf['rho']))

        densest = get_densest(sdf, N_densest)
        temps_avg.append(np.mean(densest['temperature']))
        rhos_avg.append(np.mean(densest['rho']))
    temps_max = np.array(temps_max)
    rhos_max = np.array(rhos_max)
    temps_avg = np.array(temps_avg)
    rhos_avg = np.array(rhos_avg)

    # Convert rhos
    rhos_avg = convert_rho_units(rhos_avg)
    rhos_max = convert_rho_units(rhos_max)

    # Writing to file
    if store_data:
        pd.DataFrame(data={'density [g/cm3]': rhos_avg, 'temperature [K]': temps_avg}).to_csv(save_path + ".dat", index=False)
    
    return rhos_max, temps_max, rhos_avg, temps_avg


def read_existing_analysis(saved_data):
    """
    Reads in existing analysis files.
    """
    df = pd.read_csv(saved_data)
    rhos_avg = df['density [g/cm3]']
    temps_avg = df['temperature [K]']
    return rhos_avg, temps_avg