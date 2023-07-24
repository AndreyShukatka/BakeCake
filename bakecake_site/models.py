from django.db import models


class Level(models.Model):
    title = models.CharField(max_length=200, verbose_name='Уровень')
    price = models.FloatField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.title

class Form(models.Model):
    title = models.CharField(max_length=200, verbose_name='Формы')
    price = models.FloatField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.title


class Topping(models.Model):
    title = models.CharField(max_length=200, verbose_name='Топпинг')
    price = models.FloatField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.title

class Berries(models.Model):
    title = models.CharField(max_length=200, verbose_name='Ягоды')
    price = models.FloatField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.title


class Decor(models.Model):
    title = models.CharField(max_length=200, verbose_name='Декор')
    price = models.FloatField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.title
