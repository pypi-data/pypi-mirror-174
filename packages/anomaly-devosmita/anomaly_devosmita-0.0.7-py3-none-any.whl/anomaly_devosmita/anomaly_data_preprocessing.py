#%%
from . import anomaly_libs as al
from . import anomaly_detection as ad

#%%
time_column = 'yyyymm'
time_format = '%Y%m'
id_column = 'spare_part_id'

def deseasonal_detrend(df, id_column, time_column, time_format):
    df = df.copy()
    df[time_column] = al.pd.to_datetime(df[time_column], format=time_format)
    df = df.set_index(time_column)
    parts = df[id_column].unique()
    output = list()
 
    for pn in parts:
        #print(pn)
        timeseries = df[df[id_column]==pn]
        timeseries = timeseries.drop(columns=id_column)
              
        #Checking for trend with adfuller and detrendning with signal detrend if a trend is identified
        result = al.adfuller(timeseries.values)
        
        if result[1] > 0.05:
            detrended = al.signal.detrend(timeseries)
            timeseries['demand_quantity'] = detrended
        
            print("Dataset detrended")

        #Checking for seasonality and deseasonalize
        seasonality = timeseries['demand_quantity'].autocorr()
        if seasonality > 0.75:
            tmp = timeseries.copy()
            tmp['dmd_no_seasonality'] = tmp['demand_quantity'].diff(12)
            tmp['dmd_no_seasonality'] = tmp['dmd_no_seasonality'].fillna(0)
            average = tmp['demand_quantity'].mean()
            tmp['demand_no_seasonlity'] = average+tmp['dmd_no_seasonality'] 
            
            ts_decompose = al.seasonal_decompose(x=timeseries, model='additive')
            deseasonalized = timeseries.demand_quantity.values - ts_decompose.seasonal
            
            timeseries['demand_quantity'] = deseasonalized
        
            print('Dataset deseasonalized')
        
        #Return the output
        output.append(timeseries)
    output = al.pd.concat(output)

    return(output)

    
# %%
deseasonal_detrend(ad.data_set, id_column, time_column, time_format)
# %%
