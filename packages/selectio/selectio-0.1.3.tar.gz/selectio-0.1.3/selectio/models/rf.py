"""
Factor importance using Random Forest (RF) permutation test
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from scipy.stats import spearmanr

__name__ = 'RF'
__fullname__ = 'Random Forest Permutation' 

def factor_importance(X_train, y_train, correlated = False, norm = True):
	"""
	Factor importance using RF permutation test and optional corrections 
	for multi-collinarity (correlated) features. 
	Including training of Random Forest regression model with training data 
	and setting non-significant coefficients to zero.

	Input:
		X: input data matrix with shape (npoints,nfeatures)
		y: target varable with shape (npoints)
		correlated: if True, features are assumed to be correlated
		norm: boolean, if True (default) normalize correlation coefficients to sum = 1

	Return:
		imp_mean_corr: feature importances
	"""
	rf_reg = RandomForestRegressor(n_estimators=500, min_samples_leaf=4, random_state = 42)
	rf_reg.fit(X_train, y_train)
	result = permutation_importance(rf_reg, X_train, y_train, n_repeats=20, random_state=42, 
		n_jobs=1, scoring = "neg_mean_squared_error")
	imp_mean = result.importances_mean
	imp_std = result.importances_std
	# Make corrections for correlated features
	# This is necessary since permutation importance are lower for correlated features
	if correlated:
		corr = spearmanr(X_train).correlation
		imp_mean_corr = np.zeros(len(imp_mean))
		imp_std_corr = np.zeros(len(imp_mean))
		for i in range(len(imp_mean)):
			imp_mean_corr[i] = np.sum(abs(corr[i]) * imp_mean)
			imp_std_corr[i] = np.sqrt(np.sum(abs(corr[i]) * imp_std**2))
	else:
		imp_mean_corr = imp_mean
		imp_std_corr = imp_std
	#print("Random Forest factor importances: ", imp_mean_corr)
	#print("Random Forest factor importances std: ", imp_std_corr)
	# Set non significant features to zero:
	imp_mean_corr[imp_mean_corr / imp_std_corr < 3] = 0
	imp_mean_corr[imp_mean_corr < 0.001] = 0
	if norm:
		imp_mean_corr /= np.sum(imp_mean_corr)
	return imp_mean_corr