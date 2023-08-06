from typing import Optional, Dict, Union, List, Literal, Tuple

from ..utils import utils as __utils


def daily(
    maturity: float = None,
    from_date: str = None,
    to_date: str = None,
    date: str = None,
):
    url = __utils.SERVERROOT + '/query/shibor_daily'
    kwargs = dict(
        maturity=maturity,
        from_date=from_date,
        to_date=to_date,
        date=date,
    )
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)