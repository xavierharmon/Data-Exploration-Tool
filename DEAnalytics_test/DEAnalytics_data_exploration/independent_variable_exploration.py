import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from DEAnalytics_test import config

def correlationfunction(corr_method = 'pearson'):
	'''
	
	'''
    corrmatrix = pd.DataFrame()
    relationships_df = pd.DataFrame()
    input_df = config.startdata.select_dtypes(include = np.number)
    for a in list(input_df.columns.values):
        for b in list(input_df.columns.values):
            corrmatrix.loc[a,b] = input_df.corr().loc[a,b]
            if input_df.corr(method = corr_method).loc[a,b] >= 0.05:
                if a != b:
                    relationships_df = relationships_df.append({'Var1' : a, 'Var2' : b, 'Corr_coeff' :input_df.corr().loc[a,b] }, ignore_index = True)
    return corrmatrix,relationships_df
	
def logisticfeatureimportance():
    logit_dataframe = config.startdata.select_dtypes(include = np.number)
    x_var = logit_dataframe.drop(target_variable, axis = 1)
    y_var = logit_dataframe[target_variable]
    logit_model = LogisticRegression()
    logit_model.fit(x_var,y_var)
    logit_importance = logit_model.coef_[0]
    logit_importance_final = pd.Series(logit_importance, index = x_var.columns)
    print(logit_importance_final)
    logit_fi_image = logit_importance_final.plot(kind = 'bar')
    logit_image = logit_fi_image.get_figure().savefig('logisticRegressionFeatureImportance.png')
   
def decisiontree_reg_featureimportance():
    input_df = config.startdata.select_dtypes(include = np.number)
    y_var = input_df[target_variable]
    x_var = input_df.drop([target_variable], axis = 1)
    dt_regressor_model = DecisionTreeRegressor()
    dt_regressor_model.fit(x_var, y_var)
    dt_regressor_importance = dt_regressor_model.feature_importances_
    dt_regressor_final = pd.Series(dt_regressor_importance, index = x_var.columns)
    print(dt_regressor_final)
    dt_reg_fi_image = dt_regressor_final.plot(kind = 'bar')
    dt_reg_image = dt_reg_fi_image.get_figure().savefig('DecisionTreeRegressionFeatureImportance.png')

def decisiontree_class_featureimportance():
    input_df = config.startdata.select_dtypes(include = np.number)
    y_var = input_df[target_variable]
    x_var = input_df.drop([target_variable], axis = 1)
    dt_class_model = DecisionTreeClassifier()
    dt_class_model.fit(x_var, y_var)
    dt_class_importance = dt_class_model.feature_importances_
    dt_class_final = pd.Series(dt_class_importance, index = x_var.columns)
    print(dt_class_final)
    dt_class_fi_image = dt_class_final.plot(kind = 'bar')
    dt_class_image = dt_class_fi_image.get_figure().savefig('DecisionTreeClassifierFeatureImportance.png')
	
def randomforest_reg_featureimportance():
    input_df = config.startdata.select_dtypes(include = np.number)
    y_var = input_df[target_variable]
    x_var = input_df.drop([target_variable], axis = 1)
    rf_reg_model = RandomForestRegressor()
    rf_reg_model.fit(x_var, y_var)
    rf_reg_importance = rf_reg_model.feature_importances_
    rf_reg_final = pd.Series(rf_reg_importance, index = x_var.columns)
    print(rf_reg_final)
    rf_reg_fi_image = rf_reg_final.plot(kind = 'bar')
    rf_reg_image = rf_reg_fi_image.get_figure().savefig('RandomForestRegressionFeatureImportance.png')	
	
 def randomforest_class_featureimportance():
    input_df = config.startdata.select_dtypes(include = np.number)
    y_var = input_df[target_variable]
    x_var = input_df.drop([target_variable], axis = 1)
    rf_class_model = RandomForestClassifier()
    rf_class_model.fit(x_var, y_var)
    rf_class_importance = rf_class_model.feature_importances_
    rf_class_final = pd.Series(rf_class_importance, index = x_var.columns)
    print(rf_class_final)
    rf_class_fi_image = rf_class_final.plot(kind = 'bar')
    rf_class_image = rf_class_fi_image.get_figure().savefig('RandomForestClassificationFeatureImportance.png')  