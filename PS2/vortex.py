"""




"""
import numpy as np
import matplotlib.pyplot as plt

dt = 0.1
Nsteps = 100

## Set up initial conditions (vortex centres and circulation)
# Vortex rings
y_vortices = np.array([30, -30, 30, -30])
x_vortices = np.array([-30, 30, 30, -30])
k_vortices = np.array([5, 5, 5, 5])

# Setting up the plot
plt.ion()
fig, ax = plt.subplots(1,1)
# mark the initial positions of vortices
p, = ax.plot(x_vortices, y_vortices, 'k+', markersize=10)

# draw the initial velocity streamline
ngrid = 80
Y, X = np.mgrid[-ngrid:ngrid:360j, -ngrid:ngrid:360j]
x_velocity = np.zeros_like(X)
y_velocity = np.zeros_like(Y)

# masking radius for better visualization
mask_radius = 1

# velocity field calculations
def velocity_field(x_vortices, y_vortices, k_vortices, X, Y, mask_radius, x_velocity, y_velocity):
    for i in range(len(x_vortices)):
        ## Compute total velocity field
        # Distance from each grid cell to the vortex
        r = np.sqrt((X - x_vortices[i])**2 + (Y - y_vortices[i])**2)

        # Velocity field of each vortex
        x_velocity += -k_vortices[i] * (Y - y_vortices[i]) / r
        y_velocity += k_vortices[i] * (X - x_vortices[i]) / r
        
        # mask the velocity field with NaNs
        x_velocity[r < mask_radius] = np.nan
        y_velocity[r < mask_radius] = np.nan
    
    return x_velocity, y_velocity

# initial velocity field
x_velocity, y_velocity = velocity_field(x_vortices, y_vortices, k_vortices, X, Y, mask_radius, x_velocity, y_velocity)

print(x_velocity[50, 40])


## Plot the velocity field
# Boundaries
ax.set_xlim(-ngrid, ngrid)
ax.set_ylim(-ngrid, ngrid)

# Initial strewamline
ax.streamplot(X, Y, x_velocity, y_velocity, density=[1, 1])

# Update the plot
fig.canvas.draw()

fig.savefig('vortex_initial.png')
pngrea
## Time evolution
# Initialize counter
count = 0

while count < Nsteps:
    ## Computer and update advection velocity

    # Advection velocity
    advection_x = np.zeros_like(x_vortices)
    advection_y = np.zeros_like(y_vortices)
    for i in range(len(advection_x)):
        advection_x[i] = x_velocity[int(x_vortices[i]), int(y_vortices[i])]
        advection_y[i] = y_velocity[int(x_vortices[i]), int(y_vortices[i])]
        print(advection_x)

    
    print(advection_x)
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
    p, = ax.plot(x_vortices, y_vortices, 'k+', markersize=10)

    fig.savefig('vortex_{:03d}.png'.format(count))

    print(x_vortices, y_vortices)

    count += 1


    