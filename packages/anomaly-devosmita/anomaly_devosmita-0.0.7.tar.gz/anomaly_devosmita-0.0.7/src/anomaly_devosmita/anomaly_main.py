#%%
from . import anomaly_detection as ad
from . import anomaly_models as am
from . import anomaly_libs as al

#%%
id_column = 'spare_part_id'

def anomaly_app(data_set, id_column, analysis="univariate", models=["full"]):

    test_phase, voters_list, full_df_result, ax, am, sum_votes = ad.anomaly_detector(ad.data_set, id_column)
    # no return but save of DF as file and performance of selected models over the given dataset
    ## Need to add metrics for perormance measurment so that we can display the list of models and their performance
# %%
results = anomaly_app(ad.data_set, id_column)
# %%
