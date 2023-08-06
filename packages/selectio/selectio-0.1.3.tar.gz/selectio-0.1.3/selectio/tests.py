# Test functions

import os 
import yaml
import shutil
import numpy as np
import importlib
import pkg_resources

from .simdata import create_simulated_features
from .utils import plot_correlationbar

from selectio import selectio

# import all models for feature importance calculation
from .models import __all__ as _modelnames
_list_models = []
for modelname in _modelnames:
	module = importlib.import_module('.models.'+modelname, package='selectio')
	_list_models.append(module)

_fname_settings = pkg_resources.resource_filename('selectio', 'settings/settings_featureimportance.yaml')


### Test Models ####

def test_rf_factor_importance():
    """
    Test function for feature importance using random forest 
    """
    from .models import rf
    dfsim, coefsim, feature_names = create_simulated_features(6, model_order = 'quadratic', noise = 0.05)
    X = dfsim[feature_names].values
    y = dfsim['Ytarget'].values
    imp_mean_corr = rf.factor_importance(X, y)
    assert np.argmax(coefsim) == np.argmax(imp_mean_corr)


def test_blr_factor_importance():
    """
    Test function for bayesian log-power regression model
    """
    from .models import blr
    dfsim, coefsim, feature_names = create_simulated_features(6, model_order = 'linear', noise = 0.05)
    X = dfsim[feature_names].values
    y = dfsim['Ytarget'].values
    coef_signif = blr.factor_importance(X, y)
    assert np.argmax(coefsim) == np.argmax(coef_signif)


def test_xicor_factor_importance():
    """
    Test function for generalised model
    """
    from .models import xicor
    dfsim, coefsim, feature_names = create_simulated_features(6, n_samples = 200, model_order = 'quadratic', noise = 0.05)
    X = dfsim[feature_names].values
    y = dfsim['Ytarget'].values
    corr = xicor.factor_importance(X, y)
    assert np.argmax(coefsim) == np.argmax(corr)


def test_rdt_factor_importance():
    """
    Test function for randomized decision trees (RDT)
    """
    from .models import rdt
    dfsim, coefsim, feature_names = create_simulated_features(6, n_samples = 200, model_order = 'quadratic', noise = 0.05)
    X = dfsim[feature_names].values
    y = dfsim['Ytarget'].values
    corr = rdt.factor_importance(X, y)
    assert np.argmax(coefsim) == np.argmax(corr)


def test_mi_factor_importance():
    """
    Test function for mutual information model
    """
    from .models import mi
    dfsim, coefsim, feature_names = create_simulated_features(6, n_samples = 200, model_order = 'quadratic', noise = 0.05)
    X = dfsim[feature_names].values
    y = dfsim['Ytarget'].values
    corr = mi.factor_importance(X, y)
    assert np.argmax(coefsim) == np.argmax(corr)


def test_spearman_factor_importance():
    """
    Test function for Spearman Rank analysis
    """
    from .models import spearman
    dfsim, coefsim, feature_names = create_simulated_features(6, n_samples = 200, model_order = 'quadratic', noise = 0.05)
    X = dfsim[feature_names].values
    y = dfsim['Ytarget'].values
    corr = spearman.factor_importance(X, y)
    assert np.argmax(coefsim) == np.argmax(corr)



def test_select():
    """
    Test function for selectio.select.

    This test automatically generates synthetic data and generates feature importance plots
    in the subfolder `test_featureimportance`.
    """
    # Make temporary result folder
    outpath = 'test_featureimportance'
    os.makedirs(outpath, exist_ok = True)

    # Generate simulated data
    print("Generate simulated data...")
    dfsim, coefsim, feature_names_sim = create_simulated_features(8, outpath = outpath)
    print(f'True coefficients of simulated data are: {np.round(coefsim,4)}')

    # Generate settings file for simulated data
    # (Note: you could also just simply set settings variables here, but this is also testing the settings file readout)
    fname_settings_sim = 'settings_featureimportance_simulation.yaml'
    shutil.copyfile(_fname_settings, os.path.join(outpath, fname_settings_sim))
    # Change yaml file to simulation specifications:
    with open(os.path.join(outpath, fname_settings_sim), 'r') as f:
        settings_sim = yaml.load(f, Loader=yaml.FullLoader)
    settings_sim['name_features'] = feature_names_sim
    settings_sim['name_target'] = 'Ytarget'
    settings_sim['infname'] = 'SyntheticData_quadratic_8nfeatures_0.1noise.csv'
    settings_sim['inpath'] = outpath
    settings_sim['outpath'] = outpath
    with open(os.path.join(outpath, fname_settings_sim), 'w') as f:
        yaml.dump(settings_sim, f)

    # Run main function
    selectio.main(os.path.join(outpath, fname_settings_sim))

    for i in range(len(_modelnames)):
        modelname = _modelnames[i]
        try:
            model_label = _list_models[i].__name__
            model_fullname = _list_models[i].__fullname__
        except:
            model_label = modelname
            model_fullname = modelname
        assert os.path.isfile(os.path.join(outpath, f'{model_label}-feature-importance.png')), f'Plot for {model_fullname} not generated.'
    assert os.path.isfile(os.path.join(outpath, 'Combined-feature-importance.png')), 'Plot for combined feature importance not generated.'

    # Remove temporary result folder
    # shutil.rmtree(outpath)

    print('Test completed ok.')


### Other test functions ### 

def test_plot_correlationbar(outpath):
    """
    Test function for plot_correlationbar
    """
    dfsim, coefsim, feature_names = create_simulated_features(6, model_order = 'quadratic', noise = 0.05)
    plot_correlationbar(coefsim, feature_names, outpath, 'test_plot_correlationbar.png', show = True)