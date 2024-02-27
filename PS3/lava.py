"""
PHYS 432 Problem Set 3, Question 3

@Author: Lekima Yakuden
Date: 2024-02-26
"""

import numpy as np 
import matplotlib.pyplot as plt
import imageio

## Initial conditions and parameters
# grid parameters
H       = 200 # height of the flow in cm
Ngrid   = 200 # number of grid points
Nsteps  = 500 # number of time steps
dt      = 0.02 # time step
dx      = H/Ngrid # grid spacing

# fluid parameters
alpha       = 30 # slope angle in degrees
viscosity   = 10**4 # viscosity in cm^2/s
beta        = viscosity*dt/dx**2 # matrix entry, derived in class
g           = 981 # gravity in cm/s^2

# diffusion matrix
A = np.eye(Ngrid) * (1 + 2 * beta) - np.eye(Ngrid, k=1) * beta - np.eye(Ngrid, k=-1) * beta
A[-1][-1] = 1.0 + beta # no stress condition
A[0][0] = 1 # first cell boundary conditions
A[0][1] = 1

## Set up grid
# grid
y = np.arange(Ngrid) * dx

# initial velocity field (u=0 everywhere)
u = np.zeros(Ngrid)

## Plotting
# set up plot
plt.ion()
fig, ax = plt.subplots()

# steady state solution
def steadystate(y):
    return -(g / viscosity) * np.sin(np.deg2rad(alpha)) * (0.5 * y**2 - H * y)

# plot steady state solution 
ax.plot(y, steadystate(y), '-')

# plotting objects
plt1, = ax.plot(y, u, 'ro')

# setting plotl imits and labels
ax.set_xlim([0, H])
ax.set_ylim([-5, steadystate(H) + steadystate(H) * 0.1])
ax.set_xlabel('Height (cm)')
ax.set_ylabel('Velocity (cm/s)')

## Time evolution
# time counter
count = 0

# list to store all plots
frames = []

# evolution
while count < Nsteps:
    # diffusion
    u = np.linalg.solve(A, u)

    # gravitational advection
    u = u + dt * g * np.sin(np.deg2rad(alpha))

    # no slip condition
    u[0] = 0

    # plot
    plt1.set_ydata(u)

    # update title
    ax.set_title('Velocity Profile (t = {})'.format(count))
    plt.legend(['Steady State', 't-dep Profile'])

    # update plot
    fig.canvas.draw()
    plt.pause(0.05)

    # check for steady state, break loop if achieved
    if u[-1] > steadystate(H):
        break

    current_frame = np.array(fig.canvas.renderer._renderer) # convert plot to array
    frames.append(current_frame) # append plot to list

    count += 1

# save animation
imageio.mimsave('lava.gif', frames, duration=2)
