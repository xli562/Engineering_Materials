from random import random
import numpy as np
from matplotlib import pyplot as plt

taus = []      # List of shear stresses. Shear stress = 1 / average of the least distances
# Physical constants
V_Zn = 0.0193364568*(10**-27)   # Volume a Zinc atom = (0.278)^3*0.9*1e-27
V_Cu = 0.0150994944*(10**-27)   # Volume a Copper atom = (0.256)^3*0.9*1e-27
cube_sidelength = 2e-9           # Side length of the cube in meters
# Looping parameters
nstart = 10
nend = 1000
nstep = 10
sample_size = len(range(nstart,nend,nstep))
for n in range(nstart,nend,nstep):
    # Running for more times for smaller n's for smooth data
    acc = 0.0
    runCount = 20#int(nend/n)
    for run in range(runCount):
        print(f'running{n}...')
        # Initilizing variables at the start of each loop
        points = []     # The list of n points
        rmin = 1.8      # The minimum distance between a certain point and other points
        rmins = []      # The list containing rmin
        rmin_avg = 0.0 

        # Generating list of points containing n 3-dimensional points in space.
        for i in range(n):
            for j in range(3):
                point = (cube_sidelength*random(), cube_sidelength*random(), cube_sidelength*random())
            points.append(point)

        for point in points:
            for otherpoint in points:
                if otherpoint != point:
                    # Calculating distance from 'point' to every 'otherpoint'
                    delx2 = np.square(point[0] - otherpoint[0])
                    dely2 = np.square(point[1] - otherpoint[1])
                    delz2 = np.square(point[2] - otherpoint[2])
                    r = np.sqrt(delx2+dely2+delz2)
                    # Obtaining the closest distance to the adjacent point
                    if rmin > r:
                        rmin = r
                    rmins.append(rmin)
        # Taking the average of all closest distatnces to adjacent points
        for rmin in rmins:
            rmin_avg += rmin
        rmin_avg /= len(rmins)
        acc += rmin_avg
    rmin_avg = acc / runCount
    taus.append(1/rmin_avg)

# Fitting and plotting
Cs = []     # List of concentrations
for n in range(nstart,nend,nstep):
    Cs.append(n/(n+(cube_sidelength**3-n*V_Zn)/V_Cu))
plt.plot(Cs, taus)
tau_max = 0
tau_min = taus[0]
for tau in taus:
    if tau_max < tau:
        tau_max = tau
    if tau_min > tau:
        tau_min = tau
resolution = 2*sample_size
step = (tau_max - tau_min)/resolution
Cs_reversed = Cs
Cs_reversed.reverse()
polyCoeff = np.polyfit(taus, Cs_reversed, 2)
fitted_taus = [tau_min]
fitted_Cs_reversed = []
for i in range(resolution):
    fitted_taus.append(fitted_taus[-1] + step)
for fitted_tau in fitted_taus:
    fitted_Cs_reversed.append(polyCoeff[0] * np.square(fitted_tau) + polyCoeff[1] * fitted_tau + polyCoeff[2])
fitted_Cs = fitted_Cs_reversed
fitted_Cs.reverse()
plt.plot(fitted_Cs, fitted_taus)
plt.show()




'''# Fitting and plotting
Cs = []     # List of concentrations
for n in range(nstart,nend,nstep):
    Cs.append(n/(n+(cube_sidelength**3-n*V_Zn)/V_Cu))
    # Fitting
        # Finding max item in rmin_avgs:
rmin_avg_max = 0.0
rmin_avg_min = 1.8
for rmin_avg in rmin_avgs:
    if rmin_avg_max < rmin_avg:
        rmin_avg_max = rmin_avg
    if rmin_avg_min > rmin_avg:
        rmin_avg_min = rmin_avg

polyCoeff = np.polyfit(np.divide(1,rmin_avgs), Cs, 2)
resolution = 2 * len(Cs)
step = (1/rmin_avg_max-1/rmin_avg_min) / resolution
yfits = [1/rmin_avg_min]
xfits = []
for i in range(resolution):
    yfits.append(yfits[-1] + step)

for yfit in yfits:
    xfits.append(polyCoeff[0] * np.square(yfit) + polyCoeff[1] * yfit + polyCoeff[2])

plt.plot(xfits, yfits)

plt.plot(Cs, np.divide(1,rmin_avgs))

plt.show()'''

