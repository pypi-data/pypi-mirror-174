from functools import wraps, partial
from io import BytesIO
from rich import print
import numpy as np
import pandas as pd
import json
from datetime import datetime

from numba import njit, jit

from typing import Optional, Dict, Union, List, Literal, Tuple
from pydantic import validate_arguments, BaseModel, conint, confloat
from pydantic import PositiveInt, constr, PositiveFloat

from .models import signalModel
from .pydantic.models import StrategyModel, NpDatetime, NpArray
from .pydantic.models import Dist, DistModel, NpPeriod, NpPeriodModel
from .pydantic.models import TCostModel

from .utils.utils import SERVERROOT, TOKEN, LANG, print

# from ..utils.utils import 
from .utils.utils import sendRequest, sendRequestGetText
from .utils.utils import write_to_buffer, df_to_numpy
from .utils import utils_plotting as plt

__all__ = ['Portfolio']


def _strategy_run(
        fun,
        T: int,
        d: int,
        instrumentid = NpArray[str],
        *args,
        window: Optional[int] = None,
        selfw: bool = False,
        vectorize: bool = False):
    """Function to run the strategy

    Parameters
    ----------
    fun :               Function returning the strategy -> met return a numpy array. (takes exclusively time series as args)
    T :                 Length of the time series
    d :                 Dimension of the output
    args :              Arguments for the function numpy arrays of size (T, xx)
    window = 0:            How much in the past do we look back
    selfw = False:      whether to use previous decisions (needs window at least >=1)
    vectorize = False : whether to use jit

    Returns
    -------
    numpy array of size (T-window, d)
    """
    
    # get the list of indices where args is a time series

    # now we go through the different methods
    if window is None:
        window = 0
    if not vectorize:
        w = np.zeros((T, len(instrumentid)))
        if not selfw:
            # no optimization, we run a standard loop
            # no selfw so not in the loop
            for t in range(window, T):
                argu = []
                for idx in range(len(args)):
                    argu.append(args[idx][t-window:t+1, :].squeeze())
                w[t, :] = fun(instrumentid, *tuple(argu))
        else:
            for t in range(window, T):
                argu = []
                for idx in range(len(args)):
                    argu.append(args[idx][t-window:t+1, :].squeeze())
                w[t, :] = fun(instrumentid, *tuple(argu + [w[t-window:t, :]]))
    else:
        w = np.zeros((T,len(instrumentid)))
        # we vectorize the function
        fun_jit = njit()(fun)
        if not selfw:
            @jit
            def funloop(*args):
                for t in range(window, T):
                    argu = (args[idx][t-window:t+1, :] for idx in range(len(idx)))
                    w[t, :] = fun_jit(instrumentid, *argu)
            funloop(*args)
    return w[window:, :]



class Portfolio:
    __PORT_ID = None

# ---------- for local test use -------
    def ds(self):
        url = SERVERROOT + '/portfolio/ds'
        headers = {'portfolio_id' : self.__PORT_ID}
        return sendRequest(url=url, headers=headers)
