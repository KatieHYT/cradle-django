import json
import random
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .pet_friendly.src.gpt_task_assigner import GPTTaskAssigner
from .pet_friendly.src.tools import get_file_contents 

gpt_task_assigner = GPTTaskAssigner(settings.OPENAI_API_KEY, pfj_src_dict=settings.PET_FRIENDLY_JUDGER_SRC_DICT)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        txt = request.POST.get('txt')
        if '%petfriendly%' in txt:
            reply = gpt_task_assigner.judge_store_pet_friendly(txt)  
        else:
            reply = gpt_task_assigner.chat(txt) 
        
        
        return JsonResponse({
            'response': reply,
            })
    else:
        return HttpResponseBadRequest()
