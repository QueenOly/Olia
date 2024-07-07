import requests
from . import models

class HH:
    def __init__(self, area) -> None:
        self.area = area

    def get_vacancies(self, keyword, count, ffrom):
        base_url = "https://api.hh.ru/vacancies"
        params = {
            "text": keyword,
            "area": self.area,
            "per_page": count, 
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            "User-Agent": "Your User Agent",
        }

        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("items", [])
            o = []
            print(response.content)
            for vacancy in vacancies[ffrom:ffrom+count]:
                try:
                    _ = models.Area.objects.get(id = vacancy.get('area')['id'])
                except models.Area.DoesNotExist:
                    a = models.Area(
                        id = vacancy.get('area')['id'],
                        name = vacancy.get('area')['name'],
                        url = vacancy.get('area')['url']
                    )
                    a.save()
                for _ in range(int(count)):
                    o.append({
                        "name": vacancy.get('name'),
                        "url": vacancy.get('url').encode('ascii').decode('unicode_escape').encode('utf-8').decode('utf-8'),
                        "area": vacancy.get('area')['name'],
                        "employer": vacancy.get('employer')['name'],
                        # "employer_url": vacancy.get('employer')['url'],
                        "salary_from": vacancy.get('salary'),
                        "vacancy_type": vacancy.get('type')['id'],
                        "address": vacancy.get('address'),
                        "requirements": vacancy.get('snippet'),
                        "experience": vacancy.get('experience')['name'],
                        "employment": vacancy.get('employment')['name'],
                    })
                try:
                    _ = models.Vacancy.objects.get(id=vacancy.get('id'))
                except models.Vacancy.DoesNotExist:
                    v = models.Vacancy(
                        id = vacancy.get('id'),
                        name = vacancy.get('name'),
                        url = vacancy.get('alternative_url'),
                        area = models.Area.objects.get(id = vacancy.get('area')['id']),
                        employer = vacancy.get('employer')['name'],
                        # employer_url = vacancy.get('employer')['url'],
                        salary_from = str(vacancy.get('salary')),
                        vacancy_type  = vacancy.get('type')['id'],
                        address = str(vacancy.get('address')),
                        requirements  = str(vacancy.get('snippet')),
                        experience   = vacancy.get('experience')['name'],
                        employment = vacancy.get('employment')['name'],
                    )
                    v.save()
        return {"items": o}
