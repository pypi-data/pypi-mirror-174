"""
Factor importance using Random Forest (RF) permutation test
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from scipy.stats import spearmanr
import multiprocessing

__name__ = 'RF'
__fullname__ = 'Random Forest Permutation' 


def set_njobs():
	"""
	Set optimal number of parallel jobs. 
	Here: N_Jobs = N_CPU - 1
	"""
	ncpu = multiprocessing.cpu_count()
	if ncpu > 1:
		njobs = ncpu - 1
	else:
		njobs = 1
	return njobs



def factor_importance(X_train, y_train, norm = True, max_samples = 5000):
	"""
	Factor importance using RF permutation test and optional corrections 
	for multi-collinarity (correlated) features. 
	Including training of Random Forest regression model with training data 
	and setting non-significant coefficients to zero.

	Note that for large datasets, it is recommended to set max_samples. 
	This option may provide less accurate importance estimates, but
    it keeps the method tractable.

	Input:
		X: input data matrix with shape (npoints,nfeatures)
		y: target varable with shape (npoints)
		norm: boolean, if True (default) normalize correlation coefficients to sum = 1
		max_samples: The maximum number of samples to draw from X in each repeat (without replacement)

	Return:
		imp_mean_corr: feature importances
	"""

	n_jobs = set_njobs()
	if len(y_train) < max_samples:
		max_samples = 1.0
	
	rf_reg = RandomForestRegressor(n_estimators=500, min_samples_leaf=4, random_state = 42)
	rf_reg.fit(X_train, y_train)
	
	result = permutation_importance(
		rf_reg, 
		X_train, 
		y_train, 
		n_repeats=20, 
		random_state=42, 
		n_jobs=n_jobs, 
		scoring = "neg_mean_squared_error", 
		max_samples = max_samples)

	imp_mean_corr = result.importances_mean
	imp_std_corr = result.importances_std

	# Set non significant features to zero:
	imp_mean_corr[imp_mean_corr / imp_std_corr < 3] = 0
	imp_mean_corr[imp_mean_corr < 0.001] = 0
	if norm:
		imp_mean_corr /= np.sum(imp_mean_corr)
	return imp_mean_corr