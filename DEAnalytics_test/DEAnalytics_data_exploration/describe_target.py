from DEAnalytics_test import config
from DEAnalytics_test.DEAnalytics_data_exploration import datacleanup as dc

#define global variable
model_type = ''

def model_selection_tool():
    '''
    Trying to identify the type of response of the target variable
    
    Returns
    -------
    model_type
        a variable that will be used in the data exploration tool to help drive the decision points
        for data exploration
    '''
    global model_type
    responses = len(config.startdata.groupby(target_variable))
    df_length = len(config.startdata)
    if responses == 2:
        model_type = 'Binary'
        explore_df_results = explore_df_results.append({'Topic' : 'Model Selection',
                                                      'Message' : 'Binary response variable, using categorical exploration tools.',
                                                      'ConcernFlag' : 0}, ignore_index = True)
    elif responses > 2 and responses <= (df_length *0.5):
        model_type = 'Multinomial'
        explore_df_results = explore_df_results.append({'Topic' : 'Model Selection',
                                                      'Message' : 'Multinomial response variable, using various data exploration tools.',
                                                      'ConcernFlag' : 0}, ignore_index = True)
    elif responses >= (df_length * 0.5):
        model_type = 'Continuous'
        explore_df_results = explore_df_results.append({'Topic' : 'Model Selection',
                                                      'Message' : 'Continuous response variable, using continuous exploration tools.',
                                                      'ConcernFlag' : 0}, ignore_index = True)
    return model_type