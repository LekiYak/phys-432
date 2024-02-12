"""
This script visualises the time evolution of two vortex rings as they leapfrog. The output of this script is a series of images, each corresponding to a frame of the time evolution. These images can be combined to form a gif using another script, software, or online. This script is designed to simulate the leapfroggin up until one of the vortexes exits the simulation domain, at which point the images will cease to be generated and the script will throw an IndexError. By not immediately saving the images as a gif, the user can choose to stop the simulation at any time and still have the images to work with.

@Author: Lekima Yakuden (github.com/LekiYak)
Date: 2024-02-12
"""
import numpy as np
import matplotlib.pyplot as plt

dt = 0.25 # 0.5 works well too
Nsteps = 100 # Redundant, but just in case

## set up initial conditions (vortex centres and circulation)
# vortex rings
y_vortices = np.array([55, 55, -55, -55])
x_vortices = np.array([-95, -80, -95, -80])
k_vortices = np.array([5, 5, -5, -5])

# setting up the plot
plt.ion()
fig, ax = plt.subplots(1,1)
# mark the initial positions of vortices
p, = ax.plot(x_vortices, y_vortices, 'k+', markersize=10, markeredgewidth=2)

# generate the grid for the X and Y velocity fields
ngrid = 100 # total dimenison of the grid
Y, X = np.mgrid[-ngrid:ngrid:400j, -ngrid:ngrid:400j] # subdivide 2*ngrid into 400 parts
x_velocity = np.zeros_like(X)
y_velocity = np.zeros_like(X)

# velocity field calculations
def velocity_field(x_vortices, y_vortices, k_vortices, X, Y, x_velocity, y_velocity):
    """
    Calcualtes the X and Y components of the velocity field due to the vortices.

    INPUTS:
    x_vortices: x-coordinates of the vortices
    y_vortices: y-coordinates of the vortices
    k_vortices: circulation of the vortices
    X: X grid
    Y: Y grid
    x_velocity: X component of the velocity field [initially zero]
    y_velocity: Y component of the velocity field [initially zero]
    
    OUTPUTS:
    x_velocity: X component of the velocity field
    y_velocity: Y component of the velocity field
    """

    for i in range(len(x_vortices)):
        ## Compute total velocity field
        # Distance from each grid cell to the vortex
        r = np.sqrt((X - x_vortices[i])**2 + (Y - y_vortices[i])**2)

        # Velocity field of each vortex
        x_velocity += -k_vortices[i] * (Y - y_vortices[i]) /  r 
        y_velocity += k_vortices[i] * (X - x_vortices[i]) / r
        
    return x_velocity, y_velocity

# initial velocity field
x_velocity, y_velocity = velocity_field(x_vortices, y_vortices, k_vortices, X, Y, x_velocity, y_velocity)

## plot the initial velocity field
# boundaries
ax.set_xlim(-ngrid, ngrid)
ax.set_ylim(-ngrid, ngrid)

# initial strewamline
ax.streamplot(X, Y, x_velocity, y_velocity, density=[1, 1])

# make aspect ratio equal
ax.set_aspect('equal')

# draw the plot
fig.canvas.draw()

# save the initial plot
fig.savefig('vortex_initial.png', bbox_inches='tight')

## time evolution
# initialize counter
count = 0

while count < Nsteps:
    ## compute and update advection velocity
    # advection velocity
    advection_x = np.zeros_like(x_vortices)
    advection_y = np.zeros_like(y_vortices)
    # find the velocity at each of the vortex positions from the other vortices
    for i in range(len(x_vortices)):

        # remove the i-th vortex from the vortex list and recalculate the velocity field
        x_vortices_temp = np.delete(x_vortices, i) # temporary vortex list, without the i-th vortex
        y_vortices_temp = np.delete(y_vortices, i)
        k_vortices_temp = np.delete(k_vortices, i)
        x_velocity_temp = np.zeros_like(X) # temporary velocity field
        y_velocity_temp = np.zeros_like(X)
        x_velocity_temp, y_velocity_temp = velocity_field(x_vortices_temp, y_vortices_temp, k_vortices_temp, X, Y, x_velocity_temp, y_velocity_temp)

        # find the velocity at the i-th vortex position
        x_advection = x_velocity_temp[int((y_vortices[i]+ngrid)/0.5)][int((x_vortices[i]+ngrid)/0.5)]
        y_advection = y_velocity_temp[int((y_vortices[i]+ngrid)/0.5)][int((x_vortices[i]+ngrid)/0.5)]

        # update the advection velocity
        advection_x[i] = x_advection
        advection_y[i] = y_advection

    # for monitoring
    print(count, advection_x, advection_y, x_vortices, y_vortices)

    # update vortex positions
    np.add(x_vortices, advection_x * dt, out=x_vortices, casting="unsafe")
    np.add(y_vortices, advection_y * dt, out=y_vortices, casting="unsafe")

    # recalculate velocity field
    x_velocity = np.zeros_like(X)
    y_velocity = np.zeros_like(X)
    x_velocity, y_velocity = velocity_field(x_vortices, y_vortices, k_vortices, X, Y, x_velocity, y_velocity)

    ## plot the velocity field
    # clear the previous plot
    ax.clear()
    
    # plot streamlines and vortex centres
    ax.streamplot(X, Y, x_velocity, y_velocity, density=[1, 1])
    p, = ax.plot(x_vortices, y_vortices, 'k+', markersize=10, markeredgewidth=2)

    # set title as timestep
    ax.set_title('Timestep: {}'.format(count))

    # save figure
    fig.savefig('vortex_{:03d}.png'.format(count), bbox_inches='tight')

    count += 1
