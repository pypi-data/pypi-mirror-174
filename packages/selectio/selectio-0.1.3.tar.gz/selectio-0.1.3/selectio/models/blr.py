"""
Bayesian Linear Regression model
 
Returns the estimated significance of regression coefficients.

The significance of the linear coefficient is defined by dividing the estimated coefficient 
over the standard deviation of this estimate. The correlation significance is set to zero if below threshold.
"""

import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import BayesianRidge

__name__ = 'BLR'
__fullname__ = 'Bayesian Log-Linear Regression'


def factor_importance(X, y, logspace = True, signif_threshold = 2, norm = True):
	"""
	Trains Bayesian Linear/Log Regression model and returns the estimated significance of regression coefficients.
	The significance of the linear coefficient is defined by dividing the estimated coefficient 
	over the standard deviation of this estimate. The correlation significance is set to zero if below threshold.

	Input:
		X: input data matrix with shape (npoints,nfeatures)
		y: target varable with shape (npoints)
		logspace: if True (default), models regression in logspace
		signif_threshold: threshold for coefficient significance to be considered significant (Default = 2)
		norm: boolean, if True (default) normalize correlation coefficients to sum = 1

	Return:
		coef_signif: Significance of coefficients (Correlation coefficient / Stddev)
	"""
	# Scale data using RobustScaler:
	if X.shape[1] == 1:
		X = x.reshape(-1,1)
	scaler = RobustScaler(unit_variance = True)
	X = scaler.fit_transform(X)
	y = scaler.fit_transform(y.reshape(-1,1)).ravel()
	if logspace:
		X = np.log(X - X.min(axis = 0) + 1)
		y = np.log(y - y.min() + 1)	

	y = y.reshape(-1,1).ravel()

	# Apply Bayesian Linear Regression:
	reg = BayesianRidge(tol=1e-6, fit_intercept=True, compute_score=True)
	reg.fit(X, y)

	# Set none significant coefficients to zero
	coef = reg.coef_.copy()
    
	# reg.sigma_ is the estimated variance-covariance matrix of the weights,
	# to calculate standard deviation of coeffcients:
	coef_std = np.sqrt(np.diag(reg.sigma_)).copy()
	coef_signif = coef / coef_std
	#for i in range(len(coef)):
	#	print('X' + str(i), ' wcorr=' + str(np.round(coef[i], 3)) + ' +/- ' + str(np.round(coef_sigma[i], 3)))
	# Set not significant coefficients to zero:
	coef_signif[coef_signif < signif_threshold] = 0
	# Normalize:
	if norm:
		coef_signif /= np.sum(coef_signif)
	return coef_signif