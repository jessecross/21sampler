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

####################################################
##################### MODELS #######################
####################################################



def sim_ares(fX, fstar):
    fX = 0.5
    fstar = 0.5
    sim = ares.simulations.Global21cm(fX=fX, fstar=fstar)
    sim.run()
    nu = sim.history['nu']
    T21 = sim.history['dTb']
    
    return nu, T21

sim1= ares.simulations.Global21cm()
sim1.run()
sim1.GlobalSignature(fig=1)
plt.show()




