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


class Order(models.Model):
    STATUSES = [
        ('1', 'Ожидает оплаты'),
        ('2', 'Принят к обработке'),
        ('3', 'Готовится'),
        ('4', 'Передан в доставку'),
        ('5', 'Завершен'),
    ]
    level = models.ForeignKey(Level, verbose_name='Уровень', on_delete=models.CASCADE)
    form = models.ForeignKey(Form, verbose_name='Форма', on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, verbose_name='Топпинги', on_delete=models.CASCADE)
    berries = models.ForeignKey(Berries, verbose_name='Ягоды', on_delete=models.CASCADE)
    decor = models.ForeignKey(Decor, verbose_name='Декор', on_delete=models.CASCADE)
    inscription = models.CharField(max_length=200, verbose_name='Надпись', blank=True, null=True)
    address = models.CharField('Адрес', max_length=150, blank=True, null=True)
    date = models.DateField('Дата доставки')
    time = models.TimeField('Время доставки')
    status = models.CharField(
        'Статус заказа',
        max_length=20,
        choices=STATUSES,
        default='1',
    )