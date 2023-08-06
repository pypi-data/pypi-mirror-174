from typing import Optional, Dict, Union, List, Literal, Tuple
from pydantic import validate_arguments, BaseModel, conint, confloat
from pydantic import PositiveInt, constr, PositiveFloat

from ..utils import utils as __utils

def info(
    instrumentid: Union[str, List[str], Tuple[str]] = None,
    name: Union[str, List[str], Tuple[str]] = None,
    fullname: Union[str, List[str], Tuple[str]] = None,
    enname: Union[str, List[str], Tuple[str]] = None
):
    url = __utils.SERVERROOT + '/query/stock_info'
    kwargs = dict(
        instrumentid=instrumentid,
        name=name,
        fullname=fullname,
        enname=enname
    )
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)

def daily(
    instrumentid: Union[str, List[str], Tuple[str]],
    from_date: str = None,
    to_date: str = None,
    idconvention: Literal['instrumentid', 'name'] = 'instrumentid',
    complete: bool = True
):
    url = __utils.SERVERROOT + '/query/stock_daily'
    kwargs = dict(
        instrumentid=instrumentid,
        from_date=from_date,
        to_date=to_date,
        idconvention=idconvention,
        complete=complete
    )
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)