# -------------------------------------

    @classmethod
    def help(cls, method=''):
        url = SERVERROOT + '/portfolio/help/{0}'.format(method)
        return sendRequest(url=url)

    def __init__(self, 
        instrumentid : Union[str, List[str], Tuple[str]],
        name : Optional[str] = 'Portfolio',
        description : Optional[str] = 'New Portfolio ' + datetime.now().strftime("%Y-%m-%d"),
        from_date :  Optional[NpDatetime] = None,
        to_date : Optional[NpDatetime] = None,
        tcosts : Optional[TCostModel] = TCostModel(fees = 0.0002, tax = 0.001).dict(),
    ):
        url = SERVERROOT + '/portfolio/init'
        data = {'kwargs':dict(
                            instrumentid=instrumentid,
                            name = name,
                            description = description,
                            from_date = from_date,
                            to_date = to_date,
                            tcosts = tcosts)
        }
        self.__PORT_ID = sendRequestGetText(url=url, kwargs=data, headers=None)
        if self.__PORT_ID:
            self.signal = _Signal(self.__PORT_ID)
            self.strategy = self.__inner_Strategy()(self.__PORT_ID)
            self.risk = _Risk(self.__PORT_ID)
            print("Portfolio initialized")
            self.info()


    def push(self, df:pd.DataFrame, name:str, description:str = None, typus:str = 'input'):
        url = SERVERROOT + '/portfolio/push'
        headers = {'portfolio_id' : self.__PORT_ID}
        if not isinstance(df, (pd.DataFrame, pd.Series)):
            return print(
            """You musst provide 'r' in pandas.DataFrame/Series type.
            """) 
        files = {'df' : BytesIO(write_to_buffer(df))}
        kwargs = dict(name=name, description=description, typus=typus)
        data = {'kwargs' : json.dumps(kwargs)}
        return sendRequest(url=url, headers=headers, files=files, data=data)

    def info(self, complete: bool = False, typus: str = None, name: str = None):
        url = SERVERROOT + '/portfolio/info'
        headers = {'portfolio_id' : self.__PORT_ID}
        kwargs = dict(complete=complete, typus=typus, name=name)
        data = {'kwargs':kwargs}
        result = sendRequest(url=url, headers=headers, kwargs=data)
        print(result)

    def pull(
        self,
        name : Union[str, List[str], Dict[str, Union[str, List[str]]]],
        from_date : Optional[NpDatetime] = None,
        to_date: Optional[NpDatetime] = None,
        freq: Optional[Literal['W', 'M', 'Q', 'Y']] = None
    ):
        url = SERVERROOT + '/portfolio/pull'
        headers = {'portfolio_id' : self.__PORT_ID}
        kwargs = dict(name=name, from_date=from_date, to_date=to_date, freq=freq)
        data = {'kwargs':kwargs}
        return sendRequest(url=url, headers=headers, kwargs=data)

    def pullcoords(
        self,
        name: Optional[str] = None,
        from_date : Optional[NpDatetime] = None,
        to_date: Optional[NpDatetime] = None,
        freq: Optional[Literal['W', 'M', 'Q', 'Y']] = None
    ):
        url = SERVERROOT + '/portfolio/pullcoords'
        headers = {'portfolio_id' : self.__PORT_ID}
        kwargs = dict(name=name, from_date=from_date, to_date=to_date, freq=freq)
        data = {'kwargs':kwargs}
        return sendRequest(url=url, headers=headers, kwargs=data)

    def query(
        self,
        asset : Literal['stock', 'index', 'bond'],
        instrumentid : str,
        name : str = None,
        description : str = None,
    ):
        url = SERVERROOT + '/portfolio/query'
        headers = {'portfolio_id' : self.__PORT_ID}
        kwargs = dict(asset=asset, instrumentid=instrumentid, name=name, description=description)
        data = {'kwargs':kwargs}
        return sendRequest(url=url, headers=headers, kwargs=data)

    def delete(self, name : str):
        url = SERVERROOT + '/portfolio/delete'
        headers = {'portfolio_id' : self.__PORT_ID}
        data = {'kwargs' : dict(name=name)}
        return sendRequest(url=url, headers=headers, kwargs=data)

    def set_benchmark(self, benchmark: Union[float, str] = 'bond'):
        url = SERVERROOT + '/portfolio/set_benchmark'
        headers = {'portfolio_id' : self.__PORT_ID}
        data = {'kwargs' : dict(benchmark=benchmark)}
        return sendRequest(url=url, headers=headers, kwargs=data)

    @property
    def stocks(self):
        return self.pull(name='stocks')

    @property
    def bond(self):
        return self.pull(name='bond')

    
    def __inner_Strategy(self):
        outer_obj = self

        class _Strategy:
            def __init__(self, PORT_ID):
                self.__PORT_ID = PORT_ID
                self.outer_obj = outer_obj

            def process(
                    self,
                    fun,
                    name: str,
                    strategy_type: Optional[str] = 'nshares',
                    description: Optional[str] = None,
                    strategy_args: Optional[StrategyModel] = None,
                    input_var: Union[str, List[str], Dict] = None,
                    window: Optional[conint(ge=0, le = 7)] = None,
                    selfw: Optional[bool] = False,
                    vectorize: Optional[bool] = False,
                    from_date: Optional[NpDatetime] = None,
                    to_date: Optional[NpDatetime] = None,
                    freq: Optional[Literal['W', 'M', 'Q', 'Y']] = None,
                    **kwargs
                    ):
                """Processing a strategy. Name and strategy type are required. fun can be a function (-> in that case process) or dataframe (-> in that case upload and process)

                Parameters
                ----------
                fun:            function or dataframe
                name:           name of the strategy, required
                strategy_type:  strategy type
                description:    Descirption of the strategy
                input_var:     input variables from the online portfolio
                window:         how many steps backward the strategy is looking for the variable (default is markovian = 0)
                freq:           frequency of updating (default is none, can be week 'W', month 'M', quarter 'Q' or year 'Y' (first business day of each)
                selfw:          boolean if the strategy relies on itself (default is False)
                vectorize:      if the processing should take advantage of numba (if true, the strategy must comply numba's requirement)
                from/to_date:   starting/end date of the processing (if nothing, it takes the intersection of the date availability of each variables
                **kwargs:       additional arguments for the function (for optimization purposes for instance)
                
                Return
                ------
                a dataframe with the processed strategy, uploaded and processed to the server.
                """
                if strategy_args is None:
                    sargs = StrategyModel(input_var = input_var, window = window, selfw = selfw, vectorize = vectorize, from_date = from_date, to_date = to_date, freq = freq)
                else:
                    sargs = strategy_args
                if callable(fun):
                    # we have a function, we first put the kwargs 
                    if kwargs:
                        strategy_fun = partial(fun, kwargs)
                    dfnames = None
                    dfvarnames = None
                    # we then validate input if strategy_args is None
                    #if strategy_args is None:
                    #else:
                    #    sargs = strategy_args

                    # we prepare the dataframes to receive da
                    dfnames = None
                    dfvarnames = None
                    if sargs.input_var is not None:
                        dfnames = [key for key in sargs.input_var]

                    result = None
                    # get the instrumentids
                    instrumentid = self.outer_obj.pullcoords(name = 'instrumentid')
                    idxinstrumentid = pd.Index(instrumentid, name= 'instrumentid')
                    idx = pd.Index(self.outer_obj.pullcoords(name = 'date', from_date = sargs.from_date, to_date = sargs.to_date, freq = sargs.freq), name = 'date')
                    # create the function to be executed
                    if sargs.vectorize:
                        # For the moment we can not partial functions so no kwargs
                        if len(kwargs) >0:
                            print("For Numba capacity, kwargs is not possible. Falling back to non vectorized.")
                            sargs.vectorize = False
                        else:
                            execfun = fun
                    if not sargs.vectorize:
                        execfun = partial(fun, **kwargs)
                    if dfnames is not None:
                        df = self.outer_obj.pull(name = sargs.input_var, from_date = sargs.from_date, to_date = sargs.to_date, freq = sargs.freq)
                        if not isinstance(df, dict):
                            # there is a single df
                            df = {dfnames[0] : df}
                        idx = df[dfnames[0]].index.get_level_values(level='date').drop_duplicates(keep = 'first')

                    # prepare the objective dataframe
                    objdf = pd.DataFrame(np.zeros(len(idx)), index = idx).sort_index()
                    T = len(objdf.index)
                    d = len(idxinstrumentid)
                    # we slice the dataframe according to swindow
                    if isinstance(sargs.window, int):
                        if sargs.window >0:
                            objdf = objdf.iloc[sargs.window:]
                    # prepare the arguments for the function
                    argu = []
                    if dfnames is not None:
                        for key in df:
                            for col in df[key].columns:
                                argu.append(df_to_numpy(df[key][[col]]))
                    objdf = pd.DataFrame(
                            _strategy_run(
                            execfun,
                            T,
                            d,
                            instrumentid,
                            *tuple(argu),
                            window = sargs.window,
                            selfw=sargs.selfw,
                            vectorize=sargs.vectorize
                            ), index = objdf.index, columns= idxinstrumentid)
                    # now we can send the data to the server
                    DICT = {
                            'df':               objdf,
                            'name':             name,
                            'strategy_type':    strategy_type,
                            'description':      description,
                            'input_var':        sargs.input_var,
                            'from_date':        sargs.from_date,
                            'to_date':          sargs.to_date,
                            'freq':             sargs.freq
                            }
                else:
                    # this is a dataframe
                    DICT = {
                            'df':               fun,
                            'name':             name,
                            'strategy_type':    strategy_type,
                            'description':      description,
                            'input_var':        sargs.input_var,
                            'from_date':        sargs.from_date,
                            'to_date':          sargs.to_date,
                            'freq':             sargs.freq
                            }
                # now we upload the data to the server and get P as feedback
                url = SERVERROOT + '/portfolio/strategy/process'
                headers = {'portfolio_id' : self.__PORT_ID}
                files = {'df' : BytesIO(write_to_buffer(DICT.pop('df')))}
                data = {'kwargs' : json.dumps(DICT)}
                return sendRequest(url=url, headers=headers, files=files, data=data)

            def metrics(
                    self,
                    strategy_name: str,
                    from_date: Optional[NpDatetime] = None,
                    to_date: Optional[NpDatetime] = None,
                    freq: Optional[Literal['W', 'M', 'Q', 'Y']] = 'Y',
                    metrics : Optional[List[str]] = ['performance', 'mret', 'mvol', 'maxdropdown', 'sharperatio', 'sortinoratio'],
                    report: Optional[bool] = True,
                    benchmark: Optional[bool] = True,
                    ):
                url = SERVERROOT + '/portfolio/strategy/metrics'
                headers = {'portfolio_id' : self.__PORT_ID}
                data = {
                        'kwargs': {
                            'strategy_name':    strategy_name,
                            'from_date':        from_date,
                            'to_date':          to_date,
                            'freq':             freq,
                            'metrics':          metrics,
                            'report':           report,
                            'benchmark':        benchmark
                            }
                        }
                return sendRequest(url=url, headers=headers, kwargs=data)

            def report(
                    self,
                    strategy_names: Union[str, List[str]],
                    from_date: Optional[NpDatetime] = None,
                    to_date: Optional[NpDatetime] = None,
                    freq: Optional[Literal['W', 'M', 'Q', 'Y']] = 'Y',
                    metrics : Optional[List[str]] = ['performance', 'mret', 'mvol', 'maxdropdown', 'sharperatio', 'sortinoratio'],
                    report: Optional[bool] = True,
                    benchmark: Optional[bool] = False,
                    costs: Optional[bool] = True,
                    cash: Optional[bool] = False,
                    alpha: Optional[confloat(gt = 0, lt = 1)] = 0.01,
                    data: Optional[bool] = False
                    ):
                if isinstance(strategy_names, str):
                    strategy_names = [strategy_names]

                url = SERVERROOT + '/portfolio/strategy/report'
                headers = {'portfolio_id' : self.__PORT_ID}
                data = {
                        'kwargs': {
                            'strategy_names':   strategy_names,
                            'from_date':        from_date,
                            'to_date':          to_date,
                            'freq':             freq,
                            'metrics':          metrics,
                            'benchmark':        benchmark,
                            'costs':            costs,
                            'alpha':            alpha
                            }
                        }
                result = sendRequest(url=url, headers=headers, kwargs=data)

                # we first reshape the dataframes in a meaningfull way
                if len(strategy_names)>1:
                    result['value_cost_risk'] = result['value_cost_risk'].unstack()
                # we got the results
                # 1- We print the tables
                # 2- We plot the data
                # 3- if data = True, we return the data, if not we just print
                if 'fig_performance' in result:
                    plt.iplot(result['fig_performance'])
                if 'fig_metric' in result:
                    plt.iplot(result['fig_metric'])
                if 'fig_returns' in result:
                    plt.iplot(result['fig_returns'])

                if len(strategy_names)>1:
                    for strategy_name in strategy_names:
                        print(result['metric_table'][strategy_name])
                else:
                    print(result['metric_table'])
            
                if data:
                    return result
                else:
                    return ''
        return _Strategy



