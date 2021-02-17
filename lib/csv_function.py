import os
#os.environ["ARES"] = "/Users/ivanlim/ares/"
import ares
import matplotlib.pyplot as pl

'https://ares.readthedocs.io/en/latest/fields.html?highlight=cgm#two-zone-igm-models' #PARAMETER DEFINITIONS

sim1 = ares.simulations.Global21cm()      # Initialize a simulation object
sim1.run()  
#pl.plot(sim.history['x'], sim.history['dTb'])  #ValueError: x, y, and format string must not be None
sim1.GlobalSignature(fig=1)

sim1.save('/Users/ivanlim/Desktop/csv files/sim1', suffix='csv', clobber='True')


'''
ax= None
for i, fX in enumerate([0.01,0.05,0.5,1]): #Increasing fX shifts 3rd and 4th turning points of the signal up and to the left
    sim3= ares.simulations.Global21cm(fX=fX, fstar=1)
    sim3.run()
    ax, zax = sim3.GlobalSignature(fig=2, label=r'$f_X=%.2g, f_{\ast}=%.2g$' % (fX, fstar))
    
ax.legend(loc='lower right', fontsize=14)

bx= None
for j, fstar1 in enumerate([0.01,0.05,0.5,1]): #Decreasing f* shifts the 3rd TP up and rightwards; 4th TP down leftwards
    sim4= ares.simulations.Global21cm(fX=1, fstar=fstar1)
    sim4.run()
    bx, zbx = sim4.GlobalSignature(fig=3, label=r'$f_X=%.2g, f_{\ast}=%.2g$' % (fX, fstar1))
    
bx.legend(loc='lower right', fontsize=14)
'''
'''
sim4 = ares.simulations.Global21cm(fx=0.5, fstar=0.5)
sim4.run()
sim4.GlobalSignature(fig=1)
'''