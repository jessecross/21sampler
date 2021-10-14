#!/usr/bin/env python3

import bilby
import numpy as np
import matplotlib.pyplot as plt
import os

####################################################
###################### PATH ########################
####################################################
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))   # Directory of sampler.py (should be ~/21sampler/lib)
BASE_DIR = os.path.dirname(PROJECT_ROOT)                    # Parent directory of PROJECT_ROOT (should be ~/21sampler)
directory = '{}/samples'.format(BASE_DIR)                   # Directory where samples are saved (should be ~/21sampler/samples)

####################################################
################## OUTPUT FORMAT ###################
####################################################
sampler = 'dynesty'

label = 'linear_regression_unknown_noise'
outdir = directory + '/test/' + sampler
bilby.utils.check_directory_exists_and_if_not_mkdir(outdir)


# First, we define our "signal model", in this case a simple linear function
def model(time, m, c):
    return time * m + c


# Now we define the injection parameters which we make simulated data with
injection_parameters = dict(m=0.5, c=0.2)

# For this example, we'll inject standard Gaussian noise
sigma = 1

# These lines of code generate the fake data. Note the ** just unpacks the
# contents of the injection_parameters when calling the model function.
sampling_frequency = 10
time_duration = 10
time = np.arange(0, time_duration, 1 / sampling_frequency)
N = len(time)
data = model(time, **injection_parameters) + np.random.normal(0, sigma, N)

# We quickly plot the data to check it looks sensible
fig, ax = plt.subplots()
ax.plot(time, data, 'o', label='data')
ax.plot(time, model(time, **injection_parameters), '--r', label='signal')
ax.set_xlabel('time')
ax.set_ylabel('y')
ax.legend()
fig.savefig('{}/{}_data.png'.format(outdir, label))

injection_parameters.update(dict(sigma=1))

# Now lets instantiate the built-in GaussianLikelihood, giving it
# the time, data and signal model. Note that, because we do not give it the
# parameter, sigma is unknown and marginalised over during the sampling
likelihood = bilby.core.likelihood.GaussianLikelihood(time, data, model)

priors = dict()
priors['m'] = bilby.core.prior.Uniform(0, 5, 'm')
priors['c'] = bilby.core.prior.Uniform(-2, 2, 'c')
priors['sigma'] = bilby.core.prior.Uniform(0, 10, 'sigma')

# And run sampler
result = bilby.run_sampler(
    likelihood=likelihood, priors=priors, sampler=sampler, npoints=500,
    sample='unif', injection_parameters=injection_parameters, outdir=outdir,
    label=label)
result.plot_corner()
