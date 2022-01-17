from DEAnalytics_test import config
from DEAnalytics_test.DEAnalytics_data_exploration import datacleanup as dc


def drop_null_values():
    '''
    Dropping Null/NAN values
    
    Returns
    -------
    imported_dataset
        The global data frame will now have any rows with null or NaN
        values dropped so we only get records where every column 
        has valid data
    '''
    config.startdata.dropna(inplace = True)
    dc.explore_df_results = dc.explore_df_results.append({'Topic': 'Missing Values',
                                                    'Message' : f'Missing Values Dropped.',
                                                    'ConcernFlag' : 0}, ignore_index = True)
    return config.startdata

def median_impute():
    '''
    Imputes Missing Values
    
    Returns
    -------
    imported_dataset
        Missing values Null/NaN are now imputed with the median for that
        object/column.
    '''
    config.startdata.fillna(config.startdata.median(), inplace = True)
    dc.explore_df_results = dc.explore_df_results.append({'Topic': 'Missing Values',
                                                    'Message' : f'Missing Values imputed with median.',
                                                    'ConcernFlag' : 0}, ignore_index = True)
    return config.startdata
