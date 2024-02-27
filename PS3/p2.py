import numpy as np
import matplotlib.pyplot as plt

# all in cgs
rho = 1.0
A = 40 * 180
L = 180

def friction_laminar(nu):
    return 1449 * 2**(7/2) * nu**(1/2) / 125

def friction_turbulent(nu):
    return (180**(13/7) - 18**(13/7)) * nu**(1/7) / 13*100**(8/7)

power = (friction_laminar(0.01)  + friction_turbulent(0.01)) * 100 * 2

print(power)

def velocity(nu):
    return power / (2 * (friction_laminar(nu) + friction_turbulent(nu)))

# plot for nu between 0.01 and 0.01*10^4
nu = np.arange(0.01, 0.01*10**4, 0.01)
plt.plot(nu, velocity(nu))

# plot veritcal line
# plt.axvline(x=1*10**(-2), color='b', linestyle='--', label='$\\nu_{Water} = 1cS$')
# plt.axvline(x=73*10**(-2), color='r', linestyle='--', label='$\\nu_{Honey} = 73cS$')
# plt.axvline(x=6200*10**(-2), color='g', linestyle='--', label='$\\nu_{Molasses} = 6200cS$')

# plot horizontal line
plt.axhline(y=99.7, color='r', linestyle='--', label='-0.3%, Olympic')
plt.axhline(y=66, color='b', linestyle='--', label='-40%, Recreation')

plt.xscale('log')
plt.xlabel('$\\nu_{water}$')
plt.ylabel('Percentage difference')
plt.title('Velocity as a function of $\\nu_{water}$')
plt.legend()
# make x ticks go from 1 to 10^4
plt.xticks([10**-2, 10**-1, 10**0, 10**1, 10**2], [1, 10, 10**2, 10**3, 10**4])
# make y ticks the percent difference from 100
def percent_diff(val, ref):
    return np.round((val - ref) / ((val + ref) / 2) * 100, 2)
plt.yticks([100, 90, 80, 70, 60, 50, 40, 30], [percent_diff(100, 100), percent_diff(90, 100), percent_diff(80, 100), percent_diff(70, 100), percent_diff(60, 100), percent_diff(50, 100), percent_diff(40, 100), percent_diff(30, 100)])
plt.show()