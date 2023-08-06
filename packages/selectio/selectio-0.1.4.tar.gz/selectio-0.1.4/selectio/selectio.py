"""
Multi-model Feature Importance Scoring and Auto Feature Selection.
------------------------------------------------------------------- 

This Python package returns multiple feature importance scores, feature ranks,
and automatically suggests a feature selection based on the majority vote of all models.

## Models

Currently the following six models for feature importance scoring are included:
- Spearman rank analysis (see 'models.spearman')
- Correlation coefficient significance of linear/log-scaled Bayesian Linear Regression (see 'models.blr')
- Random Forest Permutation test (see 'models.rf.py')
- Random Decision Trees on various subsamples of data (see 'models.rdt.py')
- Mutual Information Regression (see 'models.mi')
- General correlation coefficients (see 'models.xicor')

Note that the current feature importance models support numerical data only. Categorical data 
will need to be encoded to numerical features.

## Usage

The feature selection score can be either computed directly using selectio.Fsel(X,y), or can be computed 
with more functionality (including preprocessing and plotting) using a settings yaml file:
python selectio.py -s fname_settings

User settings such as input/output paths and all other options are set in the settings file 
(Default filename: settings_featureimportance.yaml) 
Alternatively, the settings file can be specified as a command line argument with: 
'-s', or '--settings' followed by PATH-TO-FILE/FILENAME.yaml 
(e.g. python selectio.py -s settings/settings_featureimportance.yaml).

For a more detailed example how to use selectio please check the notebooks.
"""

import os
import sys
import yaml
import shutil
import argparse
import datetime
from types import SimpleNamespace  
import numpy as np
import pandas as pd
import importlib
import pkg_resources
import matplotlib.pyplot as plt

# import some custom plotting utility functions
from .utils import plot_correlationbar, plot_feature_correlation_spearman, gradientbars

# import all models for feature importance calculation
from .models import __all__ as _modelnames
_list_models = []
for modelname in _modelnames:
	module = importlib.import_module('.models.'+modelname, package='selectio')
	_list_models.append(module)

# Settings for default yaml filename
_fname_settings = pkg_resources.resource_filename('selectio', 'settings/settings_featureimportance.yaml')


class Fsel:
	"""
	Auto Feature Selection

	Input:
		X: array with shape (nsample, nfeatures)
		y: vector with shape (nsample,)
	"""
	def __init__(self, X, y):
		
		self.X = X
		self.y = y

		self.nmodels = len(_modelnames)
		self.nfeatures = X.shape[1]

		# Initialise pandas dataframe to save results
		self.dfmodels = pd.DataFrame(columns=['score_' + modelname for modelname in _modelnames])


	def score_models(self):
		"""
		Calculate feature importance for all models and select features

		Return:
			dfmodels: pandas dataframe with scores for each feature
		"""
		# Loop over all models and calculate normalized feature scores
		count_select = np.zeros(self.nfeatures).astype(int)
		scores_total = np.zeros(self.X.shape[1])
		for i in range(self.nmodels):
			model = _list_models[i]
			modelname = _modelnames[i]
			print(f'Computing scores for model {modelname}...')
			corr = model.factor_importance(self.X, self.y, norm = True)
			self.dfmodels['score_' + modelname] = np.round(corr, 4)
			# Calculate which feature scores accepted
			woe = self.eval_score(corr)
			self.dfmodels['woe_' + modelname] = woe
			count_select += woe
			# Add to total scores
			scores_total += corr * woe
			print(f'Done, {woe.sum()} features selected.')

		# normalize and save combined score
		scores_total /= np.sum(scores_total)
		self.dfmodels['score_combined'] = np.round(scores_total,4)
		
		# Select features based on majority vote from all models:
		select = np.zeros(self.nfeatures).astype(int)
		select[count_select >= round(self.nmodels/2)] = 1
		self.dfmodels['selected'] = select
		
		return self.dfmodels


	def eval_score(self, score, woe_min = 0.01):
		"""
		Evaluate multi-model feature importance scores and select features based on majority vote

		Input:
			score: 1dim array with scores
			woe_min: minimum fractional contribution to total score (default = 0.01)
		Return:
			woe: array of acceptance (1 = accepted, 0 = not)
		""" 
		sum_score = score.sum()
		min_score = sum_score * woe_min
		woe = np.zeros_like(score)
		woe[score >= min_score] = 1
		return woe.astype(int)


