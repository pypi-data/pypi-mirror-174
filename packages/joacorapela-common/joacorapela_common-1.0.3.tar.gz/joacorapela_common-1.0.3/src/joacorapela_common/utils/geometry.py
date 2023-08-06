
import numpy as np


def ellipsePoints(x_center=0, y_center=0, ax1=[1, 0],  ax2=[0, 1], a=1, b=1,
                  N=100, tol=1e-6):
    """ returns N points (x, y) of the ellipse centered at (x_center, y_center)
    aligned along axes ax1 and ax2, a and b being the half length along axes
    ax1, and ax2, respectively.
    https://stackoverflow.com/questions/69109513/how-to-draw-an-ellipsoid-using-tilted-or-rotated-lines-using-plotly

    :param x_center: absissa of the ellipsoid center
    :type x_center: float
    :param y_center: ordenate of the ellipsoid center
    :type y_center: float
    :param ax1, param_ax_2: orthonormal vector representing the ellipse axis
    :type param_ax1: pair of floats
    :type param_ax2: pair of floats
    :param a, b: lengths of ax1 and ax2, respectively
    :type a: float
    :type b: float
    :param N: number of points to return.
    """
    if(np.abs(np.linalg.norm(ax1)-1.0) > tol or
       np.abs(np.linalg.norm(ax2)-1.0) > tol):
        raise ValueError('ax1, ax2 must be unit vectors')
    if(abs(np.dot(ax1, ax2)) > tol):
        raise ValueError('ax1, ax2 must be orthogonal vectors')
    # rotation matrix
    R = np.array([ax1, ax2]).T
    if np.linalg.det(R) < 0:
        R = np.array([-ax1, ax2]).T
        # raise ValueError("the det(R) must be positive to get a  positively oriented ellipse reference frame")
    t = np.linspace(0, 2*np.pi, N)
    # ellipse parameterization with respect to a system of axes of directions
    # a1, a2
    xs = a * np.cos(t)
    ys = b * np.sin(t)

    # coordinate of the  ellipse points with respect to the system of axes
    # [1, 0], [0,1] with origin (0,0)
    xp, yp = np.dot(R, [xs, ys])
    x = xp + x_center
    y = yp + y_center
    return x, y
