import pandas as pd
import textwrap

#Text Colors
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BrightBlack = '\u001b[30;1m'
    BrightRed = '\u001b[31;1m'
    BrightGreen = '\u001b[32;1m'
    BrightYellow = '\u001b[33;1m'
    BrightBlue = '\u001b[34;1m'
    BrightMagenta = '\u001b[35;1m'
    BrightCyan = '\u001b[36;1m'
    BrightWhite = '\u001b[37;1m'
    Highlight = '\033[0;30;43m'
    END = '\033[0m'

#Parameters for the package
class parameters:
    attempts_max = 3
    zero = 0

#Global Variables for the package
group = ''
y = ''
timevariable = ''
testdate = ''
resamplefreq = ''
startdata = pd.DataFrame()
forecaststeps = 12
aggregate = 'Mean'
splitdf = 'Y'
adfuller_results = pd.DataFrame()
path = ''
images_path = ''
stationary_path = ''
predictions_path = ''
model_summary_path = ''
project_name = ''

#timeseries global variables
timeseries_train_data = pd.DataFrame()
timeseries_test_data = pd.DataFrame()
forecast_data_final = pd.DataFrame()


#Setting up text wrapping for the hints and tips throughout the script. There are three different text wrapping types here
#wrapper is a general text wrapper that inserts line breaks at or before 100 characters, whichever comes first
#wrapper_indent is a wrapper for any text that is indented below a header. It will be denoted by an indention text >>...
#wrapper_head is a wrapper for any text that acts as a heading for a section or block of text, it is denoted by *...
wrapper = textwrap.TextWrapper(width = 100)
prefix = color.BOLD + '   >> ' + color.END
heading = color.BOLD + '*  ' + color.END
wrapper_indent = textwrap.TextWrapper(initial_indent=prefix, width=100, subsequent_indent=' '*len('   >> '))
wrapper_head = textwrap.TextWrapper(initial_indent=heading, width=100, subsequent_indent=' '*len('*  '))
