#%%
from . import anomaly_libs as al
from . import anomaly_models as am

#%% Importing data
data_file = r"C:\Users\A408565\Desktop\GTO\synthetic_input_data.csv"
data_set = al.pd.read_csv(data_file, sep=";")


# %%
def election(v, n_voters):
    """
    Election is the function that is calculating how many models categorized the data point as out/in lier
    Based on that number, it computes the average score. Summ of all results divided by the number of models/voters.
    v - is the DataFrame with indexes and categories of each model(voter)
    n_voters - the number of models that were trained/fit for this run.
    """
    voters = v
    
    print("### Starting the election ...")
    ax = voters.replace(1, 0) # replacing inlier with 0 to be able to compute the average
    am = ax.replace(-1, 1) # replacing outlier with 1 to be able to compute the average
    sum_votes = am.sum(axis='columns') # summing all votes(0, 1) and to know how many models categorized the point as outlier
    election_results = sum_votes / n_voters # simple average. Later to be used with a threshold for final determination (outlier/inlier)
    print("### Election complete!")

    return(election_results, ax, am, sum_votes)


# %%
def get_labels(df, id, *n_features):
    """ 
    df - data frame to be used
    id - the column which contains the spare parts
    n_features - number of features in the dataset
    """
    spare_parts = df[id].drop_duplicates()

    # Initiating containers to append labels from each fit of each model
    print("### Initiating contatiners for votes")
    ifores_labels = []
    #dbscan_labels = []
    ThymeBoost_lables = []
    ocsvm_labels = {}
    lof_labels = {}
    
    
    # To initiate
    if len(ocsvm_labels) < len(am.ocsvm_kernels):    
        for k in am.ocsvm_kernels:
            ocsvm_labels[k] = []
    
    if len(lof_labels) < len(am.lof_algs):
        for alg in am.lof_algs:
            lof_labels[alg] = []
    print("### Containers initiated")


    print("### Preparing the Data Frame")
    for spare_part in spare_parts:

        #print(spare_part)
        part_df = df.where(df[id] == spare_part).dropna()
        part_df.drop(id, axis=1, inplace=True)
        part_df.drop('yyyymm', axis=1, inplace=True)

        #part_df = StandardScaler().fit_transform(part_df.values.reshape(-1, 1))
        #part_df = pd.DataFrame(part_df)
        
        
        #dbscan_labels.extend(fit_dbscan(part_df, 3, 5))
        print("### Fitting Isolation Forest")
        ifores_labels.extend(am.fit_iforest(part_df, 0.01))
        print("### Fitting ThymeBoost")
        ThymeBoost_lables.extend(am.fit_ThymeBoost(part_df, 12))

        print("### Fitting OCSVM")
        for k in am.ocsvm_kernels:
            print(f"###===> Fitting OCSVM: {k}")
            ocsvm_labels[k].extend(am.fit_oc_svm(part_df, k))

        print("### Fitting LOF")
        for l_alg in am.lof_algs:
            print(f"###===> Fitting OCSVM: {l_alg}")
            lof_labels[l_alg].extend(am.fit_lof(part_df, l_alg))  

    
    print("### Collecting the results from voters")
    for k in am.ocsvm_kernels:
        df[f'ocsvm_{k}'] = ocsvm_labels[k]
    for l_alg in am.lof_algs:
        df[f'lof_{l_alg}'] = lof_labels[l_alg]
    #df['dbscan_lbls'] = dbscan_labels
    df['iforest_lbls'] = ifores_labels
    df['ThymeBoost_lbls'] = ThymeBoost_lables
    df["ThymeBoost_lbls"] = df["ThymeBoost_lbls"].astype(str).astype(int)
    print("### Results collected!")


    return(df)


# %%
def anomaly_detector(data_frame, id, dimensions=1, **params):

    """
    Add your description here
    """

    initial_shape = data_frame.shape[1]
    
    print("### Getting labels")
    if dimensions == 1: # the univariate option
        full_df = get_labels(data_frame, id, 1)
    elif dimensions >= 2: # multivariate option
        pass # to decide about the approach
    else:
        print("Garbage value for dimensions [it is expected to be 1 for 1D data and 2+D for multidimensional data]")
    print("### Got labels")

    final_shape = full_df.shape[1]
    new_columns = final_shape - initial_shape
    print(f"### New columsn: {new_columns}")

    voters = full_df.iloc[:, initial_shape:]
    
    print("### Preparing for election.")
    data_frame = data_frame.iloc[:, :initial_shape]
    data_frame['labels'], ax, am, sum_votes = election(voters, new_columns)
    #data_frame['labels'] = data_frame['labels'].apply(lambda x: 1 if x >= 0.7 else 0)
    
    return(data_frame, voters, full_df, ax, am, sum_votes)