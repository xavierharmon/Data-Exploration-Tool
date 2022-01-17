import sys 
sys.path.append(r'C:\Users\HarmonX\Documents')
import os
import sys
from DEAnalytics_test import config as c

def make_new_directory():
    c.path = f'{c.project_name}/dataexplorationtool'
    if not os.path.exists(c.path):
        os.makedirs(c.path)
    c.images_path = f'{c.path}/charts'
    if not os.path.exists(c.images_path):
        os.makedirs(c.images_path)
	c.categorical_path = f'{c.path}/categoricalresults'
	if not os.path.exists(c.categorical_path):
		os.makedirs(c.categorical_path)
    