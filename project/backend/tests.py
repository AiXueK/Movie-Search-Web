#import flask
#from flask import Flask
#from flask import request
from sre_constants import FAILURE
import requests
import json


if __name__ == "__main__":
    url = 'http://127.0.0.1:5000/api'

    print('\nStarting TEST[1]')

    r = requests.post(url + '/register/otc', json = {"email": "adityaphadke14@gmail.com"},)
    data = r.json()
    #print(r.text)
    if data['result'] == 'success':
        print('\n TEST[1] PASSED')
    else:
        print('\n TEST[1] FAILED')

    print('\nStarting TEST[2]')

    verificationCode = input('\nPlease enter verificationCode: ')
    r = requests.post(url + '/register', json = {"email": "adityaphadke14@gmail.com", "username": "Aditya", "password": "6610283559143a5456d5c3b7877f5db5b1c7af60585112e82d1834d72205b158", "password2": "6610283559143a5456d5c3b7877f5db5b1c7af60585112e82d1834d72205b158", "verificationCode": f'{verificationCode}'})
    data = r.json()


    if data['result'] == 'success':
        print('\n TEST[2] PASSED')
    else:
        print(r.text)
        print('\n TEST[2] FAILED')

    print('\nStarting TEST[3]')

    r = requests.post(url + '/auth', json = {"email": "adityaphadke14@gmail.com", "password": "6610283559143a5456d5c3b7877f5db5b1c7af60585112e82d1834d72205b158"},)
    data = r.json()
    if (data["result"] != 'failure'):
        print(f'\nToken Recv: {data["token"]}')

    if data['result'] == 'success':
        print('\n TEST[3] PASSED')
    else:
        print('\n TEST[3] FAILED')


    print('\nStarting TEST[4]')
    r = requests.post(url + '/auth', json = {"email": "adityaphadke14@gmail.com", "password": "6610283559143a5456d5c3b7877f5db5b1c7af60585112e82d1834d72205b159"},)
    data = r.json()

    if data['result'] == 'failure':
        print('\n TEST[4] PASSED')
    else:
        print('\n TEST[4] FAILED')

    
    print('\nStarting TEST[5]')
    r = requests.post(url + '/register', json = {"email": "adityaphadke14@gmail.com", "username": "Aditya", "password": "6610283559143a5456d5c3b7877f5db5b1c7af60585112e82d1834d72205b158", "password2": "6610283559143a5456d5c3b7877f5db5b1c7af60585112e82d1834d72205b157", "verificationCode": f'{verificationCode}'},)
    data = r.json()

    if data['result'] == 'failure':
        print('\n TEST[4] PASSED')
    else:
        print('\n TEST[4] FAILED')

