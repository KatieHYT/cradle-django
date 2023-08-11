import json
import random
import os
import openai

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .pet_friendly.src.pet_friendly_judger import PetFriendlyJudger
from .pet_friendly.src.tools import get_file_contents 

openai.api_key = settings.OPENAI_API_KEY
pfj = PetFriendlyJudger(settings.PET_FRIENDLY_JUDGER_SRC_DICT)

def _generate_response(place_name, reply):
    """
    This is a funny way (but the only way so far) to make it stream-like from client side.
    We must return meaningless \n in an interweave manner; 
    otherwise it will not pop up the next thing until it get to the end.
    
    """
    cnt = 0
    while True:
        try:
            if cnt % 2 ==0:
                if cnt == 0:
                    yield f"Is {place_name} pet-friendly?"
                else:
                    yield "\n"
            else:
                chunk = next(reply)
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content is not None:
                    #print(content)
                    yield content

        except StopIteration:
            break 
        cnt+=1

def check_is_cradle_confirm():
    #TODO(kt): re-load pandas every time for now 
    #cradle_db = pd.read_csv(settings.cradle_database_path)

    # url 2 lat lng
    return True

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        if_stream = True
        post_data = json.loads(request.body.decode("utf-8"))
        api_input = post_data['api_input']
        print(f'Front-end posting: {api_input}')
        if '%petfriendly%' in api_input:
            place_id = api_input.split("friendly%")[-1]
            print("Judging pet-friendly...")
            
            if check_is_cradle_confirm():
                reply = {
                        "confirm_date": "2023-08-10",
                        "manager": "KT",
                        "service_dog": True,
                        "non_service_dog": True,
                        "dog_treat": True,
                        "dog_water": False,
                        }
                return JsonResponse({
                    'response': reply,
                    })
            else:
                place_name, reply = pfj.judge_store(place_id, if_stream=if_stream) 
                # Return a streaming response to the client
                print("Gpt streaming...") 
                return StreamingHttpResponse(_generate_response(place_name, reply), content_type='text/event-stream')

        else:
            reply = gpt_task_assigner.chat(txt) 
    else:
        return HttpResponseBadRequest()
