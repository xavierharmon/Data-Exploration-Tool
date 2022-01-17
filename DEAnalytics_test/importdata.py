from DEAnalytics_test import config
import pandas as pd
import numpy as np
import datetime
import os
from pandas.io.json import json_normalize
import requests
from requests.auth import HTTPBasicAuth
import sys

#Error handling customized for the script
class InvalidYear(Exception):
    def __init__(self, beginyear_cpi, endyear_cpi):
        self.beginyear_cpi = beginyear_cpi
        self.endyear_cpi = endyear_cpi
        iy_message = f'Please choose a year between {self.beginyear_cpi2} and {self.endyear_cpi2}.'
        super().__init__(iy_message)

class InvalidMonth(Exception):
    def __init__(self):
        im_message = f'You have chosen a month that has not yet occurred, please try again.'
        super().__init__(im_message)

class MissingDataFrame(Exception):
    def __init__(self, previousfunctionname):
        self.previousfunctionname = previousfunctionname
        mdf_message = f'The required dataframe is empty, please be sure the function {previousfunctionname} has been properly run.'
        super().__init__(mdf_message)

class ExceededAttempts(Exception):
    def __init__(self):
        excatt_message = f'You have exceeded the number of attempts, please check your inputs and try again.'
        super().__init__(excatt_message)



##Custom Functions for this package
##This package works with the ARIMA model specifically to ensure that no matter what date is input to begin the forecast, we capture the start of the week on sunday
def last_sunday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead >= 0: # Target day already happened this week
        days_ahead -= 7
    return d + datetime.timedelta(days_ahead)

##This function makes sure that no matter what date is input into the ARIMA model we get the first day of the month if the user selects MonthStart for their aggregation
def first_day_of_month(date):
    date = datetime.datetime.strptime(date, '%m-%d-%Y').date()
    first_day = datetime.datetime(date.year, date.month, 1)
    return first_day.strftime('%Y-%m-%d')

#This function will present the data with columns in the format they need to be in
#for the timeseries function dates need to be in date format not strings
#If there are groups in the data they need to be strings
#This function also normalizes the data using the CPI index (consumer price index)
#The CPI is gathered using an API call, and using the developer key we only have 500 API calls per day

