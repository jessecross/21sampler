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
import models                      # signal models
import edges                       # edges data
import ares_sim                    # ares simulations


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
livepoints = 70


####################################################
################## OUTPUT FORMAT ###################
####################################################
label = '{}_{}_{}_{}'.format(case, data, sampler, livepoints)
outdir = directory + '/{}_{}/'.format(case, data) + label
bilby.utils.check_directory_exists_and_if_not_mkdir(outdir)


####################################################
############### PARAMETER PRIORS ###################    NOTE: Will refashion this to associate to the model (class structure) within models.py
####################################################
# Priors for absorption profile as stated in Hills (2018). Foreground priors are eye-balled from their plots since no data given in Bowman (2018) or Hills (2018)
linearised_model_priors = {'A':[0.0, 20.0],
                        'nu0':[60.0, 90.0], 
                        'w':[1.0, 40.0], 
                        'tau':[0.0, 100.0], 
                        'a0':[-11000.0, -9000.0], 
                        'a1':[-5900.0, -5400.0], 
                        'a2':[-1950.0, -1700.0], 
                        'a3':[120.0, 190.0], 
                        'a4':[11000.0, 12200.0]}

# Priors taken from Jonathan's code and slightly fiddled with itertively to find a good range.
systematic_model_priors = {'A':[0.0, 1.0],
                        'phi':[1.5 * np.pi, 2.5 * np.pi], 
                        'l':[11.0, 14.0], 
                        'a0':[2500, 2700], 
                        'a1':[-4500, -3900], 
                        'a2':[8100, 9200], 
                        'a3':[-9400, -8500], 
                        'a4':[4200, 4900],
                        'a5':[-1000, -800]}

# Priors created for test run with ARES
ares_model_priors = {'fX':[0.0, 1.0],
                'fstar':[0.0,1.0]}


####################################################
############# MODEL & PRIOR SELECTION ##############
####################################################
if case == 'linearised_model':
    model = models.linearised_model
    model_priors = linearised_model_priors
    # Injection parameters: reference values from Hills (2018) for real edges data (and used to generate mock data)
    theta = dict(A=0.553, nu0=78.31, w=18.74, tau=6.78, a0=-10111.419, a1=-5673.739, a2=-1831.621, a3=150.673, a4=11711.500)

elif case == 'systematic_model':
    model = models.systematic_model
    model_priors = systematic_model_priors
    # Injection parameters: reference values from Hills (2018) for real edges data (and used to generate mock data)
    theta = dict(A=0.057, phi=5.74, l=12.27, a0=2625.771, a1=-4202.081, a2=8636.317, a3=-8954.631, a4=4553.795, a5=-908.957)

elif case == 'ares_model':
    model = ares_sim.model_test
    model_priors = ares_model_priors
    theta = dict(fX=0.5, fstar=0.5)


# Convert priors to required form for bilby
priors = dict()
for k,v in model_priors.items():
    priors[k] = bilby.core.prior.Uniform(v[0], v[1], k)


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
##################### SAMPLER ######################
####################################################
# Instantiate a Gaussian likelihood         NOTE: Might refashion this as to generalise/modularise the selection of different types of likelihoods
likelihood = bilby.likelihood.GaussianLikelihood(nu, Tsky, model, err)

# Run sampler
result = bilby.run_sampler(likelihood=likelihood, injection_parameters=theta, sample='unif', priors=priors, 
                            sampler=sampler, nlive=livepoints, outdir=outdir, label=label, plot=True)