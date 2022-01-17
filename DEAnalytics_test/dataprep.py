from DEAnalytics_test import config
import sys
import os

def make_new_directory():
    config.path
    config.images_path
    config.stationarity_path
    config.predictions_path
    config.model_summary_path
    config.path = config.project_name
    if not os.path.exists(config.path):
        os.makedirs(config.path)
    config.images_path = f'{config.path}/charts'
    if not os.path.exists(config.images_path):
        os.makedirs(config.images_path)
    config.stationarity_path = f'{config.path}/stationarity_tests'
    if not os.path.exists(config.stationarity_path):
        os.makedirs(config.stationarity_path)
    config.predictions_path = f'{config.path}/predictions'
    if not os.path.exists(config.predictions_path):
        os.makedirs(config.predictions_path)
    config.model_summary_path = f'{config.path}/modelsummary'
    if not os.path.exists(config.model_summary_path):
        os.makedirs(config.model_summary_path)

def clean_up_data(config.startdata, config.target):
    global forecast_data
    global forecast_data_final
    config.aggregate
    config.timevariable
    config.resamplefreq
    config.group

    forecast_data = config.startdate.copy()
    forecast_data_agg = pd.DataFrame()
    forecast_data_final = pd.DataFrame()

    if forecast_data[config.timevariable].dtype != 'datetime64[ns]':
        forecast_data.timevariable = pd.to_datetime(forecast_data[config.timevariable])


    if config.group == '':
        forecast_data_reindex = forecast_data.set_index(forecast_data[config.timevariable])
        if config.aggregate == 'Mean':
            forecast_data_final['Y'] = forecast_data_reindex[config.target].resample(config.resamplefreq).mean()
        else:
            forecast_data_final['Y'] = forecast_data_reindex[config.target].resample(config.resamplefreq).sum()
    else:
        forecast_data_groups = forecast_data.groupby([config.group])
        for g in forecast_data_groups.groups:
            forecast_g = forecast_data_groups.get_group(g)
            forecast_data_reindex = forecast_g.set_index(forecast_g[config.timevariable])
            if config.aggregate == 'Mean':
                forecast_data_agg['Y'] = forecast_data_reindex[config.target].resample(config.resamplefreq).mean()
                forecast_data_agg[config.group] = g
            else:
                forecast_data_agg['Y'] = forecast_data_reindex[config.target].resample(config.resamplefreq).sum()
                forecast_data_agg[config.group] = g
            forecast_data_final = forecast_data_final.append( forecast_data_agg, ignore_index = False)
            

