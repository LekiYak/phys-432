import numpy as np
import matplotlib.pyplot as plt

# all in cgs
rho = 1.0
A = 39.5 * 180
L = 180

def friction_skin(nu):
    return (0.027/2) * L**(-1/7) * rho * A * (nu**(1/7)) * (100)**(-1/7) * 100**(2)

power = friction_skin(0.01) * 100

print(power)

def velocity(nu):
    return power / friction_skin(nu)

# plot for nu between 0.01 and 0.01*10^4
nu = np.arange(0.01, 0.01*10**4, 0.01)
plt.plot(nu, velocity(nu))
plt.xscale('log')
plt.xlabel('$\\nu_{water}$')
plt.ylabel('velocity (cm/s)')
plt.title('Velocity as a function of $\\nu_{water}$')
# make x ticks go from 1 to 10^4
plt.xticks([10**-2, 10**-1, 10**0, 10**1, 10**2], [1, 10, 10**2, 10**3, 10**4])
# make y ticks the percent difference from 100
def percent_diff(val, ref):
    return np.round((val - ref) / ((val + ref) / 2) * 100, 2)
# plt.yticks([100, 90, 80, 70, 60, 50, 40, 30], [percent_diff(100, 100), percent_diff(90, 100), percent_diff(80, 100), percent_diff(70, 100), percent_diff(60, 100), percent_diff(50, 100), percent_diff(40, 100), percent_diff(30, 100)])
plt.show()