from DEAnalytics_test import config
from DEAnalytics_test.DEAnalytics_data_exploration import datacleanup as dc



#Using Label encoding for variables that have only two options/unique values
def label_encoding():
    '''
    Encodes Categorical variables in one column
    
    Returns
    -------
    imported_dataset
        A transformed categorical variable where the column is now numerical
        and valid for use in our models    
    '''
    for i in config.startdata:
        if config.startdata[i].dtype == 'object':
            if config.startdata[i].nunique() == 2:
                config.startdata[i] = config.startdata[i].astype('category')
                config.startdata[i] = config.startdata[i].cat.codes
                dc.explore_df_results = dc.explore_df_results.append({'Topic': 'Encoding Categorical Variables',
                                                                   'Message' : f'Variable {i} was convered using label encoding.',
                                                                   'ConcernFlag' : 0}, ignore_index = True)
    return config.startdata

#Using One Hot Encoding for variables that have more than 2 options
def one_hot_encoding(pf = None,pfsep = '_'):
    '''
    Encodes Categorical variables with one-hot encoding
    
    Parameters
    ----------
    pf
        prefix, used to help identify the new columns created through
        one hot encoding, by default we have no prefix
        
    pfsep
        prefix separator, by default if we were to use a separator for 
        our prefix it will be an underscore _
    
    Returns
    -------
    imported_dataset
        A transformed categorical variable where the column is now numerical
        and valid for use in our models. With one-hot encoding will be multiple
        new columns.
    '''
    for i in config.startdata:
        if config.startdata[i].dtype == 'object':
            if config.startdata[i].nunique() > 2:
                config.startdata =  pd.get_dummies(config.startdata, prefix = pf, prefix_sep = pfsep, columns = [i], dtype = int)
                dc.explore_df_results = dc.explore_df_results.append({'Topic': 'Encoding Categorical Variables',
                                                                   'Message' : f'Variable {i} was convered using one-hot encoding.',
                                                                   'ConcernFlag' : 0}, ignore_index = True)
    return config.startdata
