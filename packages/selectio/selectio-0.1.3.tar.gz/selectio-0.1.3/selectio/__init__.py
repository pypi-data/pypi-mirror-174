"""
Multi-model Feature Importance Scoring and auto Feature Selection.
------------------------------------------------------------------- 

This Python package returns multiple feature importance scores, feature ranks,
and automatically suggests a feature selection based on the majority vote of all models.

Currently the following six models for feature importance scoring are included:
- Spearman rank analysis (see 'models.spearman')
- Correlation coefficient significance of linear/log-scaled Bayesian Linear Regression (see 'models.blr')
- Random Forest Permutation test (see 'models.rf.py')
- Random Decision Trees on various subsamples of data (see 'models.rdt.py')
- Mutual Information Regression (see 'models.mi')
- General correlation coefficients (see 'models.xicor')

The feature selection score can be either computed directly using the class Fsel, or can be called directly 
with more functionality using a settings yaml file:

python selectio.py -s fname_settings

User settings such as input/output paths and all other options are set in the settings file 
(Default filename: settings_featureimportance.yaml) 
Alternatively, the settings file can be specified as a command line argument with: 
'-s', or '--settings' followed by PATH-TO-FILE/FILENAME.yaml 
(e.g. python selectio.py -s settings/settings_featureimportance.yaml).

For more details see: https://github.com/sebhaan/selectio
"""

__version__ = "0.1.3"
__title__ = "Selectio: Multi-model Feature Importance Scoring and Auto Feature Selection"
__description__ = """
This Python package provides computation of multiple feature importance scores, feature ranks,
and automatically suggests a feature selection based on the majority vote of all models.
"""
__uri__ = "https://github.com/sebhaan/selectio"
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Sebastian Haan"

__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022 Sebastian Haan"