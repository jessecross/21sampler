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
import numpy as np
import matplotlib.pyplot as plt
import astropy.io.ascii as ascii
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
# The data mus already exist to run this. If it doesn't, run sampler.py with the chosen set-up first.

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

if path.exists(outdir) == False:
    print("This directory doesn't exist. Run sampler.py with the chosen set-up first to create the data.")
    sys.exit()

####################################################
############### IMPORT SAMPLE DATA #################
####################################################

if sampler.sampler == 'pymultinest':
    # Select posterior data file
    post_data = "{}/pm_/{}/sats.dat".format(outdir, label)

    # Read in data (as a Table object)
    data = ascii.read(post_data)

else:
    pass

print(data)