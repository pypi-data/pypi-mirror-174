from typing import Literal
import pickle
import json
from .utils import utils as __utils

def _modelrequest(**kwargs):
    url = __utils.SERVERROOT + '/model/getmodel'
    print(kwargs)
    return __utils.sendRequest(url=url, headers=None, kwargs=kwargs)



from typing import Union, Dict
from pydantic import create_model, validate_arguments




@validate_arguments
def signalModel(
        name: str,
        **kwargs):
    kwargs.update({'name': name})
    url = __utils.SERVERROOT + '/model/signalmodel'
    model = __utils.sendRequest(url=url, kwargs=kwargs)
    return model

@validate_arguments
def riskModel(
        name: Literal['emp_risk', 'empRisk', 'risk', 'anaRisk'],
        **kwargs):
    """Receive a signal name and generate the corresponding method arguments as a pydantic model

    Parameters
    ----------
    name:               Name of the function to call

    Returns
    -------
    pydantic model about the different arguements of that method
    """
    method = {'name': name} | kwargs
    modeldict = _modelrequest(model = 'Risk', method = method)
    return modeldict


@validate_arguments
def tsModel(
        name: Literal['muvol', 'arch_muvol'],
        **kwargs):
    """Receive a signal name and generate the corresponding method arguments as a pydantic model

    Parameters
    ----------
    name:               Name of the function to call

    Returns
    -------
    pydantic model about the different arguements of that method
    """
    method = {'name': name} | kwargs
    modeldict = _modelrequest(model = 'Tsa', method = method)
    return modeldict


