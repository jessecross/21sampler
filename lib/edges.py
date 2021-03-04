#!/usr/bin/env
"""
Two things here:
1) Contains a function to read the EDGES data which can be used in other files (e.g. sampler.py)
2) Run to reproduce the results plotted in Bowman (2018) and EDGES Data Releases – LoCo Lab

Code built upon work by: Dr Jonathan R. Pritchard, Researcher in Cosmology and Astrostatistics at Imperial College London
Contact: j.pritchard@imperial.ac.uk

@author: Jesse Cross, MSci Physics at Imperial College London
Contact: jesse.cross17@imperial.ac.uk
@author: Ivan Lim, MSci Physics at Imperial College London
Contact: yi.lim17@imperial.ac.uk
"""


####################################################
################### LIBRARIES ######################
####################################################
import os
import bilby
import numpy as np
import matplotlib.pyplot as plt
import astropy.io.ascii as ascii


####################################################
###################### PATH ########################
####################################################
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))   # Directory of edges.py (should be lib)
BASE_DIR = os.path.dirname(PROJECT_ROOT)                    # Parent directory of PROJECT_ROOT (should be 21sampler)


####################################################
################## FUNCTIONS #######################
####################################################
# Errors for EDGES data
def thermalNoise(Tsky, epsilon = 1.0e-4, constant = True):
    """
    Thermal noise.
    This is a modelled temporary substitute for the EGDES data errors, since we don't have hold of them yet.
    """
    # Thermal noise in K

    #use negative epsilon to indicate constant noise
    if constant == True:
        #constant noise
        noise = 0.01 * np.ones(len(Tsky))
    elif constant == False:
        #proper thermal noise
        noise = epsilon * Tsky

    return noise

# Read EDGES data
def read_edges():
    """
    Read in EDGES data and return nu, signal, errors

    See "EDGES Data Releases – LoCo Lab" for information on EDGES data.

    figure1_plotdata.csv
    129 rows (1 header row), 7 columns
    8 kB
    ----------------------------------
    column 1: Frequency [MHz]
    column 2: Weight - 0 or 1 specifying the validity of the data at that frequency
    column 3: Tsky [K] - integrated sky spectrum used for the model fitting, plotted in panel (a)
    column 4: Tres1 [K] - residuals to the best-fit foreground-only (5-term physical model), plotted in panel (b)
    column 5: Tres2 [K] - residuals to the best-fit combined foreground and 21cm model, plotted in panel (c)
    column 6: Tmodel [K] - best-fit 21cm model, plotted in panel (d)
    column 7: T21 [K] - Combined Tmodel + Tres2, plotted in panel (e)
    """

    # Select EDGES data file directory
    fig1file = "{}/edges2018/figure1_plotdata.csv".format(BASE_DIR)

    # Read in EDGES data (as a Table object)
    data = ascii.read(fig1file)
    
    # Data set has zeros as beginning and end, so skip those
    dstart = 3
    dend = -2

    # Assign data from Table
    nu = np.array(data['Frequency [MHz]'][dstart:dend])
    weight = np.array(data['Weight'][dstart:dend])
    Tsky = np.array(data['a: Tsky [K]'][dstart:dend])
    Tres1 = np.array(data['b: Tres1 [K]'][dstart:dend])
    Tres2 = np.array(data['c: Tres2 [K]'][dstart:dend])
    Tmodel = np.array(data[ 'd: Tmodel [K]'][dstart:dend])
    T21 = np.array(data['e: T21 [K]'][dstart:dend])
    
    # EDGES error data (NOTE: Need to find out where we can obtain this!)
    # For now, cheat and use something sensible (the function is defined above)
    err = thermalNoise(Tsky, epsilon=2.0e-5, constant=True)
    
    return nu, weight, Tsky, Tres1, Tres2, Tmodel, T21, err


####################################################
############## PLOT EDGES RESULTS ##################
####################################################
# Directory and file name
outdir = '{}/edges2018/reproduced'.format(BASE_DIR)
label = 'edges2018_plot'
bilby.utils.check_directory_exists_and_if_not_mkdir(outdir)

# Read EDGES data and results
nu, weight, Tsky, Tres1, Tres2, Tmodel, T21, err = read_edges()

# RMS of EDGES residuals
rms_Tres1 = round(np.sqrt(np.mean(Tres1**2)), 3)
rms_Tres2 = round(np.sqrt(np.mean(Tres2**2)), 3)

# Plot EDGES results to check it looks sensible and matches plots from "EDGES Data Releases – LoCo Lab"
fig, ax = plt.subplots(nrows=3, ncols=2)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=0.5)

