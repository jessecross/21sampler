#!/usr/bin/env
"""
Different 21 cm signal and foreground models.
Each function defines a different model.

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
import numpy as np


####################################################
##################### MODELS #######################
####################################################
model_call_counter = 0

########################################################################
# BOWMAN (2018) - Linearised Foreground with Flattened Gaussian Signal #
########################################################################
# 21 cm Signal Model
def flattened_gaussian(nu, A, nu0, w, tau):
    """
    Flattened Gaussian.
    As in Bowman (2018) equations (5) and (6).
    As in Hills (2018) equations (2) and (3).
    """

    B = (4.0 * np.power((nu - nu0), 2.0) / np.power(w, 2.0)) * np.log(-np.log((1.0 + np.exp(-tau))/2.0) / tau)
    T21 = - A * (1.0 - np.exp(-tau * np.exp(B))) / (1.0 - np.exp(-tau))

    return T21

# Foreground Signal Model
def linearised_foreground(nu, a0, a1, a2, a3, a4):
    """
    Linearised Foreground.
    As in Bowman (2018) equation (2).
    As in Hills (2018) equation (8).
    """

    nuc = 75.0          # Foreground central frequency as specified in paper
    x = nu / nuc        # Normalised frequency terms

    Tfg = a0 * np.power(x, -2.5)
    Tfg += a1 * np.power(x, -2.5) * np.log(x)
    Tfg += a2 * np.power(x, -2.5) * np.power(np.log(x), 2.0)
    Tfg += a3 * np.power(x, -4.5)
    Tfg += a4 * np.power(x, -2.0)

    return Tfg

# Combined Model
def linearised_model(nu, A, nu0, w, tau, a0, a1, a2, a3, a4):
    """
    Bowman (2018) and Hills (2018) Linearised Model with Flattened Gaussian
    """

    # global model_call_counter
    # model_call_counter += 1
    # print(f"i={model_call_counter}\t A={A}\t nu0={nu0}\t w={w}\t tau={tau}\t a0={a0}\t a1={a1}\t a2={a2}\t a3={a3}\t a4={a4}")

    T21 = flattened_gaussian(nu, A, nu0, w, tau)
    Tfg = linearised_foreground(nu, a0, a1, a2, a3, a4)

    # Combined signal
    Tsky = T21 + Tfg

    return Tsky


######################################################################
# HILLS (2018) - 5-term Polynomial Foreground with Sinusoidal Signal #
######################################################################
# 21 cm Signal Model (Sinusoidal)
def sinusoidal(nu, A, phi, l):
    """
    Sine Wave. Table 1 in Hills (2018).
    """

    y = ((2.0 * np.pi * nu)/l) + phi 
    T21 = A * np.sin(y)

    return T21

# Foreground Signal Model (5-term Polynomial)
def five_polynomial(nu, a0, a1, a2, a3, a4, a5):
    """
    5-term Polynomial Foreground as in Hills (2018) equation (10).
    """
    
    nuc = 75.0          # Foreground central frequency as specified in Hills (2018)
    x = nu / nuc        # Normalised frequency terms

    Tfg =  a0 * np.power(x, -2.5)
    Tfg += a1 * np.power(x, -1.5)        
    Tfg += a2 * np.power(x, -0.5)
    Tfg += a3 * np.power(x,  0.5) 
    Tfg += a4 * np.power(x,  1.5)
    Tfg += a5 * np.power(x,  2.5)

    return Tfg

# Combined Model
def systematic_model(nu, A, phi, l, a0, a1, a2, a3, a4, a5):
    """
    Hills (2018) 5-term Polynomial Foreground with Sinusoidal Signal
    """

    # global model_call_counter
    # model_call_counter += 1
    # print(f"i={model_call_counter}\t A={A}\t phi={phi}\t l={l}\t a0={a0}\t a1={a1}\t a2={a2}\t a3={a3}\t a4={a4}\t a5={a5}")

    T21 = sinusoidal(nu, A, phi, l)
    Tfg = five_polynomial(nu, a0, a1, a2, a3, a4, a5)

    # Combined signal
    Tsky = T21 + Tfg
    
    return Tsky