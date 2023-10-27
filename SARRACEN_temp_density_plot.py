import sarracen
import os
import re

import matplotlib.pyplot as plt
import numpy as np

def get_densest(sdf, N):
	"""
	sdf - dataframe with sim data
	N - number of densest
	"""
	return sdf.sort_values(by='rho', ascending=False).head(N)

print("reading in data")
data_dir = "/home/dc-kova1/scratch/programs/phantom_runs/tests/collapse_test_Lombardi/"
fins_all = np.sort([file for file in os.listdir(data_dir) if re.match('colltest_[0-9].', file)])
fins = fins_all
#fins = ["colltest_00300"]

N = 200
temps_max = []
rhos_max = []
temps_avg = []
rhos_avg = []
for fin in fins:
	print("Working on file {}".format(fin))
	fin = data_dir + fin
	sdf = sarracen.read_phantom(fin)
	sdf.calc_density()

	# Append to lists
	temps_max.append(np.max(sdf['temperature']))
	rhos_max.append(np.max(sdf['rho']))

	densest = get_densest(sdf, N)
	temps_avg.append(np.mean(densest['temperature']))
	rhos_avg.append(np.mean(densest['rho']))

print("plotting")
fig, ax = plt.subplots()
ax.loglog(rhos_max, temps_max, label='maxima')
ax.loglog(rhos_avg, temps_avg, label='means')
ax.legend()
ax.set_xlabel('Density [a.u.]')
ax.set_ylabel('Temperature [a.u.]')
plt.show()