# Subplot (a) - Tsky is the integrated sky spectrum used for the model fitting
ax[0,0].plot(nu, Tsky, '-k', linewidth=1)      
ax[0,0].set_title('a', loc='left', fontweight='bold', fontsize=10)
ax[0,0].set_xticks([50,60,70,80,90,100])
ax[0,0].set_xticklabels([50,60,70,80,90,100], fontsize=6)
ax[0,0].set_yticks([1000, 3000, 5000])
ax[0,0].set_yticklabels([1000, 3000, 5000], fontsize=6)
# ax[0,0].set_xlabel(r'Frequency, $\nu$ [MHz]', fontsize=8)
ax[0,0].set_ylabel(r'Temperature, $T$ [K]', fontsize=7)

# Subplot (b) - Tres1 is the residuals to the best-fit foreground-only (5-term physical model)
ax[1,0].plot(nu, Tres1, '-k', linewidth=1)      
ax[1,0].set_title('b', loc='left', fontweight='bold', fontsize=10)
ax[1,0].set_xticks([50,60,70,80,90,100])
ax[1,0].set_xticklabels([50,60,70,80,90,100], fontsize=6)
ax[1,0].set_yticks([-0.2, 0, 0.2])
ax[1,0].set_yticklabels([-0.2, 0, 0.2], fontsize=6)
# ax[1,0].set_xlabel(r'Frequency, $\nu$ [MHz]', fontsize=8)
ax[1,0].set_ylabel(r'Temperature, $T$ [K]', fontsize=7)
ax[1,0].text(0.2, 0.1, f'r.m.s. = {rms_Tres1} K', fontsize=6, horizontalalignment='center', verticalalignment='center', transform=ax[1,0].transAxes)

# Subplot (c) - Tres2 is the residuals to the best-fit combined foreground and 21cm model
ax[1,1].plot(nu, Tres2, '-k', linewidth=1)      
ax[1,1].set_title('c', loc='left', fontweight='bold', fontsize=10)
ax[1,1].set_xticks([50,60,70,80,90,100])
ax[1,1].set_xticklabels([50,60,70,80,90,100], fontsize=6)
ax[1,1].set_yticks([-0.2, 0, 0.2])
ax[1,1].set_yticklabels([])
# ax[1,1].set_xlabel(r'Frequency, $\nu$ [MHz]', fontsize=8)
# ax[1,1].set_ylabel(r'Temperature, $T$ [K]', fontsize=8)
ax[1,1].text(0.2, 0.1, f'r.m.s. = {rms_Tres2} K', fontsize=6, horizontalalignment='center', verticalalignment='center', transform=ax[1,1].transAxes)

# Subplot (d) - Tmodel is the best-fit 21cm model
ax[2,0].plot(nu, Tmodel, '-k', linewidth=1)     
ax[2,0].set_title('d', loc='left', fontweight='bold', fontsize=10)
ax[2,0].set_xticks([50,60,70,80,90,100])
ax[2,0].set_xticklabels([50,60,70,80,90,100], fontsize=6)
ax[2,0].set_yticks([-0.6, -0.4, -0.2, 0, 0.2])
ax[2,0].set_yticklabels([-0.6, -0.4, -0.2, 0, 0.2], fontsize=6)
ax[2,0].set_xlabel(r'Frequency, $\nu$ [MHz]', fontsize=7)
ax[2,0].set_ylabel(r'Temperature, $T$ [K]', fontsize=7)

# Subplot (e) - T21 is the combined Tmodel + Tres2
ax[2,1].plot(nu, T21, '-k', linewidth=1)        
# ax[2,1].set_title('e', loc='left', fontweight='bold', fontsize=10)
ax[2,1].set_xticks([50,60,70,80,90,100])
ax[2,1].set_xticklabels([50,60,70,80,90,100], fontsize=6)
ax[2,1].set_yticks([-0.6, -0.4, -0.2, 0, 0.2])
ax[2,1].set_yticklabels([-0.6, -0.4, -0.2, 0, 0.2], fontsize=6)
ax[2,1].set_xlabel(r'Frequency, $\nu$ [MHz]', fontsize=7)
ax[2,1].set_ylabel(r'Temperature, $T$ [K]', fontsize=7)

# Delete empty subplot (for the aesthetic)
fig.delaxes(ax[0,1])    

# Save the plot
fig.savefig('{}/{}.png'.format(outdir, label), dpi=300, bbox_inches='tight')