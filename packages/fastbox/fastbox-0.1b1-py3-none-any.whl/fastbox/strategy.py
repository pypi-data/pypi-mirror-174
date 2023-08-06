from functools import partial
import pandas as pd
import numpy as np
from io import BytesIO
import json


from typing import Optional, Union, Literal, List
from pydantic import confloat, conint, PositiveFloat, PositiveInt
from .utils.utils import SERVERROOT, TOKEN, LANG
# from ..utils.utils import 
from .utils.utils import sendRequest, sendRequestGetText
from .utils.utils import write_to_buffer
from .pydantic.models import TCostModel, NpDatetime

from .utils import utils_plotting as plt

__all__ = ['']

def help(method: str = ''):
    url = SERVERROOT + '/strategy/help/{0}'.format(method)
    res = sendRequest(url=url)
    if res != None:
            print(res)  

def process(
        strategy,
        strategy_type: Optional[str] = 'nshares',
        from_date: Optional[NpDatetime] = None,
        to_date: Optional[NpDatetime] = None,
        price = None,
        bond = None,
        tcosts: Optional[TCostModel] = TCostModel(fees = 0.0002, tax = 0.001)
        ):
    """Process a dataframe strategy.
    Corresponding vector prices, and bond prices are optional (in this case, fetched against the server database)

    Parameters
    ----------
    strategy :              strategy dataframe with 'date' and 'instrumentid'
    price :                 Optional, dataframe of the values of the assets with 'date' and 'instrumentid'. If none -> data are fetched
    bond :                  Optional, daily bond price. If none -> fetch data from Shibor
    tcosts :                Optional, transaction costs turns to default
    strategy_type :         Can be 'nshares' (default), 'vshares' or 'weights'
    from/to_date :          Optional from/to_date

    Returns
    -------
    dataclass with two dataframes: 'value_costs' (P, C, CA, FA) and 'strategy' clean against suspension (nshares, vshares, weights)
    """
    url = SERVERROOT + '/strategy/process'
    files = {}
    if not isinstance(strategy, (pd.DataFrame, pd.Series)):
        return print(
        """You must provide a pandas DataFrame/Series type data/instrumentid of type nshares/vshares/weights/etc.
        """)
    else:
        files['strategy'] = BytesIO(write_to_buffer(strategy))
    if price:
        if not isinstance(price, (pd.DataFrame, pd.Series)):
            return print(
            """If you provide price data, the must be of the type in pandas DataFrame/Series with date and instrumentid
            """) 
        files['price'] = BytesIO(write_to_buffer(price))
    if bond:
        if not isinstance(bond, (pd.DataFrame, pd.Series)):
            return print(
            """If you provide bond data, the must be of the type in pandas DataFrame/Series with date and in bond value (not interest)
            """) 
        files['bond'] = BytesIO(write_to_buffer(bond))
    kwargs = {
        'strategy_type': strategy_type,
        'from_date': from_date,
        'to_date': to_date,
        'tcosts': tcosts.dict()
        }
    data = {'kwargs' : json.dumps(kwargs)}
    return sendRequest(url=url, headers=None, files=files, data=data)
    
def metrics(
        P: pd.DataFrame,
        C: pd.DataFrame = None,
        Bm: pd.DataFrame = None,
        freq: Optional[str] = 'Y',
        metrics : List[str] = ['performance', 'mret', 'mvol', 'maxdropdown', 'sharperatio', 'sortinoratio'],
        strategy_name: str = None,
        benchmark_name: str = None,
        from_date: Optional[NpDatetime] = None,
        to_date: Optional[NpDatetime] = None,
        report = False
        ):
    """Takes a portfolio value P, costs C, benchmark Bm and a list of metrics to return a dataset of metrics and eventually print a report
    
    Parameters
    ----------
    P :                 Dataframe of portfolio value
    C :                 Dataframe of portfolio costs (Optional)
    Bm :                Dataframe or fixed return rate of Benchmark (Optional)
    from/to_date :      np.datetime from to when to do the things
    freq:               can be 'Y' (default), 'Q' or 'M', 'W'
    metrics :           list of the different metrics to provide
    strategy_name :     Name of the strategy (optional)
    benchmark_name :    Name of the benchmark (optional)
    report :            If True print the tables, if False (Default) just return the data

    Returns
    -------
    either a dataframe with the metric data, or print the table
    """

    url = SERVERROOT + '/strategy/metrics'
    files = {}
    if not isinstance(P, (pd.DataFrame, pd.Series)):
        return print(
        """You musst provide 'n_shares', 'price', 'bond' in pandas.DataFrame/Series type.
        """)
    else:
        files['P'] = BytesIO(write_to_buffer(P))
    if C:
        if not isinstance(C, (pd.DataFrame, pd.Series)):
            return print(
            """You musst provide 'n_shares', 'price', 'bond' in pandas.DataFrame/Series type.
            """) 
        files['C'] = BytesIO(write_to_buffer(C))
    if Bm:
        if not isinstance(Bm, (pd.DataFrame, pd.Series)):
            return print(
            """You musst provide 'n_shares', 'price', 'bond' in pandas.DataFrame/Series type.
            """) 
        files['Bm'] = BytesIO(write_to_buffer(Bm))
        kwargs = {
                'from_date':    from_date,
                'to_date':      to_date,
                'freq':         freq,
                'metrics':      metrics,
                'name':         strategy_name,
                'benchmark_name': benchmark_name,
                'report':       report
                }
    data = {'kwargs' : json.dumps(kwargs)}
    return sendRequest(url=url, headers=None, files=files, data=data)

