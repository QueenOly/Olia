from django.http import HttpResponse, JsonResponse
from par import hh
from . import models

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def vacancy(request, vacancy_id: int = None, count=10, ffrom=0):
    if vacancy_id:
        return HttpResponse(models.Vacancy.objects.get(id=vacancy_id))
    else:
        return HttpResponse(models.Vacancy.objects.all()[ffrom : ffrom + count])

def search(request, keyword:str):
    m = models.Vacancy.objects.all()
    s = []
    for i in m:
        if (keyword in i.name or keyword in i.employer.name or 
        keyword in i.responsibilities or keyword in i.requirements):
            s.append([i.name, i.employer])
    return JsonResponse(s, safe=False)

def echo(request):
    m = models.Vacancy.objects.all()
    return JsonResponse(m)

def parse_vacancies(request, keyword:str, count, ffrom):
    r = hh.HH(1)
    e = r.get_vacancies(keyword, 100, int(ffrom))
    return JsonResponse(e, safe=False)
    