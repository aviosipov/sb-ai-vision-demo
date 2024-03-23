# shared/path_utils.py
import numpy as np
from scipy.interpolate import splprep, splev

def create_smooth_path(path):
    if len(path) > 3:  # We need at least 4 points to create a cubic spline
        tck, u = splprep(path.T, u=None, s=0.0, k=3)  # Use cubic spline (k=3)
        u_new = np.linspace(u.min(), u.max(), 1000)
        x_new, y_new = splev(u_new, tck, der=0)
        smooth_path = np.vstack((x_new, y_new)).T
        return smooth_path
    elif len(path) == 3:  # For 3 points, use quadratic spline (k=2)
        tck, u = splprep(path.T, u=None, s=0.0, k=2)
        u_new = np.linspace(u.min(), u.max(), 1000)
        x_new, y_new = splev(u_new, tck, der=0)
        smooth_path = np.vstack((x_new, y_new)).T
        return smooth_path
    else:
        return path