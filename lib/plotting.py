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
# Import Libraries
####################################################
import bilby
import numpy as np
import matplotlib.pyplot as plt
import edges
import models

####################################################
# Fit model to EDGES data
####################################################
# Set directory and filename
# outdir = '/home/jcross/MSciProject/edges_bilby/Imperial/model_plots'
# label = 'model_plots'
bilby.utils.check_directory_exists_and_if_not_mkdir(outdir)

# Read EDGES data
nu, weight, Tsky, Tres1_EDGES, Tres2_EDGES, T_EDGES_model, T21, err = edges.read_edges()

# Linearised model parameters NOTE: Starting with just this model to test. Will expand to do other models.
param = {'A': 0.55,
        'nu0': 78.32, 
        'w': 18.74, 
        'tau': 6.79, 
        'a0': -10116.14, 
        'a1': -5676.02, 
        'a2': -1832.31, 
        'a3': 150.72, 
        'a4': 11716.19}

# Lienarised model temperature values
T_lin_model = models.linearised_model(nu, param['A'], param['nu0'], param['w'], param['tau'], param['a0'], param['a1'], param['a2'], param['a3'], param['a4'])

# Foreground + 21 cm Residuals for linearised model
Tres_lin = Tsky - T_lin_model
print(T_lin_model)
print(Tsky)
print(Tres_lin)
# RMS of residuals
rms_Tres_lin = round(np.sqrt(np.mean(Tres_lin**2)), 3)
rms_Tres2 = round(np.sqrt(np.mean(Tres2_EDGES**2)), 3)

# Plot model fitting to EDGES data
fig, ax = plt.subplots(nrows=2, ncols=2)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.9)

# Subplot (a) - Tsky is the integrated sky spectrum used for the model fitting
ax[0,0].plot(nu, Tsky, '-k')      
ax[0,0].set_title('Integrated sky spectrum', loc='left', fontweight='bold', fontsize=8)
ax[0,0].set_xticks([50,60,70,80,90,100])
ax[0,0].set_xticklabels([50,60,70,80,90,100], fontsize=8)
ax[0,0].set_yticks([1000, 3000, 5000])
ax[0,0].set_yticklabels([1000, 3000, 5000], fontsize=8)
ax[0,0].set_xlabel(r'Frequency, $\nu$ [MHz]', fontsize=8)
ax[0,0].set_ylabel(r'Temperature, $T$ [K]', fontsize=8)

# Subplot (b) - Tres2_EDGES is the residuals to the EDGES best-fit combined foreground and 21cm model
ax[1,0].plot(nu, Tres2_EDGES, '-k')      
ax[1,0].set_title('EDGES Foreground + 21cm residuals', loc='left', fontweight='bold', fontsize=8)
ax[1,0].set_xticks([50,60,70,80,90,100])
ax[1,0].set_xticklabels([50,60,70,80,90,100], fontsize=8)
ax[1,0].set_yticks([-0.3, 0, 0.3])
ax[1,0].set_yticklabels([-0.3, 0, 0.3], fontsize=8)
ax[1,0].set_xlabel(r'Frequency, $\nu$ [MHz]', fontsize=8)
ax[1,0].set_ylabel(r'Temperature, $T$ [K]', fontsize=8)
ax[1,0].text(0.8, 0.9, f'r.m.s. = {rms_Tres2} K', fontsize=6, horizontalalignment='center', verticalalignment='center', transform=ax[1,0].transAxes)

# Subplot (c) - Tres_lin is the residuals to our linearised model best-fit combined foreground and 21cm model
ax[1,1].plot(nu, Tres_lin, '-k')        
ax[1,1].set_title('Linearised Foreground + 21cm residuals', loc='left', fontweight='bold', fontsize=8)
ax[1,1].set_xticks([50,60,70,80,90,100])
ax[1,1].set_xticklabels([50,60,70,80,90,100], fontsize=8)
ax[1,1].set_yticks([-0.3, 0, 0.3])
ax[1,1].set_yticklabels([-0.3, 0, 0.3], fontsize=8)
ax[1,1].set_xlabel(r'Frequency, $\nu$ [MHz]', fontsize=8)
ax[1,1].set_ylabel(r'Temperature, $T$ [K]', fontsize=8)
ax[1,1].text(0.8, 0.9, f'r.m.s. = {rms_Tres_lin} K', fontsize=6, horizontalalignment='center', verticalalignment='center', transform=ax[1,1].transAxes)

# Delete empty subplot (for the aesthetic)
fig.delaxes(ax[0,1])    

# Save the plot
fig.savefig('{}/{}_data.png'.format(outdir, label), dpi=300)
