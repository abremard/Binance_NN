"""Unit Tests
    Author :
        Alexandre Bremard
    Version Control :
        1.0 - 09/26/2020 : test_get_historical_prices_1(), test_format_input_1()
    Todo :
        Add test_train, test_test, test_predict
"""

import dataPrep as dataPrep
import model as model
import os

def test_get_historical_prices_1():
    """ Simple BTCUSDT 1h historical price extraction

    Returns:
        bool: Test result
    """    
    if os.path.exists('../tmp/test_get_historical_prices_1.csv'):
        os.remove('../tmp/test_get_historical_prices_1.csv')
    dataPrep.get_historical_prices(symbol='BTCUSDT', time='1h', export_path='../tmp/test_get_historical_prices_1.csv', verbosity='NONE')
    if os.path.exists('../tmp/test_get_historical_prices_1.csv'):
        return True

def test_format_input_1():
    """ Test data preparation : dataframe -> numpy keras-friendly input data

    Returns:
        bool: Test result
    """
    x_array, y_array = dataPrep.format_input(import_path='../tmp/test_format_input_1.csv', import_cols=['close'], time_window=5, verbosity='NONE')
    if x_array is not None and y_array is not None:
        return True

def test():
    """Run each unit tests one by one
    """    
    # test_get_historical_prices_1_result = test_get_historical_prices_1()
    # print('Test Get Historical Prices 1 - '+str(test_get_historical_prices_1_result))
    # test_format_input_1_result = test_format_input_1()
    # print('Test Format Input 1 - '+str(test_format_input_1_result))
    x_array, y_array = dataPrep.format_input(import_path='../tmp/test_format_input_1.csv', import_cols=['close'], time_window=50, nrows=10000, verbosity='DEBUG')
    model.train(x_array=x_array, y_array=y_array)