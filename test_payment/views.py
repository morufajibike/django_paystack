from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
import requests
import json

import os, random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gen_random_code():
    random_code = '1-%d' %random.randint(0, 9)
    alnum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz'
    for x in range(10):
        random_code += random.choice(alnum)
    return random_code

def start(request):
    '''Verify'''
    print 'rG: ', request.GET
    print 'rP: ', request.POST
    
    if request.method == "POST":
        print request.POST
        print 'posting to paystack'
        
        secret_key      = request.POST.get('secret_key')
        request.session['secret_key'] = secret_key
        reference          = request.POST.get('reference')
        amount             = float(request.POST.get('amount'))
        amount_in_kobo     = amount * 100 
        email              = request.POST.get('email')
        
        return go_to_paystack(request, secret_key, reference, amount_in_kobo, email)
        # url = 'https://api.paystack.co/transaction/initialize'
        # headers = {'Authorization': secret_key, 'Content-Type': 'application/json'}
        # callback_url = reverse('payment:payment_result')#'http://127.0.0.1:9005/payment/start'
        # data = {'reference': reference, 'amount': amount, 'email': email, 'callback_url': callback_url}
        # r = requests.post(url, json = data, headers = headers, verify = True)
        # r_json = r.json()
        # print 'r_json.json: ',r_json
        # 
        # if r_json['status']  == True:
        #     r_json_data = r_json['data']
        #     authorization_url = r_json_data['authorization_url']
        #     return redirect(authorization_url)
            
    reference = gen_random_code()
    return render(request, 'payment/start.html', {'reference': reference})

def go_to_paystack(request, secret_key, reference, amount, email):
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {'Authorization': secret_key, 'Content-Type': 'application/json'}
    #callback_url = reverse('payment:payment_result', args=[reference])#'http://127.0.0.1:9005/payment/start'
    callback_url = request.build_absolute_uri(reverse('payment:payment_result'))#'http://127.0.0.1:9005/payment/start'
    data = {'reference': reference, 'amount': amount, 'email': email, 'callback_url': callback_url}
    r = requests.post(url, json = data, headers = headers, verify = True)
    r_json = r.json()
    print 'r_json.json: ',r_json
    
    if r_json['status']  == True:
        r_json_data = r_json['data']
        authorization_url = r_json_data['authorization_url']
        return redirect(authorization_url)
    else:
        messages.error(request, r_json['message'])
        return redirect(request.META.get('HTTP_REFERER'))
        

def payment_result(request):
    reference = request.GET.get('trxref')
    secret_key = request.session['secret_key']
    print 'reference: ',reference
    print 'secret_key: ',secret_key
    
    url = 'https://api.paystack.co/transaction/verify/%s' %reference
    headers = {'Authorization': secret_key, 'Content-Type': 'application/json'}
    r = requests.get(url, headers = headers, verify = True)
    r_json = r.json()
    print 'r_json.json: ',r_json
    
    context = {}
    if r_json['status'] == True:
        context.update({'data': r_json['data'], 'customer_data': r_json['data']['customer'], 'message': r_json['message']})
    return render(request, 'payment/payment_result.html', context)