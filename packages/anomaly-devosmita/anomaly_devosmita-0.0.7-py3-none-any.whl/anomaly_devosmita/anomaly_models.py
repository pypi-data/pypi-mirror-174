#%%
from . import anomaly_libs as al

# %% Isolation Forest
def fit_iforest(df, contamination):
    """
    Add your description here
    """
    iso = al.IsolationForest(contamination=contamination)
    iso_pred = iso.fit_predict(df)
    
    return(iso_pred)

# %%
def fit_dbscan(X, eps, min_samples):
    '''
    This function builds the DBSCAN model and returns the labels(clusters) for each row of data.
    It takes as parameters X - which is the data set that should be clustered (labeled)
    eps or epsilor, which is a very critical parameter for the model
    min_samples - The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. This includes the point itself.
    '''
    dbscan_model = al.DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    labels = dbscan_model.labels_

    return(labels)


# %%
def fit_ThymeBoost(X, p):
    """
    Add your description here
    """
    boosted_model = al.tb.ThymeBoost()
    ThymeBoost_model = boosted_model.detect_outliers(X['demand_quantity'],
                                       trend_estimator='linear',
                                       seasonal_estimator='fourier',
                                       seasonal_period=p,
                                       global_cost='maicc',
                                       fit_type='global')
    
    TB_output = ThymeBoost_model[['outliers']]
    TB_output.outliers = TB_output.outliers.replace({True: '-1', False: '1'})
    TB_lables = TB_output['outliers'].tolist()
    
    return(TB_lables)


# %%
# One-Class SVM
ocsvm_kernels = ['linear', 'poly', 'rbf', 'sigmoid']

def fit_oc_svm(X, k):
    """
    Add your description here
    """
    oc_svm_model = al.OneClassSVM(kernel=k)
    labels = oc_svm_model.fit_predict(X)
    
    return(labels)


# %%
# LOF
lof_algs = ['auto', 'ball_tree', 'kd_tree', 'brute']

def fit_lof(X, alg):
    """
    Add your description here
    """
    lof_model = al.LocalOutlierFactor(algorithm=alg)
    lof_pred = lof_model.fit_predict(X)
    
    return lof_pred