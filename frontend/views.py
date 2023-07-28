import os
import json
from django.shortcuts import render
from django.conf import settings

def index(request):
    settings4js= {
            'url_pet_friendly': os.path.join(settings.PUBLIC_IP, 'petlover/callback'),
            }
    return render(request, "frontend/index.html", {"settings4js": json.dumps(settings4js) })
