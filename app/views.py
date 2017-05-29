from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

from django.views.generic import TemplateView

from isAStudent import settings


class IndexView(TemplateView):
    template_name = 'index.html'


class APIView(TemplateView):
    def get(self, request, *args, **kwargs):
        id = request.get.GET('matric') or None
        pin = request.get.GET('name') or None


       pass

    def get_result(id, pin):
        cookies = {
            'PHPSESSID': settings.SESSION_ID,
        }

        headers = {
            'Origin': settings.ORIGIN,
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Referer': settings.REFFERER,
            'Connection': 'keep-alive',
        }

        data = [
            ('id', id),
            ('pin', pin),
            ('x', '38'),
            ('y', '14'),
            ('submitted', 'submitted'),
        ]

        data = requests.post(settings.API_URL, headers=headers, cookies=cookies, data=data)
        html = data.content

        soup = BeautifulSoup(html, 'html.parser')

        data_info = soup.find("div", {"id": "stud_info_bx"})