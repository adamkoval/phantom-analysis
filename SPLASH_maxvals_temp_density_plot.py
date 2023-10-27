import matplotlib.pyplot as plt
import pandas as pd

fin = "/home/dc-kova1/scratch/programs/phantom_runs/tests/collapse_test_Lombardi/maxvals.out"

pre_data = pd.read_csv(fin)
headers = pre_data.iloc[4]
data = pd.DataFrame(pre_data.values[5:], columns=headers)
