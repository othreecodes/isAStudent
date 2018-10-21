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

        if id is None:
            return JsonResponse(data={"error": "invalid API Usage"}, status=200)
        key = None
        try:
            key = self.get_sur_name(id)
        except:
            return JsonResponse(data={"is_student": False}, status=200)
            
        res = self.get_result(id, key)
            


        return JsonResponse(data=res, status=200)

    def post(self, request):
        id = request.POST.get('matric') or None

        if id is None:
            return JsonResponse(data={"error": "invalid API Usage"}, status=200)

        key = None
        try:
            key = self.get_sur_name(id)
        except:
            return JsonResponse(data={"is_student": False}, status=200)

        res = self.get_result(id, key)
        


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
            data = {"is_student": True, "level":100, "matric_no":id, "message":"100 Level and DE students Data would be available soon"}
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


    def get_sur_name(self,id):
        
        cookies = {
            '__cfduid': 'de910f13aba30d2d3463b428b2b8da8151539034439',
            'ASP.NET_SessionId': 'csu4g13zundreyruo30ntim2',
        }

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://streceipt.ui.edu.ng',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://streceipt.ui.edu.ng/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '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',
        '__VIEWSTATEGENERATOR': 'CA0B0334',
        '__EVENTVALIDATION': 'eDMCx6lGZLOzpD0NDkX5aJChxY8QGwsSC3m9VDQ3lIHDY1Xp7fRd4yiDeUnPMyAYvzyrYeOaCTl0jlllh11wT10Dg5U2cEPW7zRKuCtNLs0279ejjuKcXEyF0o3Su5W6AzjrrTSaBdWBLAQTWjpdUFqKh2phOzjX4+VS31aTcilZTBUxb9FT340+/gb5FMmu409uqMjjTay9yuMrek3cRPfgQNToKiZLLsBg2/aNkus8Ie2k1yN1z0/zLHhIjtnSyXU2bGbv2QoodeAHM1kBuX+y/+Q=',
        'ctl00_RadPanelBar1_ClientState': '{"expandedItems":[],"logEntries":[],"selectedItems":["0"]}',
        'ctl00$Login1$UserName': '185937',
        'ctl00$Login1$Password': 'qazwsxedc',
        'ctl00$MainContent$TextBox1': id,
        'ctl00$MainContent$Searchbtn.x': '47',
        'ctl00$MainContent$Searchbtn.y': '12',
        'ctl00_MainContent_RadTabStrip1_ClientState': '{"selectedIndexes":["1"],"logEntries":[],"scrollState":{}}',
        'ctl00_MainContent_RadGrid1_ClientState': '',
        'ctl00_MainContent_newGrid_ClientState': '',
        'ctl00_MainContent_RadMultiPage1_ClientState': ''
        }

        response = requests.post('http://streceipt.ui.edu.ng/', headers=headers, cookies=cookies, data=data)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.select_one("#ctl00_MainContent_newGrid_ctl00__0").find_all('td')[4].text