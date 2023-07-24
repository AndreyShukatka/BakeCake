from django.shortcuts import render
from .models import Level, Form, Topping, Berries, Decor


def index(request):
    levels = Level.objects.all()
    forms = Form.objects.all()
    toppings = Topping.objects.all()
    berries = Berries.objects.all()
    decors = Decor.objects.all()
    context = {
        'levels': levels,
        'forms': forms,
        'toppings': toppings,
        'berries': berries,
        'decors': decors
    }

    return render(request, "index.html", context)
