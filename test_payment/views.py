from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
import requests
import json

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def start(request):
    '''Verify'''
    print 'rG: ', request.GET
    print 'rP: ', request.POST
    
    if request.method == "POST":
        print request.POST
        print 'posting to paystack'
        
        secret_key      = request.POST.get('secret_key')
        reference          = request.POST.get('reference')
        amount             = request.POST.get('amount')
        email              = request.POST.get('email')
        
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {'Authorization': secret_key, 'Content-Type': 'application/json'}
        callback_url = 'http://127.0.0.1:9005/payment/start'
        data = {'reference': reference, 'amount': amount, 'email': email, 'callback_url': callback_url}
        r = requests.post(url, json = data, headers = headers, verify = True)
        r_json = r.json()
        print 'r_json.json: ',r_json
        
        if r_json['status']  == True:
            r_json_data = r_json['data']
            authorization_url = r_json_data['authorization_url']
            return redirect(authorization_url)
            
        messages.error(request, r_json['message'])
    return render(request, 'payment/start.html')
    
    