import random
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage, AudioSendMessage

from .pet_friendly.gpt_task_assigner import GPTTaskAssigner
from .pet_friendly.tools import get_file_contents 

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

#TODO(hyt): find aa proper way to load path
openai_api_key = get_file_contents('/TOP/home/kt/API_KEY/openai')
gpt_task_assigner = GPTTaskAssigner(openai_api_key)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # the event
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # if there's message event
                message = []
                if event.message.type=='text':
                    mtext = event.message.text
                    if '%petfriendly%' in mtext:
                        _judge = gpt_task_assigner.judge_store_pet_friendly(mtext)  
                        message.append(TextSendMessage(text=_judge))
                    else:
                        _reply = gpt_task_assigner.chat(mtext) 
                        message.append(TextSendMessage(text=_reply))
                else: 
                   message.append(TextSendMessage(text='Sorry! Not a supported servive.')) 
                line_bot_api.reply_message(
                    event.reply_token,
                    message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

