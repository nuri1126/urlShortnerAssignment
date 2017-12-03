from django.shortcuts import render_to_response, get_object_or_404
import random, string, json
from urlShortnerWebsite.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.views.decorators import csrf
from django.shortcuts import render

def index(request):
    c = {}
    return render(request, 'urlShortnerWebsite/index.html', c)

def redirect_original(request, short_id):
    url = get_object_or_404(Urls, pk=short_id) # get object, if not found return 404 error
    url.count += 1
    url.save()
    return HttpResponseRedirect(url.httpurl)

def shorten_url(request):
    url = request.POST.get("url", '')
    if not (url == ''):
        #for i in savedUrls.httpurl
        # ##############중복되는 부분 거르는 것을 잘 모르겠음...~~ ㅠㅠ
        #     if i == url:
        #         response_data = {}
        #         response_data['url'] = settings.SITE_URL + "/" + savedUrls.short_id
        #         return HttpResponse(json.dumps(response_data), content_type="application/json")
        #         #######################################
            #else:
                short_id = get_short_code()
                b = Urls(httpurl=url, short_id=short_id)
                b.save()
                response_data = {}
                response_data['url'] = settings.SITE_URL + "/" + short_id
                return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse(json.dumps({"error": "error occurs"}),
             content_type="application/json")

def get_short_code():
    length = 8
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # 랜덤으로 url 생성
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Urls.objects.get(pk=short_id)
        except:
            return short_id
