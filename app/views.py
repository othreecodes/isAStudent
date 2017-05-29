from django.http import JsonResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.views import View

from django.views.generic import TemplateView

from isAStudent import settings


class IndexView(TemplateView):
    template_name = 'index.html'


class APIView(View):
    def get(self, request):
        id = request.GET.get('matric') or None
        pin = request.GET.get('name') or None

        keys = pin.split()
        res = {}
        for key in keys:
            res = self.get_result(id, key)
            if res['is_student']:
                break

        return JsonResponse(data=res, status=200)

    def get_result(self, id, pin):
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

        data_info = soup.find_all("div", {"class": "cnt_txt"})

        # print(data_info)

        if len(data_info) == 0:
            data = {"is_student": False}
        else:
            data = {
                "is_student": True,
                "matric_no": data_info[0].text,
                "name": data_info[1].text,
                "faculty": data_info[2].text,
                "dept": data_info[3].text,
                # You see what happens is that this info is a year behind
                "level": int(data_info[4].text) + 100,
                # "cgpa":data_info[6].text # bitch You guessed IT!!!

            }

        return data
