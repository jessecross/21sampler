#!/usr/bin/env
"""
Sampler for the 21 cm signal models.

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
import os
import bilby
import numpy as np
import matplotlib.pyplot as plt
from time import process_time
import models                      # signal models
import edges                       # edges data
import ares_sim                    # ares simulations

# Start the stopwatch / counter  
start = process_time()

####################################################
###################### PATH ########################
####################################################
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))   # Directory of sampler.py (should be ~/21sampler/lib)
BASE_DIR = os.path.dirname(PROJECT_ROOT)                    # Parent directory of PROJECT_ROOT (should be ~/21sampler)
directory = '{}/samples'.format(BASE_DIR)                   # Directory where samples are saved (should be ~/21sampler/samples)


####################################################
#################### CONTROLS ######################
####################################################
# Sampler (pymultinest, dynesty, ultranest, nestle, cpnest, pypolychord) 
sampler = 'pymultinest'

# Model (linearised_model, systematic_model, ares_model)
case = 'linearised_model'

# Data ('edges', 'mock', 'ares')
data = 'edges'

# Livepoints
livepoints = 8000


####################################################
################## OUTPUT FORMAT ###################
####################################################
label = '{}_{}_{}_{}'.format(case, data, sampler, livepoints)
outdir = directory + '/{}_{}/'.format(case, data) + label
bilby.utils.check_directory_exists_and_if_not_mkdir(outdir)


####################################################
############# MODEL & PRIOR SELECTION ##############
####################################################
# Bowman (2018) and Hills (2018) Linearised Foreground with Flattened Gaussian Signal
if case == 'linearised_model':
    model = models.linearised_model
    model_priors = {'A':[[0.0, 20.0], r'$A$'],
                    'nu0':[[60.0, 90.0], r'$\nu_{0}$'], 
                    'w':[[1.0, 40.0], r'$w$'], 
                    'tau':[[0.0, 100.0], r'$\tau$'], 
                    'a0':[[-11000.0, -9000.0], r'$a_{0}$'], 
                    'a1':[[-5900.0, -5400.0], r'$a_{1}$'], 
                    'a2':[[-1950.0, -1700.0], r'$a_{2}$'], 
                    'a3':[[120.0, 190.0], r'$a_{3}$'], 
                    'a4':[[11000.0, 12200.0], r'$a_{4}$']}
    # Injection parameters as in Hills (2018)
    theta = dict(A=0.553, nu0=78.31, w=18.74, tau=6.78, a0=-10111.419, a1=-5673.739, a2=-1831.621, a3=150.673, a4=11711.500)

# Hills (2018) 5-term Polynomial Foreground with Sinusoidal Signal
elif case == 'systematic_model':
    model = models.systematic_model
    model_priors = {'A':[[0.0, 1.0], r'$A$'],
                    'phi':[[1.5 * np.pi, 2.5 * np.pi], r'$\phi$'], 
                    'l':[[11.0, 14.0], r'$l$'], 
                    'a0':[[2500, 2700], r'$a_{0}$'], 
                    'a1':[[-4500, -3900], r'$a_{1}$'], 
                    'a2':[[8100, 9200], r'$a_{2}$'], 
                    'a3':[[-9400, -8500], r'$a_{3}$'], 
                    'a4':[[4200, 4900], r'$a_{4}$'],
                    'a5':[[-1000, -800], r'$a_{5}$']}
    
    # Injection parameters as in Hills (2018)
    theta = dict(A=0.057, phi=5.74, l=12.27, a0=2625.771, a1=-4202.081, a2=8636.317, a3=-8954.631, a4=4553.795, a5=-908.957)

# Ares Simulation Model
elif case == 'ares_model':
    model = ares_sim.model_test
    model_priors = {'fX':[[0.0, 1.0], r'$f_{X}$'],
                    'fstar':[[0.0,1.0], r'$f_{\star}$']}
    
    # Injection parameters: Test values
    theta = dict(fX=0.5, fstar=0.5)


# Convert priors to required format required for bilby
priors = dict()
for k,v in model_priors.items():
    priors[k] = bilby.core.prior.Uniform(minimum=v[0][0], maximum=v[0][1], name=k, latex_label=v[1])


####################################################
############### IMPORT/SIMULATE DATA ############### 
####################################################
# Import EDGES data
if data == 'edges':
    nu, weight, Tsky, Tres1, Tres2, Tmodel, T21, err = edges.read_edges()

# Simulate mock data using model + gaussian errors
elif data == 'mock':
    nu = np.linspace(50.0, 100.0)          
    N = len(nu)
    err = 0.01 * np.ones(N)           
    Tsky = model(nu, **theta) + np.random.normal(0.0, err, N)

# Simulate mock data using ARES + gaussian erros
elif data == 'ares':
    nu, T21 = ares_sim.simulation_test(**theta)
    N = len(nu)
    err = 0.01 * np.ones(N)
    Tsky = T21 + np.random.normal(0.0, err, N)


####################################################
##################### SAMPLER ######################
####################################################
# Instantiate a Gaussian likelihood         NOTE: Might refashion this as to generalise/modularise the selection of different types of likelihoods
likelihood = bilby.likelihood.GaussianLikelihood(nu, Tsky, model, err)

# Run sampler
result = bilby.run_sampler(likelihood=likelihood, injection_parameters=theta, sample='unif', priors=priors, 
                            sampler=sampler, nlive=livepoints, outdir=outdir, label=label, plot=True)

stop = process_time()
print("Elapsed time:", stop-start)