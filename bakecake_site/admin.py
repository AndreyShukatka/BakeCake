from django.contrib import admin
from .models import (
    Level, Form, Topping, Berries, Decor
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