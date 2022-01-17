from DEAnalytics_test import importdata as imp
from DEAnalytics_test.DEA_timeseries import SimpleExpSmoothing as ses

class run_no_code():
	imp.import_data()
	ses.printing()