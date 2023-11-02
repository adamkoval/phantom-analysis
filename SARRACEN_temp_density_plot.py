import sarracen
import os
import re

import matplotlib.pyplot as plt
import numpy as np

import script_utils as su

# HOUSEKEEPING: Command line arguments or config options are processed here
cmd_args = [['--config_file', '-c', 'store', 'config_file', 'Use config file instead of cmd input?'],
		['--data_dir', '-d', 'store', 'data_dir', 'The directory with results'],
		['--output_dir', '-o', 'store', 'output_dir', 'Where to store analysis output'],
		['--store_data', '-sd', 'store_true', 'store_data', 'Whether to save the data into output'],
		['--store_plot', '-sp', 'store_true', 'store_plot', 'Whether to save the plot into output'],
		['--N_densest', '-N', 'store', 'N_densest', 'Number of densest particles to average ovrer']]
_description = "A script to plot temp against density from PHANTOM SPH simulations using the SARRACEN package."

config_file, data_dir, output_dir, store_data, store_plot = su.get_args(cmd_args)

if config_file:
	data_dir, output_dir, store_data, store_plot = su.get_config(config_file)

if store_data==True or store_plot==True and not output_dir:
	output_dir = input("No output path provided. Please provide an output path if you wish to save data OR plot (abs path to directory required):")


# DATA PROCESSING: The interesting stuff
def get_densest(sdf, N):
	"""
	sdf - dataframe with sim data
	N - number of densest
	"""
	return sdf.sort_values(by='rho', ascending=False).head(N)

print("reading in data")
fins_all = np.sort([file for file in os.listdir(data_dir) if re.match('colltest_[0-9].', file)]) # Sort files by asc. timestep
fins = fins_all

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

print("plotting")
fig, ax = plt.subplots()
ax.loglog(rhos_max, temps_max, label='maxima')
ax.loglog(rhos_avg, temps_avg, label='means')
ax.legend()
ax.set_xlabel('Density [a.u.]')
ax.set_ylabel('Temperature [a.u.]')
# [ADD SAVEFIG THING - check if I can add a timestamp from the data..]
plt.show()
