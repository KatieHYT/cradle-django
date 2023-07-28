import json
import random
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .pet_friendly.gpt_task_assigner import GPTTaskAssigner
from .pet_friendly.tools import get_file_contents 

#TODO(hyt): find aa proper way to load path
openai_api_key = get_file_contents('/TOP/home/kt/API_KEY/openai')
gpt_task_assigner = GPTTaskAssigner(openai_api_key)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        event = json.loads(request.body.decode('utf-8'))
        txt = event['txt']
        response_dict = {}
        if '%petfriendly%' in txt:
            reply = gpt_task_assigner.judge_store_pet_friendly(txt)  
        else:
            reply = gpt_task_assigner.chat(txt) 
        
        response_dict['reply'] = reply
        
        return JsonResponse(response_dict)
    else:
        return HttpResponseBadRequest()
