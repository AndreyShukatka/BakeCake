from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Missing email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Имя', max_length=250, default='some_user', blank=True)
    email = models.EmailField('Адрес электронной почты', max_length=50, unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    is_staff = models.BooleanField('Является сотрудником', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.username

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
    user = models.ForeignKey(User, verbose_name='Заказчик', on_delete=models.CASCADE, related_name='order')
    level = models.ForeignKey(Level, verbose_name='Уровень', on_delete=models.CASCADE)
    form = models.ForeignKey(Form, verbose_name='Форма', on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, verbose_name='Топпинги', on_delete=models.CASCADE)
    berries = models.ForeignKey(Berries, verbose_name='Ягоды', on_delete=models.CASCADE, blank=True, null=True)
    decor = models.ForeignKey(Decor, verbose_name='Декор', on_delete=models.CASCADE, blank=True, null=True)
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