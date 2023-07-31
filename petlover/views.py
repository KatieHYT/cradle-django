import json
import random
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .pet_friendly.src.gpt_task_assigner import GPTTaskAssigner
from .pet_friendly.src.tools import get_file_contents 

gpt_task_assigner = GPTTaskAssigner(settings.OPENAI_API_KEY, pfj_src_dict=settings.PET_FRIENDLY_JUDGER_SRC_DICT)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        if_stream = True
        post_data = json.loads(request.body.decode("utf-8"))
        txt = post_data['txt']
        if '%petfriendly%' in txt:
            reply = gpt_task_assigner.judge_store_pet_friendly(txt, if_stream=if_stream)  
        else:
            reply = gpt_task_assigner.chat(txt) 
        
        if if_stream:
            def _generate_response():
                """
                This is a funny way (but the only way so far) to make it stream-like from client side.
                We must return meaningless \n in an interweave manner; 
                otherwise it will not pop up the next thing until it get to the end.
                
                """
                cnt = 0
                while True:
                    try:
                        if cnt % 2 ==0:
                            yield "\n"
                        else:
                            chunk = next(reply)
                            content = chunk["choices"][0].get("delta", {}).get("content")
                            if content is not None:
                                print(content)
                                yield content

                    except StopIteration:
                        break 
                    cnt+=1
            # Return a streaming response to the client
            return StreamingHttpResponse(_generate_response(), content_type='text/event-stream')
        else:
            return JsonResponse({
                'response': reply,
                })
    else:
        return HttpResponseBadRequest()
