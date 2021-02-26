#!/usr/bin/env
"""
ARES 21 cm signal simulations.

@author: Jesse Cross, MSci Physics at Imperial College London
Contact: jesse.cross17@imperial.ac.uk
@author: Ivan Lim, MSci Physics at Imperial College London
Contact: yi.lim17@imperial.ac.uk
"""

####################################################
#################### LIBRARIES #####################
####################################################
import os
import numpy as np
import matplotlib.pyplot as plt
import ares
import bilby
import math as m
from scipy.interpolate import interp1d

####################################################
###################### PATH ########################
####################################################
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))   # Directory of ares_sim.py (should be lib)
BASE_DIR = os.path.dirname(PROJECT_ROOT)                    # Parent directory of PROJECT_ROOT (should be 21sampler)

####################################################
##################### MODELS #######################
####################################################
def simulation(fX, fstar):
    # Directory and file name
    outdir = '{}/samples/temp'.format(BASE_DIR)
    label = 'sim_ares'
    bilby.utils.check_directory_exists_and_if_not_mkdir(outdir)

    sim = ares.simulations.Global21cm(fX=fX, fstar=fstar)
    sim.run()
    ax, zax = sim.GlobalSignature(color='k', fig=1)
    plt.savefig('{}/{}.png'.format(outdir, label), dpi=300)

    nu_sim = sim.history['nu']
    T21_sim = sim.history['dTb']

    return nu_sim, T21_sim

def model(nu, fX, fstar):
    '''
    Functional form of 21cm Global signal should go here.
    '''
    sim = ares.simulations.Global21cm(fX=fX, fstar=fstar)
    sim.run()
    nu_mod = sim.history['nu']
    T21_mod = sim.history['dTb']

    f = interp1d(nu_mod, T21_mod, fill_value="extrapolate") # Create function
    T21_model_new = f(nu)   # Create new data point from function

    return T21_model_new




# def mirocha2017():
#     # Directory and file name
#     outdir = '{}/samples/temp'.format(BASE_DIR)
#     label = 'mirocha2017'
#     bilby.utils.check_directory_exists_and_if_not_mkdir(outdir)

#     pars = ares.util.ParameterBundle('bowman2018')
#     sim = ares.simulations.Global21cm(**pars)
#     sim.run()
#     nu = sim.history['nu']
#     T21 = sim.history['dTb']
#     ax, zax = sim.GlobalSignature(color='k', fig=1)
#     plt.savefig('{}/{}.png'.format(outdir, label), dpi=300)

#     return nu, T21, pars

# nu, T21, pars = mirocha2017()
# print(pars)

# def mirocha2017_model():
#     # 
#     xbar_i = Q_HII + (1-Q_HII)*x_e

#     # Equation (8) Mirocha2017 - Differential Brightness Temperature
#     A = 27 * (1 - xbar_i)
#     B = (Omega_b0 * h**2)/(0.023)
#     C = (0.15/(Omega_m0 * h**2)) * ((1+z)/10)
#     D = m.sqrt(C)
#     E = 1 - (T_gamma/T_S)

#     T21 =   A * B * D * E

#     return T21