def report(
        strategy: pd.DataFrame,
        strategy_type: Optional[Literal['nshares', 'vshares', 'weights', 'mbm0']] = 'nshares',
        strategy_name: Optional[str] = None,
        Bm: Optional[pd.DataFrame] = None,
        price: pd.DataFrame = None,
        bond: pd.DataFrame = None,
        freq: Optional[Literal['W', 'M', 'Q', 'Y']] = 'Y',
        metrics : List[str] = ['performance', 'mret', 'mvol', 'maxdropdown', 'sharperatio', 'sortinoratio'],
        from_date: Optional[NpDatetime] = None,
        to_date: Optional[NpDatetime] = None,
        name: str = None,
        tcosts: TCostModel = TCostModel(fees = 0.0002, tax = 0.001),
        costs: Optional[bool] = True,
        cash: Optional[bool] = False,
        alpha: Optional[confloat(gt = 0, lt = 1)] = 0.01,
        data: Optional[bool] = False
        ):
    """Report strategy with all the informations

    Parameters
    ----------
    strategy :          dataframe of the strategy
    strategy_type:      'nshares' (default), 'vshares', 'weights'
    strategy_name:      name of the strategy (Optional)
    Bm :                Dataframe of Benchmark value (Optional)
    price :             Dataframe of prices (optional) if none, the prices are fetched from the database.
    bond :              bond value (optional) if none, get the shibor Bond rate
    freq:               Frequency for the metric report 'Y' (default), 'Q', 'M', 'W'
    metrics :           list of the different metrics to provide
    from/to_date :      date
    tcosts :            Transaction costs (turn to default)
    costs :             if True include the costs in the metrics
    cash:               if True report the cash account in the figures
    alpha:              Confidence level for (a)V@R
    data:               if true, returns the data on top of the tables and figures.

    Returns
    -------
    dictionary of {'value_costs': value_costs, 'metrics_date': metrics_data, 'metrics_table': metrics_table, 'risk_data': risk_data}

    """    
    url = SERVERROOT + '/strategy/report'
    files = {}

    if not isinstance(strategy, (pd.DataFrame, pd.Series)):
        return print(
        """You musst provide 'n_shares', 'price', 'bond' in pandas.DataFrame/Series type.
        """)
    else:
        files['strategy'] = BytesIO(write_to_buffer(strategy))
    if price:
        if not isinstance(price, (pd.DataFrame, pd.Series)):
            return print(
            """You musst provide 'n_shares', 'price', 'bond' in pandas.DataFrame/Series type.
            """) 
        files['price'] = BytesIO(write_to_buffer(price))
    if bond:
        if not isinstance(bond, (pd.DataFrame, pd.Series)):
            return print(
            """You musst provide 'n_shares', 'price', 'bond' in pandas.DataFrame/Series type.
            """) 
        files['bond'] = BytesIO(write_to_buffer(bond))
    if Bm:
        if not isinstance(Bm, (pd.DataFrame, pd.Series)):
            return print(
            """You musst provide 'n_shares', 'price', 'bond' in pandas.DataFrame/Series type.
            """) 
        files['Bm'] = BytesIO(write_to_buffer(Bm))
    kwargs = {
        'strategy_type': strategy_type,
        'freq': freq,
        'metrics': metrics,
        'from_date': from_date,
        'to_date': to_date,
        'name': strategy_name,
        'tcosts': tcosts.dict(),
        'costs': costs,
        'cash': cash,
        'alpha': alpha,
        'data': data
        }

    data = {'kwargs' : json.dumps(kwargs)}
    result = sendRequest(url=url, headers=None, files=files, data=data)
    # we first reshape the dataframes in a meaningfull way
    # we got the results
    # 1- We print the tables
    # 2- We plot the data
    # 3- if data = True, we return the data, if not we just print
    if 'fig_performance' in result:
        plt.plot(result['fig_performance'])
    if 'fig_metric' in result:
        plt.plot(result['fig_metric'])
    if 'fig_returns' in result:
        plt.plot(result['fig_returns'])

    print(result['metric_table'])
    
    if data:
        return result
    else:
        return ''
