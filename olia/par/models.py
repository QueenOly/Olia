from django.db import models


class Area(models.Model):
    id   = models.IntegerField(primary_key=True)
    name  = models.CharField(max_length=100)
    url   = models.CharField(max_length=100)

class Vacancy(models.Model):
    id  = models.IntegerField(primary_key=True)
    name       = models.CharField(max_length=10000)
    area        = models.ForeignKey(Area, models.CASCADE)
    url          = models.CharField(max_length=10000, null=True)
    employer = models.CharField(max_length=10000, null=True)
    employer_url = models.CharField(max_length=10000, null=True)
    salary_from  = models.CharField(max_length=10000)
    vacancy_type    = models.CharField(max_length=100)
    address= models.CharField(max_length=100000)
    requirements    = models.TextField()
    responsibilities= models.TextField()
    experience     = models.TextField()
    employment= models.TextField()