class _Signal:
    def __init__(self, PORT_ID):
        self.__PORT_ID = PORT_ID

    def __operation(self, _func_name_, **kwargs):
        url = SERVERROOT + '/portfolio/signal/{0}'.format(_func_name_)
        headers = {'portfolio_id' : self.__PORT_ID}
        data = {'kwargs' : kwargs}
        return sendRequest(url=url, headers=headers, kwargs=data)
    

    def ret(self, window: Optional[PositiveInt] = 1):
        """Computing rolling returns

        Parameters
        ----------
        window:             (df[t]-df[t-window])/df[t-window]

        Returns
        -------
        Returns (droping the first window steps)
        """    
        return self.__operation(_func_name_ = 'ret', window = window)

    def lret(self, window: Optional[PositiveInt] = 1):
        """Computing rolling log returns

        Parameters
        ----------
        window:             ln(df[t]/df[t-window])

        Returns
        -------
        Log returns (droping the first window steps)
        """
        return self.__operation('lret', window = window)

    def sma(self, window: Optional[PositiveInt] = 1):
        """Getting the (simple) moving average

        Parameters
        ----------
        window:             mean(df[t], ... , df[t-window +1])

        Returns
        -------
        Moving average (droping the first window steps)
        """
        return self.__operation('sma', window = window)

    def wma(self, window: Optional[PositiveInt] = 1):
        """Getting the weighted moving average

        Parameters
        ----------
        window :            wma[t] = (window * df[t] + ... + df[t-window + 1])/(window + ... 2 + 1)

        Returns
        -------
        Weighted moving average (droping the first window steps)

        """
        return self.__operation('wma', window = window)

    def ema(self, coef: Optional[confloat(gt=0, lt=1)] = 0.2):
        """Getting the exponential moving average

        Parameters
        ----------
        coef:               eav[t] = coef * df[t-1] + (1-coef) * eav[t-1]

        Returns
        -------
        Exponential moving average
        """
        return self.__operation('ema', coef = coef)

    def mu(self, window: Optional[conint(ge =2)] = 5, as_returns: Optional[bool] = False):
        """Getting the rolling mean return

        Parameters
        ----------
        window :            length of the rolling
        as_returns:         bool: false (default) will compute returns

        Returns
        -------
        rolling mean returns
        """
        return self.__operation('mu', window = window, as_returns = as_returns)

    def vol(self, window: Optional[conint(ge =5)] = 5, as_returns: Optional[bool] = False):
        """Getting the rolling volatility

        Parameters
        ----------
        window :            length of the rolling
        as_returns:         bool: false (default) will compute returns

        Returns
        -------
        rolling volatility
        """
        return self.__operation('vol', window = window, as_returns = as_returns)

    def corr(self, window: Optional[conint(ge =5)] = 30, as_returns: Optional[bool] = False):
        """Getting the rolling correlation (empirical)

        Parameters
        ----------
        window :            length of the rolling
        as_returns:         bool: false (default) will compute returns

        Returns
        -------
        rolling (empirical) pearson correlation
        """
        return self.__operation('corr', window = window, as_returns = as_returns)

    def cov(self, window: Optional[conint(ge =5)] = 30, as_returns: Optional[bool] = False):
        """Getting the rolling covariance (empirical)

        Parameters
        ----------
        window :            length of the rolling
        as_returns:         bool: false (default) will compute returns

        Returns
        -------
        rolling (empirical) covariance
        """
        return self.__operation('cov', window = window, as_returns = as_returns)

    def muvol(self, window: Optional[conint(ge =5)] = 30, as_returns: Optional[bool] = False):
        """Getting the rolling mean returns and volatility

        Parameters
        ----------
        window :            length of the rolling
        as_returns:         bool: false (default) will compute returns

        Returns
        -------
        rolling (empirical) mean returns and volatility
        """
        return self.__operation('muvol', window = window, as_returns = as_returns)

    def mucov(self, window: Optional[conint(ge =5)] = 30, as_returns: Optional[bool] = False):
        """Getting the rolling mean returns and covariance

        Parameters
        ----------
        window :            length of the rolling
        as_returns:         bool: false (default) will compute returns

        Returns
        -------
        rolling (empirical) mean returns and covariance
        """

        return self.__operation('mucov', window = window, as_returns = as_returns)

    def arch(
            self,
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
        return self.__operation(
                'arch_muvol',
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

    def vector_ar(
        self,
        period: Optional[NpPeriod] = None,
        maxlags: Optional[PositiveInt] = 5,
        ic: Optional[str] = 'aic',
        as_returns: Optional[bool] = False):
        """Use Vector Autoregression to predict one step mean returns
        We use the same notations as the VAR of statsmodels with adapted implementation for rolling performance.
        Not all the functionalities of the statsmodel class are provided

        Parameters
        ----------
        period:             Set the period at which the model is updated
        maxlags:            Maximum of lags to allow for the search of the optimal number of lags
        ic:                 Methods against which choosing the optimal number of lags
        as_returns:         bool: false (default) will compute returns

        Returns
        -------
        Returns a one step vector mean prediction of returns.
        """
        return self.__operation('vector_ar_mu', period = period, maxlags = maxlags, ic = ic, as_returns = as_returns)

    def mgarch(
            self,
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
        return self.__operation('mgarch_mucov', period = period, vol = vol, p = p, o = o, q = q, power = power, as_returns = as_returns)

class _Risk:
    def __init__(self, PORT_ID):
        self.__PORT_ID = PORT_ID

    def marginal(
            self,
            strategy_name: str,
            date : Optional[NpDatetime] = None,
            alpha: Optional[confloat(gt = 0, lt = 1)] = 0.01,
            dist: Optional[dict] = None,    
            method: Optional[dict] = None,
            data: Optional[bool] = False
            ):
        url = SERVERROOT + '/portfolio/risk/marginal'
        headers = {'portfolio_id' : self.__PORT_ID}
        data = {
                'kwargs': {
                    'strategy_name':   strategy_name,
                    'date':             date,
                    'alpha':            alpha,
                    'method':           method
                    }
                }
        result = sendRequest(url=url, headers=headers, kwargs=data)
        plt.iplot(result['figure_marginal_risk'])
        if data:
            return result
        else:
            pass