def import_data():
    filepath_attempts = config.parameters.zero
    while filepath_attempts < config.parameters.attempts_max:
        filepath = input(config.wrapper.fill('Please place the complete file path here with the file name for your dataset in .csv or .xlsx format.'))
        if os.path.exists(filepath):
            break
        else:
            filepath_attempts += 1
            print(config.wrapper.fill(f'The file path you have tried to import is not valid, please check to make sure you have the correct file path with the file name and try again. You have {3-filepath_attempts} attempts remaining.'))
            if filepath_attempts == config.parameters.attempts_max:
                raise(ExceededAttempts)
                exit()
    filepath_last_chars = filepath[-3:]
    if filepath_last_chars == 'csv':
        config.startdata = pd.read_csv(filepath)
    elif filepath_last_chars == 'xlsx':
        config.startdata = pd.read_xlsx(filepath)
    else:
        print(config.wrapper.fill('Please make sure your file is in .csv or .xlsx format for the import data function and try again.'))
    config.startdata = pd.read_csv(fr'{filepath}')
    config.startdata.columns = config.startdata.columns.str.lower()
    y_attempts = config.parameters.zero
    while y_attempts < config.parameters.attempts_max:
        yvariablebox = input('What is the dependent (y) variable for your dataset?')
        config.y = yvariablebox.lower()
        if config.y in config.startdata.columns:
            break
        else:
            y_attempts += 1
            print(f'Time variable cannot be found in data file you imported.Please try again. You have {3-y_attempts} attempts remaining before the script will close.')
            if y_attempts == config.parameters.attempts_max:
                raise(ExceededAttempts)
                exit()
    if config.startdata[config.y].dtype == np.int64 or config.startdata[config.y].dtype == np.float64:
        'Dependent variable datatype is correct, the program will proceed.'
    else:
        config.startdata[config.y] = config.startdata[config.y].str.replace(',','')
        config.startdata[config.y] = pd.to_numeric(config.startdata[config.y])
        warnings.warn('\n' + '\n' + config.wrapper.fill('The specified column was not an integer or float datatype so the package has converted all datapoints in the column to an integer.'), Warning)
    config.project_name = f'{config.y}'
    hastimevariable = input(config.wrapper.fill('Does your dataset have a time component? (y/n).'))
    hastimecomponent_attempts = config.parameters.zero
    while hastimecomponent_attempts < config.parameters.attempts_max:
        if hastimevariable == 'n':
            break
        else:
            timevar_attempts = config.parameters.zero
            while timevar_attempts < config.parameters.attempts_max:
                timevariablebox = input('What is the time variable you wish to use for your model?')
                config.timevariable = timevariablebox.lower()
                if config.timevariable in config.startdata.columns:
                    break
                else:
                    timevar_attempts += 1
                    print(f'Time variable cannot be found in data file you imported.Please try again. You have {3-timevar_attempts} attempts remaining before the script will close.')
                    if timevar_attempts == config.parameters.attempts_max:
                        raise(ExceededAttempts)
                        exit()
            resample_attempt = config.parameters.zero
            while resample_attempt < config.parameters.attempts_max:
                config.resamplefreq = input(config.wrapper.fill('What time frequency do you want for your output? Type MS for Monthly and W for weekly results. If your data is already aggregated to a weekly or monthly level please choose that option.'))
                if config.resamplefreq in ['MS','W']:
                    break
                else:
                    resample_attempt += 1
                    print(f'You did not select a valid frequency, please use MS for monthly time series results and W for weekly results.')
                    if resample_attempt == config.parameters.attempts_max:
                        raise(ExceededAttempts)
                        exit()
            config.forecaststeps = input(config.wrapper.fill('How many periods into the future would you like to generate your forecast for? By default the package has set this value to 12, Keep in mind the granularity of your data. Here 12 would be a year for monthly data while 52 would be a year for weekly data. Please use integers'))
            config.forecaststeps = int(config.forecaststeps)
            config.splitdf = input(config.wrapper.fill('Will you need to split your dataset into a testing and training dataset for validating your model? y/n'))
            if config.splitdf.lower() == 'y':
                inputdate = input(config.wrapper.fill('What date do you wish to split your dataset into a training and testing dataset? This is not the date the forecast will begin.'))
                if config.resamplefreq == 'MS':
                    config.testdate = first_day_of_month(inputdate)
                else:
                    inputdate = datetime.datetime.strptime(inputdate, '%m-%d-%Y').date()
                    config.testdate = last_sunday(inputdate, 6) 
            groupsindata = input('Do you have groups in your dataset? With groups you will be able to run a seperate timeseries model for each group. Please type (Y/N)')
            if groupsindata.lower() == 'y':
                group_attempt = config.parameters.zero
                while group_attempt < config.parameters.attempts_max:
                    groupbox = input('What is the column name for the groups in your dataset?')
                    config.group = groupbox.lower()
                    if config.group in config.startdata.columns:
                        config.startdata[config.group] = config.startdata[config.group].astype(str)
                        break
                    else:
                        group_attempt += 1
                        print(f'Time group variable cannot be found in data file you imported.Please try again. You have {3-group_attempt} attempts remaining before the script will close.')
                        if group_attempt == config.parameters.attempts_max:
                            raise(ExceededAttempts)
                            exit()
            config.startdata[config.timevariable] = pd.to_datetime(config.startdata[config.timevariable])
            config.startdata['period'] = (config.startdata[config.timevariable].dt.strftime('%B'))
            config.startdata['year'] = (config.startdata[config.timevariable].dt.year)
    normalizedata = input('Do you want to normalize any monetary data? (acceptable answers are yes/no or y/n)')
    if normalizedata.upper() == 'YES' or normalizedata.upper() == 'Y':
        cpi_frame = pd.DataFrame()
        headers = {'Content-type': 'application/json'}
        endyear_cpi = date.today().year
        beginyear_cpi = endyear_cpi - 10
        jsondata = json.dumps({"seriesid": ['CUUR0000SA0'],"startyear":beginyear_cpi, "endyear": endyear_cpi})
        p = requests.get('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=jsondata, headers=headers, auth = HTTPBasicAuth('apikey', 'e5f82668f98943a6becb6c6dfb08841f'))
        json_data = json.loads(p.text)
        print('\n' + config.wrapper.fill('You are about to run a function to generate the Consumer Price Index (CPI). The CPI can be used to account for inflation in monetary data.'))
        chooseyear = input('What year do you want to index data to?')
        #Checking to make sure the year is valid otherwise raising a custom error
        if int(chooseyear) < beginyear_cpi or int(chooseyear) > endyear_cpi: 
            raise InvalidYear(beginyear_cpi, endyear_cpi)
        choosemonth = input(f'What month of {chooseyear} do you want to index data to?')
        #Checking to make sure the month is not in the future, if it is raising a custom error
        if int(chooseyear) == endyear_cpi and int(datetime.datetime.strptime(choosemonth.capitalize(),"%B").strftime("%m")) > (date.today().month - 1):
            raise InvalidMonth()
        #If the user inputs an integer instead of spelling out the month this will find the proper month text to avoid errors.
        if choosemonth.isnumeric() == True: 
            datetime_object = datetime.datetime.strptime(choosemonth, "%m")
            choosemonth = datetime_object.strftime("%B")
        for series in json_data['Results']['series']:
            cs = ["series id","year","period","value"]
            for item in series['data']:
                data_ses = np.array([series['seriesID'],item['year'], item['periodName'], item['value']])
                row_seperator = item['year'] + '_' + item['periodName']
                cpi_f = pd.DataFrame([data_ses],[row_seperator],columns = cs)
                cpi_frame = cpi_frame.append(cpi_f)
        x = cpi_frame.loc[(cpi_frame['year'] == chooseyear)&(cpi_frame['period'] == choosemonth.capitalize()), 'value'].values
        cpi_frame['CPI'] = x.astype(float)/cpi_frame['value'].astype(float)
        cpi_frame['year'] = cpi_frame['year'].astype(int)  
    if normalizedata.upper() == 'YES' or normalizedata.upper() == 'Y':
        config.startdata = pd.merge(config.startdata, cpi_frame, on = ["period", "year"], how = 'left')
        config.startdata['NormalizedValue'] = config.startdata['Cost'] * config.startdata['CPI']
    return config.startdata


