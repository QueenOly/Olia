from django.urls import path

from . import views

urlpatterns = [
    path('<int:vacancy_id>/<int:count>/<int:ffrom>/', views.vacancy, name='vacancy'),
    path('search/<str:keyword>/', views.search, name='search'),
    path('parse/<str:keyword>/<int:count>/<int:ffrom>/', views.parse_vacancies, name='parse'),
    path('echo/', views.echo, name='echo'),
]
