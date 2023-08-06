# Generate simulated data

import os
import numpy as np
import pandas as pd
import itertools
from sklearn.datasets import make_regression
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def create_simulated_features(n_features, outpath = None, n_samples = 200, model_order = 'quadratic', correlated = False, noise= 0.1):
	"""
	Generate synthetic datasets for testing

	Input:
		n_features: number of features
		outpath: path to save simulated data
		n_samples: number of samples	
		model_order: order of the model, either 'linear', 'quadratic', or 'cubic'
		correlated: if True, the features are correlated
		noise: noise level [range: 0-1]

	Return:
		dfsim: dataframe with simulated features
		coefsim: simulated coefficients
		feature_names: list of feature names
	"""
	if correlated:
		n_rank = int(n_features/2)
	else:
		n_rank = None
	Xsim, ysim, coefsim = make_regression(n_samples=n_samples, n_features = n_features, n_informative=int(n_features/2), n_targets=1, 
		bias=0.5, noise=noise, shuffle=False, coef=True, random_state=42, effective_rank = n_rank)	
	feature_names = ["Feature_" + str(i+1) for i in range(n_features)]
	coefsim /= 100
	scaler = MinMaxScaler()
	scaler.fit(Xsim)
	Xsim = scaler.transform(Xsim)
	#plot_feature_correlation(Xsim, feature_names)
	# make first-order model
	if model_order == 'linear':
		ysim_new = np.dot(Xsim, coefsim) + np.random.normal(scale=noise, size = n_samples)
	elif model_order == 'quadratic':
		# make quadratic model
		Xcomb = []
		for i, j in itertools.combinations(Xsim.T, 2):
			Xcomb.append(i * j) 
		Xcomb = np.asarray(Xcomb).T
		Xcomb = np.hstack((Xsim, Xcomb, Xsim**2))
		coefcomb = []
		for i, j in itertools.combinations(coefsim, 2):
			coefcomb.append(i * j) 
		coefcomb = np.asarray(coefcomb)
		coefcomb = np.hstack((coefsim, coefcomb, coefsim**2))
		ysim_new = np.dot(Xcomb, coefcomb) + np.random.normal(scale=noise, size = n_samples)
	elif model_order == 'quadratic_pairwise':
		# make quadratic model
		Xcomb = []
		for i, j in itertools.combinations(Xsim.T, 2):
			Xcomb.append(i * j) 
		Xcomb = np.asarray(Xcomb).T
		Xcomb = np.hstack((Xsim, Xcomb))
		coefcomb = []
		for i, j in itertools.combinations(coefsim, 2):
			coefcomb.append(i * j) 
		coefcomb = np.asarray(coefcomb)
		coefcomb = np.hstack((coefsim, coefcomb))
		ysim_new = np.dot(Xcomb, coefcomb) + np.random.normal(scale=noise, size = n_samples)
	#Save data as dataframe and coefficients on file
	header = np.hstack((feature_names, 'Ytarget'))
	data = np.hstack((Xsim, ysim_new.reshape(-1,1)))
	df = pd.DataFrame(data, columns = header)
	if outpath is not None:
		os.makedirs(outpath, exist_ok=True)
		df.to_csv(os.path.join(outpath, f'SyntheticData_{model_order}_{n_features}nfeatures_{noise}noise.csv'), index = False)
		df_coef = pd.DataFrame(coefsim.reshape(-1,1).T, columns = feature_names)
		df_coef.to_csv(os.path.join(outpath, f'SyntheticData_coefficients_{model_order}_{n_features}nfeatures_{noise}noise.csv'), index = False)
	return df, coefsim, feature_names