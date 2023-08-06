# Custom utility functions for visualisation and modeling

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from scipy.cluster import hierarchy


def gradientbars(bars, data):
	"""
	Helper function for making colorfull bars

	Input:
		bars: list of bars
		data: data to be plotted
	"""
	ax = bars[0].axes
	lim = ax.get_xlim()+ax.get_ylim()
	ax.axis(lim)
	for bar in bars:
		bar.set_zorder(1)
		bar.set_facecolor("none")
		x,y = bar.get_xy()
		w, h = bar.get_width(), bar.get_height()
		grad = np.atleast_2d(np.linspace(0,1*w/max(data),256))
		ax.imshow(grad, extent=[x,x+w,y,y+h], aspect="auto", zorder=0, norm=mpl.colors.NoNorm(vmin=0,vmax=1))
	ax.axis(lim)


def plot_correlationbar(corrcoefs, feature_names, outpath, fname_out, name_method = None, show = False):
	"""
	Helper function for plotting feature correlation.
	Result plot is saved in specified directory.

	Input:
		corrcoefs: list of feature correlations
		feature_names: list of feature names
		outpath: path to save plot
		fname_out: name of output file (should end with .png)
		name_method: name of method used to compute correlations
		show: if True, show plot
	"""
	sorted_idx = corrcoefs.argsort()
	fig, ax = plt.subplots(figsize = (6,5))
	ypos = np.arange(len(corrcoefs))
	bar = ax.barh(ypos, corrcoefs[sorted_idx], tick_label = np.asarray(feature_names)[sorted_idx], align='center')
	gradientbars(bar, corrcoefs[sorted_idx])
	if name_method is not None:	
		plt.title(f'{name_method}')	
	plt.xlabel("Feature Importance")
	plt.tight_layout()
	plt.savefig(os.path.join(outpath, fname_out), dpi = 200)
	if show:
		plt.show()
	plt.close('all')


def plot_feature_correlation_spearman(X, feature_names, outpath, show = False):
	"""
	Plot feature correlations using Spearman correlation coefficients.
	Feature correlations are automatically clustered using hierarchical clustering.

	Result figure is automatically saved in specified path.

	Input:
		X: data array
		feature names: list of feature names
		outpath: path to save plot
		show: if True, interactive matplotlib plot is shown
	"""
	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))
	corr = spearmanr(X).correlation
	corr_linkage = hierarchy.ward(corr)
	dendro = hierarchy.dendrogram(corr_linkage, labels=feature_names, ax=ax1, leaf_rotation=90)
	dendro_idx = np.arange(0, len(dendro['ivl']))

	# Plot results:
	pos = ax2.imshow(corr[dendro['leaves'], :][:, dendro['leaves']])
	ax2.set_xticks(dendro_idx)
	ax2.set_yticks(dendro_idx)
	ax2.set_xticklabels(dendro['ivl'], rotation='vertical')
	ax2.set_yticklabels(dendro['ivl'])
	fig.colorbar(pos, ax = ax2)
	fig.tight_layout()
	plt.savefig(os.path.join(outpath, 'Feature_Correlations_Hierarchical_Spearman.png'), dpi = 300)
	if show:
		plt.show()


