from django.contrib import admin
from .models import (
    Level, Form, Topping, Berries, Decor, Order, User, Ready_cakes, Bitly_statistic
)


@admin.register(Ready_cakes)
class Ready_cakesAdmin(admin.ModelAdmin):
    pass

@admin.register(Bitly_statistic)
class Bitly_statisticAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    pass

@admin.register(Berries)
class BerriesAdmin(admin.ModelAdmin):
    pass

@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass