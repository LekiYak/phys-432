"""




"""
import numpy as np
import matplotlib.pyplot as plt

dt = 0.01
Nsteps = 1000

## Set up initial conditions (vortex centres and circulation)
# Vortex rings
y_vortices = np.array([])
x_vortices = np.array([])
k_vortices = np.array([])

# Setting up the plot
plt.ion()
fig, ax = plt.subplots(1,1)
# mark the initial positions of vortices
p, = ax.plot(x_vortices, y_vortices, 'k+', markersize=10)

# draw the initial velocity streamline
ngrid = 100
Y, X = np.mgrid[-ngrid:ngrid:360j, -ngrid:ngrid:360j]
x_velocity = np.zeros_like(X)
y_velocity = np.zeros_like(Y)

# masking radius for better visualization
mask_radius = 10

# velocity field calculations
for i in range(len(x_vortices)):
    break

## plot the velocity field
# Boundaries
ax.set_xlim(-ngrid, ngrid)
ax.set_ylim(-ngrid, ngrid)

# Initial strewamline
ax.streamplot(X, Y, x_velocity, y_velocity, density=[1, 1])

# Update the plot
fig.canvas.draw()

# Time evolution
count = 0

while count < Nsteps:
    