import pandas as pd
from matplotlib import pyplot as plt
import numpy
from DEAnalytics_test import config
from DEAnalytics_test.DEAnalytics_data_exploration import datacleanup as dc

def categorical_target_weights():
	'''
	Generates weights for our categorical variables to understand if we have any
	variables that are overweighted and could cause balancing issues in our final result set
	
	Returns
	-------
	target_freq
		A table of our target variables, their frequencies, 
		and the proportion of the total result set that
		contains that value.
	'''
    global explore_df_results
    target_freq = pd.DataFrame()
    target_freq['Count'] = config.startdata.groupby(target_variable).size()
    target_freq['Percentage'] = config.startdata.groupby(target_variable).size().transform(lambda x: x/x.sum())
    max_percent = round(max(target_freq['Percentage']), 2)
    weight_number_groups = 1/len(target_freq.index)
    categoricalpath = config.project_name + '/dataexplorationtool/categoricalresults'
    target_freq.to_csv(categoricalpath + '/targetvariableweights.csv',',')
    print(wrapper.fill('Target variable weights have been saved to a local folder <insert path here> under the file name targetvariableweights.csv. To access this information you can run the pd.read_csv() command.'))
    print('\n')
    if max_percent > (weight_number_groups):
        unequal_weight_text = wrapper.fill(f'An equally distributed target variable would have a weight of {weight_number_groups}, but based on your potential categorical response options you have an unequal distribution for your responses with a max of {max_percent}. Be aware of this imbalanced data as you proceed with your analysis.')
        print(unequal_weight_text)
        explore_df_results = explore_df_results.append({'Topic' : 'Variable Weights',
                                                      'Message' : 'Unequal distribution for response variable',
                                                      'ConcernFlag' : 1}, ignore_index = True)
    else:
        explore_df_results = explore_df_results.append({'Topic' : 'Variable Weights',
                                                      'Message' : '',
                                                      'ConcernFlag' : 0}, ignore_index = True)
    return target_freq
	

	
def crosstab_data():
    '''
    Runs Cross tabulation of our dataset with the categorical variables
    to help us understand the relationship between our dependent (y)
    variable and our other independent (x) variables
    
    Returns
    -------
    dict_of_df
        Dictionary of dataframes used to help understand each 
        cross tabular output. This will be used in the report
        at the end of our program.
    '''
    df_x = config.startdata.drop(target_variable, axis = 1)

    df_y = config.startdata[target_variable]
    global dict_of_df
    dict_of_df = {}
    for i in df_x:
        if df_x[i].nunique() <= 10:
            dict_of_df['df_{}'.format(i)] =  pd.crosstab(df_y, df_x[i])
    return dict_of_df	
	
def crosstab_visuals():
	'''
	Creates plots for each of the X and Y relationships
	to help visualize the crosstabular data in a different way
	
	Returns
	-------
	A plot for each X and Y relationship. These plots are also saved
	in a folder in the data exploration directory.
	'''
    df_x = config.startdata.drop(target_variable, axis = 1)
    df_y = config.startdata[target_variable]
    global report_df
    for i in df_x:
        if df_x[i].nunique() <= 10:
            plot = pd.crosstab(df_x[i], df_y).plot(kind = 'bar')

            plt.title('Frequencies')
            plt.xlabel(i)
            plt.ylabel(target_variable)
            crosstab_image = plot.get_figure().savefig(f'plot_{i}.png')

          