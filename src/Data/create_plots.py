#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plotting
import loading
import matplotlib.pyplot as plt
import os
import pandas as pd

# %%
# Load Data
# my_trials = loading.load_folder('../../Output')

def load_file(filename):
    """ Load the CSV file specified
    @param filename: The name of the file or the relative path to the file you wish to load
    @returns A pandas DataFrame containing the data loaded from the specified file
    """
    return pd.read_csv(filename)

folder = '../../Output'
dataframes = []

files = sorted(os.listdir(folder))
for file in files:
    csv_filename = os.path.join(folder, file)
    csv_file = load_file(csv_filename)
    dataframes.append(csv_file)

print len(dataframes[1])

# %% Plot individual motions
plotting.plot_individual_motions(dataframes[0])

# # %% Plot learning curve
# plt.figure()  # create new plot window
# plotting.plot_learning_curve(my_trials)
#
# # %% Plot pedal presses
# plt.figure()  # create new plot window
# plotting.plot_pedal_press_counts_per_trial(my_trials)
