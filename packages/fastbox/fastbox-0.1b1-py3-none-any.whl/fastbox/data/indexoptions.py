from typing import Optional, Dict, Union, List, Literal, Tuple

from ..utils import utils as __utils


def info(
    instrumentid: Union[str, List[str], Tuple[str]] = None,
    underlyingid: Union[str, List[str], Tuple[str]] = None,
    type: Literal['P', 'C'] = None,
    from_date: str = None,
    to_date: str = None
):
    url = __utils.SERVERROOT + '/query/index_option_info'
    kwargs = dict(
        instrumentid=instrumentid,
        underlyingid=underlyingid,
        type=type,
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
    url = __utils.SERVERROOT + '/query/index_option_daily'
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
    url = __utils.SERVERROOT + '/query/index_option_lv1'
    kwargs = dict(
        instrumentid=instrumentid,
        from_date=from_date,
        to_date=to_date,
        date=date,
    )
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)