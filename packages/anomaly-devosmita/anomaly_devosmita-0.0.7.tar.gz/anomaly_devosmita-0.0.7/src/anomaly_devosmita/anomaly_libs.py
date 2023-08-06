# %%
# Default libs
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Detrend & deseason
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import signal
from statsmodels.tsa.stattools import adfuller
from statsmodels.formula.api import ols

# ML models
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from ThymeBoost import ThymeBoost as tb
# %%
