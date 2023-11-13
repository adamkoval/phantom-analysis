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
# Progress update
print("reading in data")

# Get simulation info from run log
date, time = su.grep_tstamp(run_log_path)
save_path = output_dir + ''.join(date.split('/')[::-1]) + '_' + time.replace(':', '')

# Sort files
fins_all = np.sort([file for file in os.listdir(data_dir) if re.match('colltest_[0-9].', file)]) # Sort files by asc. timestep
fins = fins_all#[:2] # Used for debugging

# Check if analysis has been done
if any(save_path.split('/')[-1] in file for file in os.listdir(output_dir)):
	rhos_avg, temps_avg = du.read_existing_analysis(save_path + ".dat")
else:
	# Parsing the data with SARRACEN
	rhos_max, temps_max, rhos_avg, temps_avg = du.parse_with_SARRACEN(data_dir, fins, save_path, N_densest, store_data)

# Reading in comparison files
fin_lomb_merc, fin_stam_merc, fin_stam_max = [i.strip() for i in comp_file_paths.split(',')]
dat_lomb_merc = pd.read_csv(fin_lomb_merc, names=['density [g/cm3]', 'temperature [K]'])
dat_stam_merc = pd.read_csv(fin_stam_merc, names=['density [g/cm3]', 'temperature [K]'])
dat_stam_max = pd.read_csv(fin_stam_max, comment='#', delim_whitespace=True, header=None)[[6, 7]]
dat_stam_max.columns = ['density [g/cm3]', 'temperature [K]']


# PLOTTING
print("plotting")
fig, ax = plt.subplots()
try:
	ax.loglog(rhos_max, temps_max, label='maxima')
except:
	pass
ax.loglog(rhos_avg, temps_avg, label='Stamatellos ($N_{avg}=200$)', color='r')
ax.loglog(dat_lomb_merc['density [g/cm3]'], dat_lomb_merc['temperature [K]'], label='Lombardi-Mercer+2018', ls='--', color='g')
ax.loglog(dat_stam_merc['density [g/cm3]'], dat_stam_merc['temperature [K]'], label='Stamatellos-Mercer+2018', ls='--', color='k')
#ax.loglog(dat_stam_max['density [g/cm3]'], dat_stam_max['temperature [K]'], label='Stamatellos maxvals', ls='--')

ax.legend()
ax.set_xlabel('Density (g cm$^{-3}$)')
ax.set_ylabel('Temperature (K)')
title = "Finished on {}, {}".format(time, date)
ax.set_title(title)
ax.grid()
if store_plot:
	plt.savefig(save_path + "_fig.png", format='png')
plt.show()