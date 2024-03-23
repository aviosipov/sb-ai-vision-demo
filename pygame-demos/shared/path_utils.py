# shared/path_utils.py
import numpy as np
from scipy.interpolate import splprep, splev

def create_smooth_path(path):
    if len(path) > 2:  # We need at least 3 points to create a smooth spline
        tck, u = splprep(path.T, u=None, s=0.0)  # You may adjust the s parameter for smoothing
        u_new = np.linspace(u.min(), u.max(), 1000)
        x_new, y_new = splev(u_new, tck, der=0)
        smooth_path = np.vstack((x_new, y_new)).T
        return smooth_path
    else:
        return path