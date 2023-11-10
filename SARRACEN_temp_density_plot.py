import sarracen
import os
import re
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import script_utils as su
import data_utils as du

# HOUSEKEEPING: Command line arguments or config options are processed here
cmd_args = [['--config_file', '-c', 'store', 'config_file', 'Use config file instead of cmd input?'],
		['--data_dir', '-d', 'store', 'data_dir', 'The directory with results'],
		['--output_dir', '-o', 'store', 'output_dir', 'Where to store analysis output'],
		['--store_data', '-sd', 'store_true', 'store_data', 'Whether to save the data into output'],
		['--store_plot', '-sp', 'store_true', 'store_plot', 'Whether to save the plot into output'],
		['--N_densest', '-N', 'store', 'N_densest', 'Number of densest particles to average ovrer'],
		['--run_log', '-rl', 'store', 'run_log_path', 'Path to the run log of this simulation'],
		['--comp_files', '-cf', 'store', 'comp_file_paths', 'Paths of comparison files']]
description = "A script to plot temp against density from PHANTOM SPH simulations using the SARRACEN package."

config_file, data_dir, output_dir, store_data, store_plot, N_densest, run_log_path, comp_file_paths = su.get_args(cmd_args, _description=description) # Get command line args

# If config file present, use that
if config_file:
	data_dir, output_dir, store_data, store_plot, N_densest, run_log_path, comp_file_paths = su.get_config(config_file)

# Check for output dir
while (store_data==True or store_plot==True) and not output_dir: # If store option selected, ensure an output path is present
	output_dir = input("No output path provided. Please provide an output path if you wish to save data OR plot (abs path to directory required):")
if not os.path.exists(output_dir):
	ask_make_path = input("Output path does not exist, create?")
	if ask_make_path in ['yes', 'y', 'YES', 'Yes', 'Y']:
		os.mkdir(output_dir)
	else:
		print("Cannot proceed without output path. Exiting.")
		sys.exit()


# DATA PROCESSING: The interesting stuff
def get_densest(sdf, N):
	"""
	sdf - dataframe with sim data
	N - number of densest
	"""
	return sdf.sort_values(by='rho', ascending=False).head(N)

# Sort files
print("reading in data")
date, time = su.grep_tstamp(run_log_path)
fins_all = np.sort([file for file in os.listdir(data_dir) if re.match('colltest_[0-9].', file)]) # Sort files by asc. timestep
fins = fins_all[:2]

# Parsing the data with SARRACEN
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
rhos_avg_conv = du.convert_rho_units(rhos_avg)

# Writing to file
save_path = output_dir + time + "_" + date.replace('/', '.')
if store_data:
	pd.DataFrame(data={'density [g/cm3]': rhos_avg_conv, 'temperature [K]': temps_avg}).to_csv(save_path + ".dat", index=False)

# Reading in comparison files
fin_lomb_merc, fin_stam_merc, fin_stam_max = [i.strip() for i in comp_file_paths.split(',')]
dat_lomb_merc = pd.read_csv(fin_lomb_merc, names=['density [g/cm3]', 'temperature [K]'])
dat_stam_merc = pd.read_csv(fin_lomb_merc, names=['density [g/cm3]', 'temperature [K]'])
dat_stam_max = pd.read_csv(fin_stam_max, comment='#', delim_whitespace=True, header=None)[[6, 7]]
dat_stam_max.columns = ['density [g/cm3]', 'temperature [K]']


# PLOTTING
print("plotting")
fig, ax = plt.subplots()
ax.loglog(du.convert_rho_units(rhos_max), temps_max, label='maxima')
ax.loglog(rhos_avg_conv, temps_avg, label='means')
ax.loglog(dat_lomb_merc['density [g/cm3]'], dat_lomb_merc['temperature [K]'], label='Lombardi-Mercer')
ax.loglog(dat_stam_merc['density [g/cm3]'], dat_stam_merc['temperature [K]'], label='Stamatellos-Mercer')
ax.loglog(dat_stam_max['density [g/cm3]'], dat_stam_max['temperature [K]'], label='Stamatellos maxvals')

ax.legend()
ax.set_xlabel('Density [g/cm3]')
ax.set_ylabel('Temperature [K]')
title = "Finished on {}, {}".format(time, date)
ax.set_title(title)
if store_plot:
	plt.savefig(save_path + "_fig", format='png')
plt.show()