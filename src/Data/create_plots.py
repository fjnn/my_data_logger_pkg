#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import plotting
import loading
import matplotlib.pyplot as plt

# %%
# Load Data
my_trials = loading.load_folder('Output')
# Clean Data
my_trials = loading.clean_many_dataframes_from_initial_values(my_trials)

# %% Plot learning curve
plt.figure()  # create new plot window
plotting.plot_learning_curve(my_trials)

# %% Plot pedal presses
plt.figure()  # create new plot window
plotting.plot_pedal_press_counts_per_trial(my_trials)
