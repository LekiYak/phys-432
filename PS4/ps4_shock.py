"""
PHYS 432 Problem Set 4, Question 3

@Author: Lekima Yakuden
Date: 2024-03-25
"""

import numpy as np 
import matplotlib.pyplot as plt
import imageio

## Initial conditions and parameters
# grid parameters
L      = 1 # length of the simulation in m
Ngrid  = 200 # number of grid points
Nsteps = 500 # number of time steps
dt     = 0.01 # time step
dx     = L/Ngrid # grid spacing

# constants
gamma = 1.4 # adiabatic index

# initial conditions
x = np.arange(Ngrid) * dx
rho = np.ones(Ngrid) # density
rho_u = np.zeros(Ngrid) # momentum density
rho_e = np.ones(Ngrid) # energy density

# add pertubation in energy density
rho[10:12] = 1.05
rho_u[10:12] = 0.1

advection = np.zeros(Ngrid) # rightgoing advection
pressure = np.zeros(Ngrid) # pressure
cs = np.ones(Ngrid) # sound speed

## donor cell advection
def cell_wall_velocity(i):
    return 0.5 * (rho_u[i] / rho[i] - rho_u[i+1] / rho[i+1])

def advect(q, dx, dt, i):

    right_flux = 0
    left_flux = 0

    # flux conditions
    if advection[i] > 0:
        right_flux = advection[i] * q[i]
    elif advection[i] < 0:
        right_flux = advection[i] * q[i+1]
    else:
        right_flux = 0

    if advection[i-1] > 0:
        left_flux = advection[i-1] * q[i-1]
    elif advection[i-1] < 0:
        left_flux = advection[i-1] * q[i]
    else:
        left_flux = 0

    # update q
    return q[i] - dt/dx * (right_flux - left_flux)

## time evolution

# set up plot with rho on top and mach number on bottom for animation
plt.ion()
fig, ax = plt.subplots(2, 1)
plt1, = ax[0].plot(x, rho, 'r')
plt2, = ax[1].plot(x, advection, 'b')

frames = []

for i in range(Nsteps):
    
    # compute advection velocities for i=1 to Ngrid-2
    j=0
    for j in range(1, Ngrid-2):
        advection[j] = cell_wall_velocity(j)
    advection[0] = 0
    advection[Ngrid-1] = 0

    print(advection)

    # advect density
    j=0
    for j in range(1, Ngrid-2):
        rho[j] = advect(rho, dx, dt, j)

    # advect momentum density
    j=0
    for j in range(1, Ngrid-2):
        rho_u[j] = advect(rho_u, dx, dt, j)

    # compute pressure
    pressure = (gamma - 1) * rho_e

    # compute sound speed
    cs = np.sqrt(gamma * pressure / rho)

    # pressure gradient term for momentum
    j=0
    for j in range(1, Ngrid-2):
        rho_u[j] = rho_u[j] - cs[j]**2 * dt/dx * (rho[i+1] - rho[i-1])
    rho_u[0] = rho_u[0] - 0.5 * (dt/dx) * (pressure[1] - pressure[0])
    rho_u[Ngrid-1] = rho_u[Ngrid-1] - 0.5 * (dt/dx) * (pressure[Ngrid-1] - pressure[Ngrid-2])

    # recalcualte advection velocities
    j=0
    for j in range(1, Ngrid-1):
        advection[j] = cell_wall_velocity(j)
    advection[0] = 0
    advection[Ngrid-1] = 0

    # advect energy density
    j=0
    for j in range(1, Ngrid-2):
        rho_e[j] = advect(rho_e, dx, dt, j)

    # recalculate pressure
    pressure = (gamma - 1) * rho_e

    # pressure gradient term for energy
    j=0
    for j in range(1, Ngrid-2):
        rho_e[j] = rho_e[j] - cs[j]**2 * (dt/dx) * (rho[i+1] - rho[i-1])
    rho_e[0] = rho_e[0] - 0.5 * (dt/dx) * (pressure[1] - pressure[0])
    rho_e[Ngrid-1] = rho_e[Ngrid-1] - 0.5 * (dt/dx) * (pressure[Ngrid-1] - pressure[Ngrid-2])

    # recalculate pressure
    pressure = (gamma - 1) * rho_e

    # recalculate sound speed
    cs = np.sqrt(gamma * pressure / rho)

    plt1.set_ydata(rho)
    plt2.set_ydata((rho_u / rho) / cs)

    ax[0].set_xlim([0, L])
    ax[0].set_ylim([0, 3])
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('Density')
    ax[0].set_title('Density Profile (t = {})'.format(i))

    ax[1].set_xlim([0, L])
    ax[1].set_ylim([-5, 5])
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('Mach Number')
    ax[1].set_title('Mach Number Profile (t = {})'.format(i))

    fig.canvas.draw()
    plt.pause(0.05)

    current_frame = np.array(fig.canvas.renderer._renderer) # convert plot to array
    frames.append(current_frame) # append plot to list

# save animation
imageio.mimsave('shock.gif', frames, fps=10)
