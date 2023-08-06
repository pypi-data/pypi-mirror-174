import requests
import json
import pickle
import os
import pandas as pd
import numpy as np
from ruamel import yaml

from ..VARS import *

__all__ = ['']


## create the console

from rich.console import Console
width = np.maximum(Console().width, 120)
print = Console(width = width).print



def login(username = None, password = None):
    """
    """
    data = {'username':username, 'password':password}
    try:
        res = requests.post(url= SERVERROOT+'/token', data=data)
        if res.status_code == 200:
            tokenvalue = json.loads(res.text)['access_token']
        else:
            return print(res.text)
    except Exception as e:
        return print("Authorization connection problem. ", e)

    try:
        tokenfile = '.fdatatoken.yaml'
        tokenpath = os.path.join(os.path.expanduser('~'), tokenfile)
        with open(tokenpath, "w", encoding="utf-8") as f:
            yaml.dump({'token':tokenvalue}, f, Dumper=yaml.RoundTripDumper)
        TOKEN['token'] = tokenvalue
        print('User authorized.')
        help()
    except yaml.YAMLError as e:
        print(e)
    except Exception as e:
        print(e)

def auth():
    """
    """
    for attemp in range(3):
        print("Please enter your user name and password for authentication.")
        username = input("Please input your user name: ")
        password = input("Please input your password: ")
        data = {'username':username, 'password':password}
        try:
            res = requests.post(url=SERVERROOT+'/token', data=data)
            if res.status_code == 200:
                tokenvalue = json.loads(res.text)['access_token']
                break
            else:
                print("User not authorized. Incorrect username or password.")
        except Exception as e:
            print("Authorization connection problem. ", e)
    else:
        raise ValueError("Check your username and password, and call function again.")

    try:
        tokenfile = '.fdatatoken.yaml'
        tokenpath = os.path.join(os.path.expanduser('~'), tokenfile)
        with open(tokenpath, "w", encoding="utf-8") as f:
            yaml.dump({'token':tokenvalue}, f, Dumper=yaml.RoundTripDumper)
        TOKEN['token'] = tokenvalue
        print('User authorized.')
    except yaml.YAMLError as e:
        print(e)
    except Exception as e:
        print(e)

def help(module: str = ''):
    url = SERVERROOT + '/help/{0}'.format(module)
    res = sendRequest(url=url)
    if res != None:
            print(res)  

def getAndSetToken():
    if TOKEN['token'] is None:
        try:
            tokenfile = '.fdatatoken.yaml'
            tokenpath = os.path.join(os.path.expanduser('~'), tokenfile)
            with open(tokenpath, "r", encoding="utf-8") as f:
                token = yaml.safe_load(f)['token']
            return token
        except FileNotFoundError:
            print("Authentication recreating...")
        except yaml.YAMLError as e:
            print(e)
        auth()  # take authentication
        token = TOKEN['token']
    else:
        token = TOKEN['token']
    return token

def readToLocalLang():
    if LANG['lang'] is None:
        for name in ["LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"]:
            if name in os.environ and os.environ[name]:
                LANG['lang'] = os.environ[name]
                break
    return LANG['lang']

def setLang(lang=None):
    if lang is None:
        for name in ["LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"]:
            if name in os.environ and os.environ[name]:
                lang = os.environ[name]
                break
    LANG.update(lang=lang)
    print('Current language is:', lang)

def showLang():
    print(LANG['lang'])

def makeTokenHeader(token:str):
    headers = {'Authorization':'Bearer {0}'.format(token)}
    return headers

def makeLangHeader(lang:str):
    headers = {'accept-language' : lang}
    return headers

def sendRequest(url, headers=None, kwargs=None, files=None, data=None):
    tmpheader = {}
    tmpheader.update(makeTokenHeader(getAndSetToken())) # update token header
    tmpheader.update(makeLangHeader(readToLocalLang())) # update lang header
    # update header to request
    if headers is None:
        headers = tmpheader
    else:
        headers.update(tmpheader)
        
    try:
        if files:
            res = requests.post(url=url, headers=headers, data=data, files=files)
        else:
            res = requests.post(url=url, headers=headers, json=kwargs)
    except Exception as e:
        return print(e)
    if res.status_code == 200:
        content = pickle.loads(res.content)
        return print(content) if type(content)==str else content
    if res.status_code == 401:
        print("Authentication has expired.")
        auth() # auth and send request again
        headers.update(makeTokenHeader(TOKEN['token']))
        try:
            if files:
                res = requests.post(url=url, headers=headers, data=data, files=files)
            else:
                res = requests.post(url=url, headers=headers, json=kwargs)
        except Exception as e:
            return print(e)
        if res.status_code == 200:
            content = pickle.loads(res.content)
            return print(content) if type(content)==str else content
        else:
            print(res.text)
    else:
        print(res.text)

def sendRequestGetText(url, headers=None, kwargs=None, files=None, data=None):
    tmpheader = {}
    tmpheader.update(makeTokenHeader(getAndSetToken())) # update token header
    tmpheader.update(makeLangHeader(readToLocalLang())) # update lang header
    # update header to request
    if headers is None:
        headers = tmpheader
    else:
        headers.update(tmpheader)

    try:
        if files:
            res = requests.post(url=url, headers=headers, data=data, files=files)
        else:
            res = requests.post(url=url, headers=headers, json=kwargs)
    except Exception as e:
        return print(e)
    if res.status_code == 200:
        content = json.loads(res.text)
        return content
    if res.status_code == 401:
        print("Authentication has expired.")
        auth() # auth and send request again
        headers.update(makeTokenHeader(TOKEN['token']))
        try:
            if files:
                res = requests.post(url=url, headers=headers, data=data, files=files)
            else:
                res = requests.post(url=url, headers=headers, json=kwargs)
        except Exception as e:
            return print(e)
        if res.status_code == 200:
            content = json.loads(res.text)
            return content
        else:
            print(res.text)
    else:
        print(res.text)

def write_to_buffer(df, key="/data"):
    with pd.HDFStore(
            "data.h5", mode="a", driver="H5FD_CORE",
            driver_core_backing_store=0
            ) as out:
        out[key] = df
        return out._handle.get_file_image()

def df_to_numpy(df):
    try:
        shape = [len(level) for level in df.index.levels]
    except AttributeError:
        shape = [len(df.index)]
    ncol = df.shape[-1]
    if ncol > 1:
        shape.append(ncol)
    return df.to_numpy().reshape(shape)

