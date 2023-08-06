from typing import Optional, Dict, Union, List, Literal, Tuple

from ..utils import utils as __utils


def info(
    instrumentid: Union[str, List[str], Tuple[str]] = None,
    underlyingid: Union[str, List[str], Tuple[str]] = None,
    exchange: Literal['SHFE', 'INE', 'DCE', 'CZCE', 'CFFEX'] = None,
    from_date: str = None,
    to_date: str = None
):
    url = __utils.SERVERROOT + '/query/future_info'
    kwargs = dict(
        instrumentid=instrumentid,
        underlyingid=underlyingid,
        exchange=exchange,
        from_date=from_date,
        to_date=to_date
    )
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)

def daily(
    instrumentid: Union[str, List[str], Tuple[str]] = None,
    underlyingid: Union[str, List[str], Tuple[str]] = None,
    from_date: str = None,
    to_date: str = None,
    date: str = None,
    complete: bool = True
):
    url = __utils.SERVERROOT + '/query/future_daily'
    kwargs = dict(
        instrumentid=instrumentid,
        underlyingid=underlyingid,
        from_date=from_date,
        to_date=to_date,
        date=date,
        complete=complete
    )
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)

def lv1(
    instrumentid: str,
    from_date: str = None,
    to_date: str = None,
    date: str = None
):
    url = __utils.SERVERROOT + '/query/future_lv1'
    kwargs = dict(
        instrumentid=instrumentid,
        from_date=from_date,
        to_date=to_date,
        date=date,
    )
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)

def lv2(
    instrumentid: str,
    from_date: str = None,
    to_date: str = None,
    date: str = None
):
    url = __utils.SERVERROOT + '/query/future_lv2'
    kwargs = dict(
        instrumentid=instrumentid,
        from_date=from_date,
        to_date=to_date,
        date=date,
    )
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)