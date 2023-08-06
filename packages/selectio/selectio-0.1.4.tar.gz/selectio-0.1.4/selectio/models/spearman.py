"""
Spearman rank-order correlation analysis for feature importance

Limitations: assumes monotonic functions and no interaction terms.
"""

import numpy as np
from scipy.stats import spearmanr

__name__ = 'Spearman'
__fullname__ = 'Spearman Rank-Order'

def factor_importance(X_train, y_train, norm = True):
	"""
	Spearman rank-order analysis

	Input:
		X: input data matrix with shape (npoints, nfeatures)
		y: target varable with shape (npoints)
		norm: boolean, if True (default) normalize correlation coefficients to sum = 1

	Return:
		result: feature correlations
	"""
	nfeatures = X_train.shape[1]
	corr = np.zeros(nfeatures)
	for i in range(nfeatures):
		sr = spearmanr(X_train[:,i], y_train)
		if sr.pvalue < 0.01:
			corr[i] = abs(sr.correlation)
	if norm:
		corr /= np.sum(corr)
	return corr