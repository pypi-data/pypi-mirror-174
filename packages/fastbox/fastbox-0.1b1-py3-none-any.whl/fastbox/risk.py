from functools import wraps, partial
from io import BytesIO
import numpy as np
import pandas as pd
import json
from rich import print
from typing import Union, Optional, Literal, Dict

from pydantic import PositiveInt, constr, PositiveFloat, conint, confloat

from .pydantic.models import Dist, DistModel, NpPeriod, NpPeriodModel

from .utils.utils import SERVERROOT, TOKEN, LANG
# from ..utils.utils import 
from .utils.utils import sendRequest, sendRequestGetText
from .utils.utils import write_to_buffer

__all__ = ['']

def help(method: str = ''):
    url = SERVERROOT + '/risk/help/{0}'.format(method)
    res = sendRequest(url=url)
    if res != None:
            print(res)  

def empirical(r: pd.DataFrame, alpha: confloat(gt = 0.0, lt = 1.0) = 0.05, window: PositiveInt = 250):
    url = SERVERROOT + '/risk/empirical'
    if not isinstance(r, (pd.DataFrame, pd.Series)):
        return print(
        """You musst provide 'r' in pandas.DataFrame/Series type.
        """) 
    files = {'r' : BytesIO(write_to_buffer(r))}
    kwargs = dict(
        alpha=alpha,
        window=window,
    )
    data = {'kwargs' : json.dumps(kwargs)}
    return sendRequest(url=url, headers=None, files=files, data=data)

def analytical(r: pd.DataFrame, rvol: pd.DataFrame = None, **kwargs):
    url = SERVERROOT + '/risk/analytical'
    if not isinstance(r, (pd.DataFrame, pd.Series)):
        return print(
        """You musst provide 'r' in pandas.DataFrame/Series type.
        """) 
    if rvol:
        if not isinstance(rvol, (pd.DataFrame, pd.Series)):
            return print(
            """You musst provide 'rvol' in pandas.DataFrame/Series type.
            """) 
        files = {
            'r' : BytesIO(write_to_buffer(r)), 
            'rvol' : BytesIO(write_to_buffer(rvol)), 
        }
    else :
        files = {
            'r' : BytesIO(write_to_buffer(r)), 
        }
    data = {'kwargs' : json.dumps(kwargs)}
    return sendRequest(url=url, headers=None, files=files, data=data)

def marginal(r: pd.DataFrame, weights: pd.DataFrame, **kwargs):
    url = SERVERROOT + '/risk/marginal'
    if not (
        isinstance(r, (pd.DataFrame, pd.Series)) and \
        isinstance(weights, (pd.DataFrame, pd.Series)) 
    ):
        return print(
        """You musst provide 'r', 'weights' in pandas.DataFrame/Series type.
        """) 
    files = {
        'r' : BytesIO(write_to_buffer(r)),
        'weights' : BytesIO(write_to_buffer(weights))
    }
    data = {'kwargs' : json.dumps(kwargs)}
    return sendRequest(url=url, headers=None, files=files, data=data)
