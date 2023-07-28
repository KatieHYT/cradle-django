import os
import json
from django.shortcuts import render
from django.conf import settings

def index(request):
    url_pet_friendly = os.path.join(settings.PUBLIC_IP, 'petlover/callback')
    settings4js= {
            'url_pet_friendly': url_pet_friendly,
            }
    return render(request, "frontend/index.html", settings4js)
