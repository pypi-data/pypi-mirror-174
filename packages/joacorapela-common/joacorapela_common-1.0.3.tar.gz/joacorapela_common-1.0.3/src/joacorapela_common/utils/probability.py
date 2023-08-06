
import numpy as np
import scipy.stats
from . import geometry


def quantileEllipse(mean, cov, quantile=.95, N=100):
    """Answers an ellipse that contains *quantile* percent of points drawn from a
    2D Gaussian distribution with mean *mean* and covariance *cov*.
    https://www.visiondummy.com/2014/04/draw-error-ellipse-representing-covariance-matrix/

    param mean: mean of a 2D Gaussian distribution
    type mean: list-like of length 2
    param cov: covariance of a 2D Gaussian distribution
    type cov: numpy matrix of size (2, 2)
    param quantile: percentage of points drawn from the Gaussian distribution
    that should lie inside the answered ellipse
    """
    quantile_value = scipy.stats.chi2.ppf(q=quantile, df=2)
    # eig_vec, eig_val, _ = np.linalg.svd(cov)
    eig_val, eig_vec = np.linalg.eig(cov)
    # begin orthogonlize
    # first orthogonalize
    eig_vec[:, 1] = eig_vec[:, 1] - \
        np.dot(eig_vec[:, 0], eig_vec[:, 1]) * eig_vec[:, 0]
    # next set norm 1
    eig_vec[:, 1] = eig_vec[:, 1] / np.linalg.norm(eig_vec[:, 1])
    # end orthogonlize
    x, y = geometry.ellipsePoints(x_center=mean[0], y_center=mean[1],
                                  ax1=eig_vec[:, 0], ax2=eig_vec[:, 1],
                                  a=np.sqrt(eig_val[0]*quantile_value),
                                  b=np.sqrt(eig_val[1]*quantile_value),
                                  N=N)
    return x, y
