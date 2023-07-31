from urllib.parse import urlparse

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from yookassa import Configuration, Payment

from .forms import UserRegistrationForm
from .models import Level, Form, Topping, Berries, Decor, Ready_cakes, Order, Order_Ready_cakes
from .models import User, Bitly_statistic


class IndexPage(View):
    template_name = 'index.html'
    all_ready_cakes = Ready_cakes.objects.all()

    def get_context_data(self):
        context = {
            'levels': Level.objects.all(),
            'forms': Form.objects.all(),
            'toppings': Topping.objects.all(),
            'berries': Berries.objects.all(),
            'decors': Decor.objects.all(),
            'cakes': self.all_ready_cakes
        }
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if request.POST.get('login'):
            if User.objects.filter(email=email):
                user = authenticate(email=email, password=password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            else:
                user_registration_form = UserRegistrationForm(request.POST)
                if user_registration_form.is_valid():
                    new_user = user_registration_form.save(commit=False)
                    new_user.set_password(user_registration_form.cleaned_data['password'])
                    new_user.save()
                    email = request.POST.get('email')
                    password = request.POST.get('password')
                    user = authenticate(email=email, password=password)
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('index')
        else:
            level = Level.objects.get(title=request.POST.get('LEVELS'))
            form = Form.objects.get(title=request.POST.get('FORM'))
            topping = Topping.objects.get(title=request.POST.get('TOPPING'))
            berries = Berries.objects.get(title=request.POST.get('BERRIES', default='Нет'))
            decor = Decor.objects.get(title=request.POST.get('DECOR', default='Нет'))
            inscription = request.POST.get('WORDS', default="Нет")
            if inscription:
                order_coast = level.price + form.price + topping.price + berries.price + decor.price + 200.00
            else:
                order_coast = level.price + form.price + topping.price + berries.price + decor.price
            Order.objects.create(
                user=User.objects.get(email=request.POST.get('EMAIL')),
                level=level,
                form=form,
                topping=topping,
                berries=berries,
                decor=decor,
                inscription=inscription,
                total_price=order_coast,
                address=request.POST.get('ADDRESS'),
                date=request.POST.get('DATE'  ),
                time=request.POST.get('TIME'),
                order_comment=request.POST.get('COMMENTS'),
                delivery_comment=request.POST.get('DELIVCOMMENTS'),
            )
            last_order = Order.objects.filter(user=request.user.id).order_by('-id').latest('id')
            payment_id, payment_url = create_payment(order_coast, last_order)
            return redirect(payment_url)

        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class LkPage(View):
    template_name = 'lk.html'
    users = User.objects.all()

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        user.username = request.POST.get('NAME')
        user.email = request.POST.get('EMAIL')
        user.phone = request.POST.get('PHONE')
        user.save()
        return redirect('lk')

    def get(self, request, *args, **kwargs):
        context = {
            'orders': Order.objects.filter(user=request.user.id),
            'order_ready_cake': Order_Ready_cakes.objects.filter(user=request.user.id)

        }
        return render(request, self.template_name, context=context)


class CatalogPage(View):
    template_name = 'catalog.html'
    all_ready_cakes = Ready_cakes.objects.all()
    content = {'cakes': all_ready_cakes}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.content)

    def post(self, request):
        ready_cake = Ready_cakes.objects.get(id=request.POST.get('id'))
        price = ready_cake.price
        Order_Ready_cakes.objects.create(
            user=User.objects.get(id=request.user.id),
            ready_cake=ready_cake,
            price=price
        )
        last_order = Order.objects.filter(user=request.user.id).order_by('-id').latest('id')
        payment_id, payment_url = create_payment(order_coast=price, last_order=last_order)
        print(payment_id)
        return redirect(payment_url)

class BitlyPage(View):
    template_name = 'bitly.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        url = f'{settings.URL_FOR_BITLY}#{request.POST["chanel_name"]}'
        token = settings.BITLY_TOKEN
        body = {'long_url': url}
        headers = {'Authorization': f'Bearer {token}'}
        bitly_url = 'https://api-ssl.bitly.com/v4/shorten'
        response = requests.post(
            bitly_url,
            headers=headers,
            json=body
        )
        response.raise_for_status()
        bitlink = response.json()['link']
        Bitly_statistic.objects.create(telegramm_name=request.POST['chanel_name'], url=bitlink)
        return redirect(reverse('admin:index'))


class BitlyUpdatePage(View):
    template_name = 'bitly_update.html'
    def get(self, request):
        token = settings.BITLY_TOKEN
        headers = {'Authorization': f'Bearer {token}'}
        param = {'units': -1}
        parsed_urls = Bitly_statistic.objects.all()
        for parsed_url in parsed_urls:
            url = urlparse(parsed_url.url)
            telegramm_name = parsed_url.telegramm_name
            bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url.netloc}' \
                    f'{url.path}/clicks/summary'
            response = requests.get(
                bitly_url,
                headers=headers,
                params=param
            )
            response.raise_for_status()
            clicks_count = response.json()['total_clicks']
            chanel = Bitly_statistic.objects.get(telegramm_name=telegramm_name)
            chanel.number_transitions = clicks_count
            chanel.save()
        return redirect(reverse('admin:index'))


def create_payment(order_coast, last_order):
    Configuration.configure(settings.YOOKASSA_SHOPID,settings.YOOKASSA_TOKEN)
    payment = Payment.create(
        {
            "amount": {
                "value": str(order_coast),
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": settings.YOOKASSA_RETURN_URL
            },
            "capture": True,
            "description": f"Оплата: торт на заказ,{last_order}"
        }
    )
    return payment.id, payment.confirmation.confirmation_url