from django.contrib import admin
from .models import (
    Level, Form, Topping, Berries, Decor, Order, User, Ready_cakes, Bitly_statistic
)


@admin.register(Ready_cakes)
class Ready_cakesAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'index_page'
    )


@admin.register(Bitly_statistic)
class Bitly_statisticAdmin(admin.ModelAdmin):
    list_display = (
        'telegramm_name',
        'url',
        'number_transitions'
    )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
    )


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
    )


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
    )


@admin.register(Berries)
class BerriesAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
    )


@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'address',
    )
