from typing import Optional, Dict, Union, List, Literal, Tuple

from ..utils import utils as __utils


def info():
    url = __utils.SERVERROOT + '/query/index_info'
    kwargs = dict()
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)

def daily(
    instrumentid: Union[str, List[str], Tuple[str]],
    from_date: str = None,
    to_date: str = None,
    complete: bool = True
):
    url = __utils.SERVERROOT + '/query/index_daily'
    kwargs = dict(
        instrumentid=instrumentid,
        from_date=from_date,
        to_date=to_date,
        complete=complete
    )
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)
