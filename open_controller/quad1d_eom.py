import numpy as np
import matplotlib.pyplot as plt
from open_controller import Open_Controller

def ydot(y, t, controller):
    # Returns the state vector at the next time-step
    
    # Parameters:
    # -----------
    # y(k) = state vector, a length 2 list
    #      = [altitude, speed]
    # t = time, (sec)
    # pid = instance of the PIDController class

    # Returns:
    # --------
    # y(k+1) = [y[0], y[1]] = y(k) + ydot*dt

    # Model state
    y0 = y[0]   # altitude, m
    y1 = y[1]   # speed, m/s

    # Model parameters
    g = -9.81   # gravity, m/s^2
    m = 1.54    # quadrotor mass, kg
    c = 10.0    # electro-mechanical transmission constant

    # time step, sec
    dt = t - controller.last_timestamp_
    # Control effort
    u = controller.getControlEffort(t)

    ### State derivatives
    if (y0 <= 0.):
        # if control input, u <= gravity, vehicle stays at rest on the ground
        # this prevents quadrotor from "falling" through the ground when thrust
        # is too small
        if u <= np.absolute(g*m/c):
            y0dot = 0.
            y1dot = 0.
        else:   # else if u > gravity and quadrotor accelerates upward
            y0dot = y1
            y1dot = g + c/m*u - 0.75*y1
    else:   # otherwise quadrotor is already in the air
        y0dot = y1
        y1dot = g + c/m*u - 0.75*y1

    y0 += y0dot*dt
    y1 += y1dot*dt
    return [y0, y1]
