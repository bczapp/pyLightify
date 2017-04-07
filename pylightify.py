import requests
import json
import re

def _url(path):
    return 'https://eu.lightify-api.org/lightify/services' + path

def post_gettoken(username, password, serialnumber):
    headers = {'content-type': 'application/json'}
    payload = {"username": username, "password": password, "serialNumber": serialnumber}
    resp = requests.post(url=_url('/session'), json=payload, headers=headers)
    gettoken_dict = json.loads(resp.text)
    if str(resp.status_code) == "200":
        return gettoken_dict['securityToken']
    else:
        return "ERROR" + str(resp.status_code)

def get_devices(at):
    headers = {'Authorization': at}
    resp = requests.get(_url('/devices'), headers=headers)
    devices_dict = json.loads(resp.text)
    if str(resp.status_code) == "200":
        return devices_dict
    else:
        return "ERROR" + str(resp.status_code)

def get_turngroupon(at, groupid):
    headers = {'Authorization': at}
    resp = requests.get(_url('/group/set?idx=' + groupid + '&onoff=1'), headers=headers)
    resp_dict = json.loads(resp.text)
    if str(resp.status_code) == "200":
        return resp_dict
    else:
        return "ERROR" + str(resp.status_code)

def get_turngroupoff(at, groupid):
    headers = {'Authorization': at}
    resp = requests.get(_url('/group/set?idx=' + groupid + '&onoff=0'), headers=headers)
    resp_dict = json.loads(resp.text)
    if str(resp.status_code) == "200":
        return resp_dict
    else:
        return "ERROR" + str(resp.status_code)

def get_turnallon(at):
    headers = {'Authorization': at}
    resp = requests.get(_url('/device/all/set?onoff=1'), headers=headers)
    resp_dict = json.loads(resp.text)
    if str(resp.status_code) == "200":
        return resp_dict
    else:
        return "ERROR" + str(resp.status_code)

def get_turnalloff(at):
    headers = {'Authorization': at}
    resp = requests.get(_url('/device/all/set?onoff=0'), headers=headers)
    resp_dict = json.loads(resp.text)
    if str(resp.status_code) == "200":
        return resp_dict
    else:
        return "ERROR" + str(resp.status_code)

def get_apiversion(at):
    headers = {'Authorization': at}
    resp = requests.get(_url('/version'), headers=headers)
    resp_dict = json.loads(resp.text)
    if str(resp.status_code) == "200":
        return resp_dict
    else:
        return "ERROR" + str(resp.status_code)