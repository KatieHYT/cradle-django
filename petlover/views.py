import json
import random
import os
import openai
import pandas as pd
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .pet_friendly.src.pet_friendly_judger import PetFriendlyJudger
from .pet_friendly.src.tools import get_file_contents, read_json

openai.api_key = os.environ["OPENAI_API_KEY"]
pfj = PetFriendlyJudger(settings.PET_FRIENDLY_JUDGER_SRC_DICT)

def _generate_response(place_name, reply, last_review_path):
    """
    This is a funny way (but the only way so far) to make it stream-like from client side.
    We must return meaningless \n in an interweave manner; 
    otherwise it will not pop up the next thing until it get to the end.
    
    """
    cnt = 0
    data_to_write=""
    while True:
        try:
            if cnt % 2 ==0:
                if cnt == 0:
                    content = f"Is {place_name} pet-friendly?"
                    data_to_write += content + " "
                    yield content
                else:
                    yield "\n"
            else:
                chunk = next(reply)
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content is not None:
                    #print(content)
                    data_to_write += content + " "
                    yield content

        except StopIteration:
            # Open the file in write mode ('w')
            with open(last_review_path, 'w') as file:
                # Write the data to the file
                file.write(data_to_write)
            
            # Print a message to indicate that the file has been written
            print(f'Data has been written to {file_path}')
            break 
        cnt+=1

def check_is_cradle_confirm(url):
    url2latlng = read_json(os.environ["URL2LATLNG_PATH"])
    db = pd.read_csv(os.environ["CRADLE_DB_PATH"])
    cradle_confirm = None
    if not url in url2latlng.keys():
        return cradle_confirm
    else:
        latlng = url2latlng[url]
    
        if latlng in list(db['latlng']):
            _row = db[db['latlng']==latlng]
            cradle_confirm = {
                "manager_confirm_date": _row['manager_confirm_date'].item(),
                "manager_name": _row['manager_name'].item(),
                "service_dog": bool( _row['service_dog'].item()),
                "non_service_dog": bool( _row['non_service_dog'].item()),
                "dog_treat": bool( _row['dog_treat'].item()),
                "dog_water": bool( _row['dog_water'].item()),
                    }

        return cradle_confirm

def save_use_record(file_content, save_dir='./use_record'):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, f"{formatted_datetime}.txt")
    with open(save_path, "w") as file:
        file.write(file_content)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        if_stream = True
        post_data = json.loads(request.body.decode("utf-8"))
        api_input = post_data['api_input']
        print(f'Front-end posting: {api_input}')
        if '%petfriendly%' in api_input:
            place_info = api_input.split("friendly%")[-1]
            print("Judging pet-friendly...")

            if ('/maps/search' in place_info) or ('/maps/place' in place_info):
                url = place_info
            else:
                url = f'https://www.google.com/maps/place/?q=place_id:{place_info}'
            save_use_record(url) 

            #cradle_confirm = check_is_cradle_confirm(url)
            ##TODO(yt)
            #if cradle_confirm:
            #    return JsonResponse({
            #        'response': cradle_confirm,
            #        })
            #else:
            #    place_name, reply = pfj.judge_store(url, if_stream=if_stream) 
            #    # Return a streaming response to the client
            #    print("Gpt streaming...") 
            #    return StreamingHttpResponse(_generate_response(place_name, reply), content_type='text/event-stream')

            place_name, reply = pfj.judge_store(url, if_stream=if_stream) 
            url2latlng = read_json(os.environ["URL2LATLNG_PATH"])
            latlng = url2latlng[url]
            last_review_path = os.path.join(os.environ["LAST_SUMMARY_DIR"], latlng+'.txt')
            # Return a streaming response to the client
            print("Gpt streaming...") 
            return StreamingHttpResponse(_generate_response(place_name, reply, last_review_path), content_type='text/event-stream')
        elif '%checkcall' in api_input:
            place_id = api_input.split("call%")[-1]
            url = f'https://www.google.com/maps/place/?q=place_id:{place_id}'
            print(f"Checking call history...{place_id}")

            url2latlng = read_json(os.environ["URL2LATLNG_PATH"])
            call_conversation = None
            if url in url2latlng.keys():
                latlng = url2latlng[url]
                print(latlng)
                last_list = os.listdir(os.environ["LAST_CALL_DIR"]) 
                if latlng+'.txt' in last_list:
                    path = os.path.join(os.environ["LAST_CALL_DIR"], latlng+'.txt')
                    # Open the file in read mode ('r')
                    with open(path, 'r') as file:
                        # Read the entire file content into a variable
                        call_conversation = file.read()
            #call_conversation =  "\
            #        Last call time: 2023-09-08 20:21:03\n\
            #        A: 123\n\
            #        B: 456\n\
            #        A: 333\n"
            return JsonResponse({
                'call_conversation': call_conversation,
                })

        elif '%checkreview' in api_input:
            place_id = api_input.split("review%")[-1]
            url = f'https://www.google.com/maps/place/?q=place_id:{place_id}'
            print(f"Checking summary history...{place_id}")
            
            url2latlng = read_json(os.environ["URL2LATLNG_PATH"])
            review_summary = None
            if url in url2latlng.keys():
                latlng = url2latlng[url]
                last_list = os.listdir(os.environ["LAST_SUMMARY_DIR"]) 
                if latlng+'.txt' in last_list:
                    path = os.path.join(os.environ["LAST_SUMMARY_DIR"], latlng+'.txt')
                    # Open the file in read mode ('r')
                    with open(path, 'r') as file:
                        # Read the entire file content into a variable
                        review_summary = file.read()

            return JsonResponse({
                'review_summary': review_summary,
                })

        else:
            assert 1==0, "Not implemented"
    else:
        return HttpResponseBadRequest()
