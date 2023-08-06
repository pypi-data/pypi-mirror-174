"""
Factor importance using randomized decision trees (a.k.a. extra-trees)
on various sub-samples of the dataset
"""

import numpy as np
from sklearn.ensemble import ExtraTreesRegressor

__name__ = 'RDT'
__fullname__ = 'Randomized Decision Trees'


def factor_importance(X_train, y_train, norm = True):
    """
    Factor importance using randomized decision trees (a.k.a. extra-trees)
    on various sub-samples of the dataset

    Input:
        X: input data matrix with shape (npoints,nfeatures)
        y: target varable with shape (npoints)
        norm: boolean, if True (default) normalize correlation coefficients to sum = 1

    Return:
        result: feature importances
    """
    model = ExtraTreesRegressor(n_estimators=500, random_state = 42)
    model.fit(X_train, y_train)
    result = model.feature_importances_
    result[result < 0.001] = 0
    if norm:
        result /= np.sum(result)
    return result