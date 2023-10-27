import sarracen
import os
import re

import matplotlib.pyplot as plt
import numpy as np

def extract_info(fin):
	

# A friendly message
data_dir = "/home/dc-kova1/scratch/programs/phantom_runs/tests/collapse_test_Lombardi/"
print("reading in data from {}".format(data_dir))

#fins = [file for file in os.listdir(data_dir) if re.match('colltest_[0-9].', file)]
#fins = fins[0]
fins = ["colltest_00300"]

temps = []
rhos = []
for fin in fins:
	fin = data_dir + fin
	sdf = sarracen.read_phantom(fin)
	sdf.calc_density()
	temps.append(sdf['temperature'])
	rhos.append(sdf['rho'])

print("doing some calcs")
t_max = [np.max(run) for run in temps]
rho_max = [np.max(run) for run in rhos]

t_avg = [np.mean(run) for run in temps]
rho_avg = [np.mean(run) for run in rhos]

#print("plotting")
#fig, ax = plt.subplots()
#ax.plot(rho_max, t_max, label='maxima')
#ax.plot(rho_mean, t_mean, label='means')
#ax.legend()
#ax.set_xlabel('Density [a.u.]')
#ax.set_ylabel('Temperature [a.u.]')
#plt.show()
