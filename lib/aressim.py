#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 22:45:50 2021

@author: ivanlim
"""
import os
os.environ["ARES"] = "/Users/ivanlim/ares/"
import ares
import numpy as np
import matplotlib.pyplot as pl

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
pl.show()