def plot_allscores(dfscores, feature_names, outpath, show = False):
	"""
	Generates overview plot of all scores and saves in output path

	Input:
		dfscores: pandas dataframe with score results
		feature_names: list of fetaure names, must match order in dfscores
		outpath: output directory
		show: boolean, if True shows matplotlib plot
	"""
	
	fig, ax = plt.subplots(3,2, figsize = (10,8))
	j =0 
	for i in range(6):
		modelname = _modelnames[i]
		model_fullname = _list_models[i].__fullname__
		scores = dfscores['score_' + modelname].values
		sorted_idx = scores.argsort()
		ypos = np.arange(len(scores))
		if i >= 3:
			i -= 3
			j = 1
		bar = ax[i, j].barh(ypos, scores[sorted_idx], tick_label = np.asarray(feature_names)[sorted_idx], align='center')
		gradientbars(bar, scores[sorted_idx])
		ax[i, j].set_title(f'{model_fullname}')	
	ax[2, 0].set_xlabel('Feature Importance Score')	
	ax[2, 1].set_xlabel('Feature Importance Score')
	plt.tight_layout()
	fname_out = f'Models-feature-importances.png'
	plt.tight_layout()
	plt.savefig(os.path.join(outpath, fname_out), dpi = 300)
	if show:
		plt.show()
	plt.close('all')


def main(fname_settings):
	"""
	Main function for running selectio.

	Generating feature importance scores and selection. 
	Results are saved as csv file and scores are plotted as png.

	See settings file for input and output.

	Input:
		fname_settings: path and filename to yaml settings file (see examples)
	"""
	# Load settings from yaml file
	with open(fname_settings, 'r') as f:
		settings = yaml.load(f, Loader=yaml.FullLoader)
	# Parse settings dictinary as namespace (settings are available as 
	# settings.variable_name rather than settings['variable_name'])
	settings = SimpleNamespace(**settings)

	# Verify output directory and make it if it does not exist
	os.makedirs(settings.outpath, exist_ok = True)

	# Read data
	data_fieldnames = settings.name_features + [settings.name_target]
	df = pd.read_csv(os.path.join(settings.inpath, settings.infname), usecols=data_fieldnames)

	# Verify that data is cleaned:
	assert df.select_dtypes(include=['number']).columns.tolist().sort() == data_fieldnames.sort(), 'Data contains non-numeric entries.'
	assert df.isnull().sum().sum() == 0, "Data is not cleaned, please run preprocess_data.py before"

	# Generate Spearman correlation matrix for X
	print("Calculate Spearman correlation matrix...")
	plot_feature_correlation_spearman(df[data_fieldnames].values, data_fieldnames, settings.outpath, show = False)

	X = df[settings.name_features].values
	y = df[settings.name_target].values

	# Generate feature importance scores
	fsel = Fsel(X,y)
	dfres = fsel.score_models()

	dfres.insert(loc = 0, column = 'name_features', value = settings.name_features)

	print('Feature selection: ')
	dfselect = dfres.loc[dfres.selected == 1, ['name_features', 'score_combined']]
	print(dfselect.sort_values('score_combined', ascending=False))
	
	# Save results as csv
	dfres.to_csv(os.path.join(settings.outpath, 'feature-importance_scores.csv'), index_label = 'Feature_index')

	# Plot scores
	print("Generating score plots ...")
	plot_allscores(dfres, settings.name_features, settings.outpath)

	# Plot combined score
	plot_correlationbar(dfres['score_combined'].values, settings.name_features, settings.outpath, 'Combined-feature-importance.png', name_method = 'Combined Model Score', show = False)
	print('COMPLETED.')


if __name__ == '__main__':
	# Parse command line arguments
	parser = argparse.ArgumentParser(description='Calculating feature importance.')
	parser.add_argument('-s', '--settings', type=str, required=False,
						help='Path and filename of settings file.',
						default = _fname_settings)
	args = parser.parse_args()

	# Log computational time
	#datetime_now = datetime.datetime.now()

	# Run main function
	main(args.settings)

	# print out compute time of main function in seconds
	#print('Total computational time: {:.2f} seconds'.format((datetime.datetime.now() - datetime_now).total_seconds()))