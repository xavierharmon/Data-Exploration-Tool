from DEAnalytics_test import config
import pandas as pd
import numpy as np


explore_df_results = pd.DataFrame()


#Add logging here so we know what was dropped
def drop_non_categorical_objects(variable_proportion = 0.10):
    '''
    Dropping categorical/object variables that have a significant number of categories
    and likely wont be used in a prediction model think customer name
    
    Parameters
    ----------
    variable_proportion
        This is our threshold, i.e. if it is 0.10 then our dependent categorical variables
        must have a unique count of values less than or equal to 10% of the row count
        for our dataset. This is to eliminate noisy or invalid categorical data
        like customer name.
    
    Returns: 
    imported_dataset with only the categorical variables that might prove valuable
    '''
    config.startdata
    for i in config.startdata:
        if config.startdata[i].dtype == 'object':
            if config.startdata[i].nunique() > len(config.startdata)*variable_proportion:
                explore_df_results = explore_df_results.append({'Topic': 'Categorical Variable Selection',
                                                               'Message' : f'Variable {i} will be dropped from the model.',
                                                               'ConcernFlag' : 0}, ignore_index = True)
                config.startdata = config.startdata.drop([i], axis = 1)
    return config.startdata
