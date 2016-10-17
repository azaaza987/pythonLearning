import requests
import base64

requrl='http://192.168.0.1/'
username='admin'
password='111111'

cookies=dict(Authorization='Basic%20YWRtaW46MTExMTEx')

def login():
    r=requests.get(requrl,cookies=cookies)
    print r.text

login()