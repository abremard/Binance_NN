"""
    Author :
        Alexandre Bremard
    Version Control :
        1.0 - 09/25/2020 : get_historical_prices()
        1.1 - 09/26/2020 : format_input()
    Todo :
        get_historical_prices()
        - add end timestamp for data collect
        - convert close_time to date
"""

import os
import btalib
import pandas as pd
import json
import logging
import numpy as np
import datetime
import debugUtils as debugUtils
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

# constant
import_cols = ['date', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'base_asset_vol', 'trades', 'taker_buy_vol', 'taker_buy_base_asset_vol', 'ignore']
# default
export_cols = ['open', 'high', 'low', 'close', 'volume', 'close_time', 'base_asset_vol', 'trades', 'taker_buy_vol', 'taker_buy_base_asset_vol', 'ignore']
import_cols = ['open', 'high', 'low', 'close', 'volume', 'close_time', 'base_asset_vol', 'trades', 'taker_buy_vol', 'taker_buy_base_asset_vol', 'ignore']
testnet_client = Client('g852Dn6vv1zQ3zFJ6s9KCilduMTC3EZXbqgPUywhotpnBWK7ZPtd0LmDv4e5COVF', 'CuaRMQpu8UqKNyyqS1F7hDRz5hXUqaesOEH4pnRhlfG3Ql3rTbzX4PsiBqxhZ122')

def get_historical_prices(symbol = None, time = None, export_path = None, timestamp=None, client = testnet_client, export_cols=export_cols, verbosity = 'NORMAL', log_level = 'DEBUG'):
    """ Extract historical prices data

    Args:
        symbol (str, mandatory): trading pair eg. 'BTCUSDT'
        time (str, mandatory): frequency eg. '1h', valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        export_path (str, mandatory): csv export path eg. '../data/my-data.csv'
        timestamp (str, optional): starting timestamp for data collect. Defaults to earliest valid timestamp.
        client (binance.client.Client, optional): client connection using API key + secret. Defaults to testnet_client.
        export_cols (str[], optional): csv export columns to keep. Defaults to export_cols.
        verbosity (str, optional): Defaults to 'NORMAL'.
        log_level (str, optional): Defaults to 'DEBUG'.
    """
    try:
        debugUtils.task_start('GET HISTORICAL PRICES', verbosity)

        # get timestamp
        if timestamp is None:
            timestamp = client._get_earliest_valid_timestamp(symbol, time)
        if verbosity == 'DEBUG':
            print('Earliest valid timestamp is ' + datetime.datetime.fromtimestamp(timestamp/1000).strftime('%m-%d-%Y %H:%M:%S'))
        if log_level == 'DEBUG':
            logging.debug('GET HISTORICAL PRICES - Earliest valid timestamp is ' + datetime.datetime.fromtimestamp(timestamp/1000).strftime('%m-%d-%Y %H:%M:%S'))

        # data fetch
        if verbosity == 'DEBUG':
            print('Fetching bars ...')
        if log_level == 'DEBUG':
            logging.debug('GET HISTORICAL PRICES - Fetching bars ...')
        bars = client.get_historical_klines(symbol, time, timestamp)
        if verbosity == 'DEBUG':
            print('Bars fetched successfully, converting to dataframe ...')
        if log_level == 'DEBUG':
            logging.debug('GET HISTORICAL PRICES - Bars fetched successfully, converting to dataframe ...')

        # dataframe conversion
        df = pd.DataFrame(bars, columns=import_cols)
        if verbosity == 'DEBUG':
            print('Converted successfully, setting index ...')
        if log_level == 'DEBUG':
            logging.debug('GET HISTORICAL PRICES - Converted successfully, setting index ...')

        # set index
        df.set_index('date', inplace=True)
        if verbosity == 'DEBUG':
            print('Index is set, converting index to human-readable date ...')
        if log_level == 'DEBUG':
            logging.debug('GET HISTORICAL PRICES - Index is set, converting index to human-readable date ...')

        # index conversion
        df.index = pd.to_datetime(df.index, unit='ms')
        if verbosity == 'DEBUG':
            print('Converted successfully, exporting to csv ...')
        if log_level == 'DEBUG':
            logging.debug('GET HISTORICAL PRICES - Converted successfully, exporting to csv ....')

        # csv export
        df.to_csv(export_path, columns=export_cols)
        if verbosity == 'DEBUG':
            print('Data exported successfully!')
        if log_level == 'DEBUG':
            logging.debug('GET HISTORICAL PRICES - Data exported successfully!')
        if verbosity is not 'NONE':
            print(df.head())

    except Exception as e:
        debugUtils.task_fail('GET HISTORICAL PRICES', verbosity, e)

    else:
        debugUtils.task_success('GET HISTORICAL PRICES', verbosity)


def format_input(import_path = None, import_cols=import_cols, time_window=10, nrows=None, verbosity = 'NORMAL', log_level = 'DEBUG'):
    """ Convert dataframe to a usable form for training

    Args:
        import_path (str, optional): Defaults to None.
        import_cols (str[], optional): Defaults to import_cols.
        time_window (int, optional): Nb periods back used for prediction. Defaults to 10.
        verbosity (str, optional): Defaults to 'NORMAL'.
        log_level (str, optional): Defaults to 'DEBUG'.

    Returns:
        x_array (numpy.array), y_array (numpy.array): train set, label set
    """
    try:
        debugUtils.task_start('FORMAT INPUT', verbosity)

        # read csv
        if verbosity == 'DEBUG':
            print('Reading csv ...')
        if log_level == 'DEBUG':
            logging.debug('FORMAT INPUT - Reading csv ...')
        if nrows is not None:
            df = pd.read_csv(import_path, usecols=import_cols, nrows=nrows)
        else:
            df = pd.read_csv(import_path, usecols=import_cols)
        if verbosity == 'DEBUG':
            print('Data imported successfully, flattening dataframe ...')
        if log_level == 'DEBUG':
            logging.debug('FORMAT INPUT - Data imported successfully, flattening dataframe ...')
        if verbosity is not 'NONE':
            print(df.head())
            print(df.shape)

        # flatten
        x_array = []
        y_array = []
        for i in range(df.shape[0]-time_window):
            df_slice = df[i:time_window+i]
            mean = df_slice.mean()
            std = df_slice.std()
            df_slice = (df_slice-mean)/std
            flatten_df = df_slice.values.flatten()
            x_array.append(flatten_df.reshape(time_window,1))
            y_array.append((df.iloc[i+1,:].values[0] - mean)/std)
        if verbosity == 'DEBUG':
            print('Dataframe flattened successfully, converting to numpy object ...')
        if log_level == 'DEBUG':
            logging.debug('FORMAT INPUT - Dataframe flattened successfully, converting to numpy object ...')

        # convert to numpy
        x_array = np.asarray(x_array)
        y_array = np.asarray(y_array)
        if verbosity == 'DEBUG':
            print('Converted successfully!')
        if log_level == 'DEBUG':
            logging.debug('FORMAT INPUT - Data imported successfully, flattening dataframe!')
        if verbosity is not 'NONE':
            print('x_array shape : '+str(x_array.shape))
            print('y_array shape : '+str(y_array.shape))
        return x_array, y_array

    except Exception as e:
        debugUtils.task_fail('FORMAT INPUT', verbosity, e)

    else:
        debugUtils.task_success('FORMAT INPUT', verbosity)
