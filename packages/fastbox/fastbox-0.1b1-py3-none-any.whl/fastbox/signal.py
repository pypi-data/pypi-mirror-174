from functools import wraps, partial
import pandas as pd

from typing import Union, Optional, Literal, Dict, List

from pydantic import PositiveInt, constr, PositiveFloat, conint, confloat

from .pydantic.models import Dist, DistModel, NpPeriod, NpPeriodModel

from io import BytesIO
import numpy as np
import pandas as pd
import json
from rich import print
# TODO:
# rich print

from .utils.utils import SERVERROOT, TOKEN, LANG
# from ..utils.utils import 
from .utils.utils import sendRequest, sendRequestGetText
from .utils.utils import write_to_buffer

__all__ = ['']

def help(method: str = ''):
    url = SERVERROOT + '/signal/help/{0}'.format(method)
    res = sendRequest(url=url)
    if res != None:
            print(res)  


def ret(df: pd.DataFrame, window: Optional[PositiveInt] = 1):
    """Computing rolling returns

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    window:             (df[t]-df[t-window])/df[t-window]

    Returns
    -------
    Returns (droping the first window steps)
    """    
    return __operation(_func_name_ = 'ret', df = df, window = window)

def lret(df: pd.DataFrame, window: Optional[PositiveInt] = 1):
    """Computing rolling log returns

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    window:             ln(df[t]/df[t-window])

    Returns
    -------
    Log returns (droping the first window steps)
    """
    return __operation('lret', df = df, window = window)

def sma(df: pd.DataFrame, window: Optional[PositiveInt] = 1):
    """Getting the (simple) moving average

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    window:             mean(df[t], ... , df[t-window +1])

    Returns
    -------
    Moving average (droping the first window steps)
    """
    return __operation('sma', df = df, window = window)

def wma(df: pd.DataFrame, window: Optional[PositiveInt] = 1):
    """Getting the weighted moving average

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    window :            wma[t] = (window * df[t] + ... + df[t-window + 1])/(window + ... 2 + 1)

    Returns
    -------
    Weighted moving average (droping the first window steps)

    """
    return __operation('wma', df = df, window = window)

def ema(df: pd.DataFrame, coef: Optional[confloat(gt=0, lt=1)] = 0.2):
    """Getting the exponential moving average

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    coef:               eav[t] = coef * df[t-1] + (1-coef) * eav[t-1]

    Returns
    -------
    Exponential moving average
    """
    return __operation('ema', df = df, coef = coef)

def mu(df: pd.DataFrame, window: Optional[conint(ge =2)] = 5, as_returns: Optional[bool] = False):
    """Getting the rolling mean return

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    window :            length of the rolling
    as_returns:         bool: false (default) will compute returns

    Returns
    -------
    rolling mean returns
    """
    return __operation('mu', df = df, window = window, as_returns = as_returns)

def vol(df: pd.DataFrame, window: Optional[conint(ge =5)] = 5, as_returns: Optional[bool] = False):
    """Getting the rolling volatility

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    window :            length of the rolling
    as_returns:         bool: false (default) will compute returns

    Returns
    -------
    rolling volatility
    """
    return __operation('vol', df = df, window = window, as_returns = as_returns)

def corr(df: pd.DataFrame, window: Optional[conint(ge =5)] = 30, as_returns: Optional[bool] = False):
    """Getting the rolling correlation (empirical)

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    window :            length of the rolling
    as_returns:         bool: false (default) will compute returns

    Returns
    -------
    rolling (empirical) pearson correlation
    """
    return __operation('corr', df = df, window = window, as_returns = as_returns)

def cov(df: pd.DataFrame, window: Optional[conint(ge =5)] = 30, as_returns: Optional[bool] = False):
    """Getting the rolling covariance (empirical)

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    window :            length of the rolling
    as_returns:         bool: false (default) will compute returns

    Returns
    -------
    rolling (empirical) covariance
    """
    return __operation('cov', df = df, window = window, as_returns = as_returns)

def muvol(df: pd.DataFrame, window: Optional[conint(ge =5)] = 30, as_returns: Optional[bool] = False):
    """Getting the rolling mean returns and volatility

    Parameters
    ----------
    df :                Series/Dataframe with `date` as coordinate.
    window :            length of the rolling
    as_returns:         bool: false (default) will compute returns

    Returns
    -------
    rolling (empirical) mean returns and volatility
    """
    return __operation('muvol', df = df, window = window, as_returns = as_returns)

def mucov(df: pd.DataFrame, window: Optional[conint(ge =5)] = 30, as_returns: Optional[bool] = False):
    """Getting the rolling mean returns and covariance

    Parameters
    ----------
    df :                Dataframe with `date` as coordinate and more than two columns
    window :            length of the rolling
    as_returns:         bool: false (default) will compute returns

    Returns
    -------
    rolling (empirical) mean returns and covariance
    """

    return __operation('mucov', df = df, window = window, as_returns = as_returns)

