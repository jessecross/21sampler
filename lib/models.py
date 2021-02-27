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

def linearised_model(nu, A, nu0, w, tau, a0, a1, a2, a3, a4):
    """
    Flattened Gaussian 21cm and Linearised Foreground
    Model as in Bowman (2018). Foreground signal - Equation (2). 21 cm signal - Equations (5) and (6).
    Also as in Hills (2018). Foreground signal - Equation (8). 21 cm signal - Equations (2) and (3).
    """
    
    # 21 cm Signal Model (Flattened Gaussian Profile)
    B = (4.0 * np.power((nu - nu0), 2.0) / np.power(w, 2.0)) * np.log(-np.log((1.0 + np.exp(-tau))/2.0) / tau)
    T21 = - A * (1.0 - np.exp(-tau * np.exp(B))) / (1.0 - np.exp(-tau))
    
    # Foreground Signal Model (Linearised emission)
    nuc = 75.0          # Foreground central frequency as specified in paper
    x = nu / nuc        # Normalised frequency terms

    Tfg = a0 * np.power(x, -2.5)
    Tfg += a1 * np.power(x, -2.5) * np.log(x)
    Tfg += a2 * np.power(x, -2.5) * np.power(np.log(x), 2.0)
    Tfg += a3 * np.power(x, -4.5)
    Tfg += a4 * np.power(x, -2.0)

    # Combined signal
    Tsky = T21 + Tfg

    return Tsky


def systematic_model(nu, A, phi, l, a0, a1, a2, a3, a4, a5):
    """
    Flattened Gaussian 21cm and 5-term Polynomial Foreground.
    Model as in Hills (2018). Foreground signal - Equation (10). 21 cm signal - Equation within Table 1.
    """

    # 21 cm Signal (Sinusoidal)
    y = ((2.0 * np.pi * nu)/l) + phi 
    T21 = A * np.sin(y)

    # Foreground signal
    nuc = 75.0          # Foreground central frequency as specified in Hills (2018)
    x = nu / nuc        # Normalised frequency terms

    Tfg =  a0 * np.power(x, -2.5)
    Tfg += a1 * np.power(x, -1.5)        
    Tfg += a2 * np.power(x, -0.5)
    Tfg += a3 * np.power(x,  0.5) 
    Tfg += a4 * np.power(x,  1.5)
    Tfg += a5 * np.power(x,  2.5)

    # Combined signal
    Tsky = T21 + Tfg
    
    return Tsky