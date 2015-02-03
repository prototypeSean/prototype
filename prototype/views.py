# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import mimetypes
import settings
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseForbidden
from bs4 import BeautifulSoup
import urllib2

def media_view(request, path):
    # 假設你的 URL rule 長這樣：r'/media/(?P<path>.*)'
    # 那麼 path 現在應該會長得像這樣："uranusjr/<3.png"
    # 如果使用者不符合，就直接吐 HTTP 403。你可以用自己喜歡的回應。
    if request.user.username != path.split('/')[1]:
        return HttpResponseForbidden('nop!')


    # 找到圖片檔路徑
    abspath = os.path.abspath(os.path.join(settings.MEDIA_ROOT, path))

    # 用內建的 mimetypes 模組猜測 content type。
    # 正常來講這會用副檔名，例如 .png 就會變成 image/png
    mimetype = mimetypes.guess_type(abspath)[1]

    # 讀取圖片內容，組合成 HTTP response。
    with open(abspath, 'rb') as f:
        response = HttpResponse(f, content_type=mimetype)
    response['Content-Disposition'] = 'attachment; filename={fn}'.format(
        fn=os.path.basename(abspath),
        )
    return response
