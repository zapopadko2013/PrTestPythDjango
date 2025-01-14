from django.db import models
from django.utils import timezone

class User(models.Model):
    phone=models.BigIntegerField()
    password = models.CharField(max_length=20)
    status=models.IntegerField()
    name = models.CharField(max_length=200)
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
