"""




"""
import numpy as np
import matplotlib.pyplot as plt

dt = 0.5
Nsteps = 100

## Set up initial conditions (vortex centres and circulation)
# Vortex rings
y_vortices = np.array([0, -0])#, 50, -50])
x_vortices = np.array([-25, 25])#, -60, -60])
k_vortices = np.array([5, 5])#, 5, -5])

# Setting up the plot
plt.ion()
fig, ax = plt.subplots(1,1)
# mark the initial positions of vortices
p, = ax.plot(x_vortices, y_vortices, 'k+', markersize=10, markeredgewidth=2)

# draw the initial velocity streamline
ngrid = 100
Y, X = np.mgrid[-ngrid:ngrid:400j, -ngrid:ngrid:400j]
x_velocity = np.zeros_like(X)
y_velocity = np.zeros_like(X)

# print(Y)  # Y ARRAY IS [[BOTTOM], [BOTTOM+1], .. [TOP]] (Y AXIS), each row is the same
# [int((-y+80)/0.4)][int((-x+80)/0.4)] to get index of point y
# print(X) # X ARRAY IS ALSO [[BOTTOM], [BOTTOM+1], .. [TOP]] (X AXIS), each column is the same
# [int((-y+80)/0.4)][int((-x+80)/0.4)] to get index of point x,y for the x information

# masking radius for better visualization
mask_radius = 1

# velocity field calculations
def velocity_field(x_vortices, y_vortices, k_vortices, X, Y, mask_radius, x_velocity, y_velocity):
    for i in range(len(x_vortices)):
        ## Compute total velocity field
        # Distance from each grid cell to the vortex
        r = np.sqrt((X - x_vortices[i])**2 + (Y - y_vortices[i])**2)

        # Velocity field of each vortex
        x_velocity += -k_vortices[i] * (Y - y_vortices[i]) /  r
        y_velocity += k_vortices[i] * (X - x_vortices[i]) / r
        
        # mask the velocity field with NaNs
        # x_velocity[r < mask_radius] = np.nan
        # y_velocity[r < mask_radius] = np.nan
    
    return x_velocity, y_velocity

# initial velocity field
x_velocity, y_velocity = velocity_field(x_vortices, y_vortices, k_vortices, X, Y, mask_radius, x_velocity, y_velocity)

# test for velocity field
# print(x_velocity[int((0+80)/0.4)][int((15+80)/0.4)])
# print(x_velocity[int((0+80)/0.4)][int((-15+80)/0.4)])
# print(y_velocity[int((0+80)/0.4)][int((-40+80)/0.4)])
# so it's int((y+80)/0.4) for y and int((x+80)/0.4) for x

## Plot the velocity field
# Boundaries
ax.set_xlim(-ngrid, ngrid)
ax.set_ylim(-ngrid, ngrid)

# Initial strewamline
ax.streamplot(X, Y, x_velocity, y_velocity, density=[1, 1])

# Update the plot
fig.canvas.draw()

fig.savefig('vortex_initial.png')

## Time evolution
# Initialize counter
count = 0

while count < Nsteps:
    ## Computer and update advection velocity

    # Advection velocity
    advection_x = np.zeros_like(x_vortices)
    advection_y = np.zeros_like(y_vortices)
    # find the velocity at each of the vortex positions from the other vortices
    for i in range(len(x_vortices)):
        x_advection = x_velocity[int((y_vortices[i]+100)/0.5)][int((x_vortices[i]+100)/0.5)]
        y_advection = y_velocity[int((y_vortices[i]+100)/0.5)][int((x_vortices[i]+100)/0.5)]

        advection_x[i] = x_advection
        advection_y[i] = y_advection

    print(count, advection_x, advection_y, x_vortices, y_vortices)
    # Update vortex positions
    np.add(x_vortices, advection_x * dt, out=x_vortices, casting="unsafe")
    np.add(y_vortices, advection_y * dt, out=y_vortices, casting="unsafe")

    # Recalculate velocity field
    x_velocity = np.zeros_like(X)
    y_velocity = np.zeros_like(Y)
    x_velocity, y_velocity = velocity_field(x_vortices, y_vortices, k_vortices, X, Y, mask_radius, x_velocity, y_velocity)

    ## Plot the velocity field
    # Clear the previous plot
    ax.clear()
    
    ax.streamplot(X, Y, x_velocity, y_velocity, density=[1, 1])
    p, = ax.plot(x_vortices, y_vortices, 'k+', markersize=10, markeredgewidth=2)

    fig.savefig('vortex_{:03d}.png'.format(count))

    # print(x_vortices, y_vortices)

    count += 1


    