def arch(
        df: pd.DataFrame,
        mean: Optional[str] = 'Constant',
        lags: Optional[Union[conint(ge=0), List[conint(ge = 0)]]] = 0,
        vol: Optional[str] = 'Garch',
        p: Optional[PositiveInt] = 1,
        o: Optional[conint(ge=0)] = 0,
        q: Optional[PositiveInt] = 1,
        power: Optional[float] = 2.0,
        dist: Optional[Dist] = DistModel(),
        horizon: Optional[PositiveInt] = 1,     
        complete: Optional[bool] = False,
        min_num_obs: Optional[conint(gt = 200)] = 520,
        update_obs: Optional[conint(ge =5, lt = 200)] = 40,
        as_returns: Optional[bool] = False):
    """Use (g)arch model to provide a rolling prediction of mean and volatility
    The model is recalibrated every update_obs steps, necessitate min_num_obs.
    Adopt the same notation as the arch module from Kevin Sheppard https://github.com/bashtage/arch
    Special implementation that does not cover the original arch module (see documentation)

    Parameters
    ----------
    df:                 Series/Dataframe of values
    mean:               'Constant' (default), 'Zero', 'AR' (autoregression)
    lags:               Number of lags if mean is not constant of zero (or a list thereof)
    vol:                'Garch' (default), 'Arch', 'Tarch', 'Egarch'
    p:                  p garch order (1)
    o:                  differentiation order (0)
    q:                  q garch order (1)
    power:              power of volatility (2.0),
    dist:               distribution used `normal` (default) or `T`
    horizon:            number of steps to predict (1)
    complete:           if additional informations are returned such as calibration results (disabled for now)
    min_num_obs:        minimum number of observation necessary for the first prediction
    update_obs:         frequency at which the model is recalibrated
    as_returns:         bool: false (default) will compute returns

    Returns
    -------
    returns a rolling (g)arch prediction of mean and volatility
    """
    return __operation(
            'arch_muvol',
            df = df,
            mean = mean,
            lags = lags,
            vol=vol,
            p = p,
            o = o,
            q = q,
            power = power,
            dist = dist.dict(),
            horizon = horizon,
            complete = complete,
            min_num_obs = min_num_obs,
            update_obs = update_obs,
            as_returns = as_returns
            )

def vector_ar(df: pd.DataFrame, period: Optional[NpPeriod] = None, maxlags: Optional[PositiveInt] = 5, ic: Optional[str] = 'aic', as_returns: Optional[bool] = False):
    """Use Vector Autoregression to predict one step mean returns
    We use the same notations as the VAR of statsmodels with adapted implementation for rolling performance.
    Not all the functionalities of the statsmodel class are provided

    Parameters
    ----------
    df:                 Dataframe of values
    period:             Set the period at which the model is updated
    maxlags:            Maximum of lags to allow for the search of the optimal number of lags
    ic:                 Methods against which choosing the optimal number of lags
    as_returns:         bool: false (default) will compute returns

    Returns
    -------
    Returns a one step vector mean prediction of returns.
    """
    return __operation('vector_ar_mu', df = df, period = period, maxlags = maxlags, ic = ic, as_returns = as_returns)

def mgarch(
        df: pd.DataFrame,
        period: Optional[NpPeriod] = None,
        vol: Optional[str] = 'Garch',
        p: Optional[PositiveInt] = 1,
        o: Optional[conint(ge=0)] = 0,
        q: Optional[PositiveInt] = 1,
        power: Optional[float] = 2.0,
        as_returns: Optional[bool] = False
        ):
    """Use a (DCC) multivariate garch model to predict one step mean returns (using VAR) covariance and correlation.
    As for now, only multivariate normal distribution is available.

    Parameters
    ----------
    df:                 Series/Dataframe of values
    period:             Period from which to where the model should predict
    vol:                'Garch' (default), 'Arch', 'Tarch', 'Egarch'
    p:                  p garch order (1)
    o:                  differentiation order (0)
    q:                  q garch order (1)
    power:              power of volatility (2.0),
    as_returns:         bool: false (default) will compute returns

    Returns
    -------
    return a one step mean (VAR model) covariance and correlation prediction according to (DCC) mgarch model
    """
    return __operation('mgarch_mucov', df = df, period = period, vol = vol, p = p, o = o, q = q, power = power, as_returns = as_returns)

def __operation(_func_name_: str, **kwargs):
    url = SERVERROOT + '/signal/{0}'.format(_func_name_)
    for k in kwargs.copy():
        if isinstance(kwargs[k], (pd.DataFrame, pd.Series)):
            df = kwargs.pop(k)
            break
    else:
        return print(
            """Pandas DataFrame/Series required to compute signal.
               \nUse signal.help("<method>") for more info.
            """)
    files = {'file' : BytesIO(write_to_buffer(df))}
    data = {'kwargs' : json.dumps(kwargs)}
    return sendRequest(url=url, headers=None, files=files, data=data)


def __getattr__(_func_name_: str):
    return partial(__operation, _func_name_)
