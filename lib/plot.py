#!/usr/bin/env
"""
Plotting the models and estimated parameter values to deterimine fit.

Code built upon work by: Dr Jonathan R. Pritchard, Researcher in Cosmology and Astrostatistics at Imperial College London
Contact: j.pritchard@imperial.ac.uk

@author: Jesse Cross, MSci Physics at Imperial College London
Contact: jesse.cross17@imperial.ac.uk
@author: Ivan Lim, MSci Physics at Imperial College London
Contact: yi.lim17@imperial.ac.uk
"""


####################################################
#################### LIBRARIES #####################
####################################################
import bilby
import corner
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import edges
import models
import os
import sys

####################################################
###################### PATH ########################
####################################################
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))           # Directory of plot.py (should be ~/21sampler/lib)
BASE_DIR = os.path.dirname(PROJECT_ROOT)                            # Parent directory of PROJECT_ROOT (should be ~/21sampler)
directory = '{}/samples'.format(BASE_DIR)                           # Directory where sample data is (should be ~/21sampler/samples)


####################################################
################### SELECT DATA ####################
####################################################
# The data must already exist to run this. If it doesn't, run sampler.py with the chosen set-up first.

# Sampler (pymultinest, dynesty, ultranest, nestle, cpnest, pypolychord) 
sampler = 'pymultinest'

# Model (linearised_model, systematic_model, ares_model)
case = 'linearised_model'

# Data ('edges', 'mock', 'ares')
data = 'edges'

# Livepoints
livepoints = 5000


####################################################
################## OUTPUT FORMAT ###################
####################################################
label = '{}_{}_{}_{}'.format(case, data, sampler, livepoints)
outdir = directory + '/{}_{}/'.format(case, data) + label
bilby.utils.check_directory_exists_and_if_not_mkdir(outdir)
print(outdir)

if os.path.exists(outdir) == False:
    print("This directory doesn't exist. Run sampler.py with the chosen set-up first to create the data.")
    sys.exit()

####################################################
############### IMPORT SAMPLE DATA #################
####################################################
# Read in sampelr data (as a dataframe object)
# result = "{}/{}_result.json".format(outdir, label)
result = bilby.result.read_in_result(outdir=outdir, label=label)
#print(result.posterior.loc[result.posterior['log_likelihood'] == np.amax(result.posterior['log_likelihood'].values)])
#print(result.parameter_labels)

max_post_param = []

for param in result.parameter_labels:
    print(f'{param} median is:', result.get_one_dimensional_median_and_error_bar(key=[f'{param}']).median)
    print(f'{param} minus error is:', result.get_one_dimensional_median_and_error_bar(key=[f'{param}']).minus)
    print(f'{param} plus error is:', result.get_one_dimensional_median_and_error_bar(key=[f'{param}']).plus)
    max_post_param.append(result.get_one_dimensional_median_and_error_bar(key=[f'{param}']).median)

print(max_post_param)

####################################################
################# MODEL SELECTION ##################
####################################################
if case == 'linearised_model':
    model = models.linearised_model

elif case == 'systematic_model':
    model = models.systematic_model

elif case == 'ares_model':
    model = ares_sim.model_test


####################################################
###################### DATA ######################## 
####################################################
# Edges data
if data == 'edges':
    nu, weight, Tsky, Tres1, Tres2, Tmodel, T21, err = edges.read_edges()

# Simulate data with a normal distribution of errors
elif data == 'mock':
    nu = np.linspace(50.0, 100.0)          
    N = len(nu)
    err = 0.01 * np.ones(N)           
    Tsky = model(nu, **theta) + np.random.normal(0.0, err, N)

# Simulate 21cm from ARES
elif data == 'ares':
    nu, T21 = ares_sim.simulation_test(**theta)
    N = len(nu)
    err = 0.01 * np.ones(N)
    Tsky = T21 + np.random.normal(0.0, err, N)

####################################################
####################### PLOT #######################
####################################################

# Plot 1: Corner
samples = result.samples
labels = result.parameter_labels
fig = corner.corner(samples, labels=labels)


# Plot 2: Residuals
Tsky_post = model(nu, *max_post_param)          # Model using maximum posterior parameter values
Tres = Tsky - Tsky_post                         # Residuals = [simulated or real sky data] - [maximum posterior model]
rms_Tres = round(np.sqrt(np.mean(Tres**2)), 3)  # RMS of our residuals
rms_Tres2 = round(np.sqrt(np.mean(Tres2**2)), 3)   # RMS of Bowman2018 residuals

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,5))
ax.tick_params(axis='both', which='major', labelsize=12) 
ax.axhline(y=0.01, linestyle=':', color='grey', linewidth=1, label='Error bars')
ax.axhline(y=-0.01, linestyle=':', color='grey', linewidth=1)
ax.plot(nu, Tres, linestyle='-', color='black', linewidth=1, label=f'Our residuals (RMS = {rms_Tres} K)')
ax.plot(nu, Tres2, linestyle='--', color='dimgrey', linewidth=1, label=f'Bowman et al. 2018 residuals (RMS = {rms_Tres2} K)')
ax.set_xlabel(r'Frequency, $\nu$ [MHz]', fontsize=12)
ax.set_ylabel(r'Temperature, $T$ [K]', fontsize=12)
# ax.text(0.5, 0.05, f'RMS = {rms_Tres} K', fontsize=12, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
ax.legend(loc='lower right', fontsize=12)

fig.savefig('{}/{}_residuals.png'.format(outdir, label), dpi=300, bbox_inches='tight')
