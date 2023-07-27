from .models import Level, Form, Topping, Berries, Decor
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.urls import reverse, reverse_lazy


class IndexPage(View):
    template_name = 'index.html'

    def get_context_data(self):
        context = {
            'levels': Level.objects.all(),
            'forms': Form.objects.all(),
            'toppings': Topping.objects.all(),
            'berries': Berries.objects.all(),
            'decors': Decor.objects.all()
        }
        return context

    def post(self, request, *args, **kwargs):
        if request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
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
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class LkPage(View):
    template_name = 'lk.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        user.username = request.POST.get('NAME')
        user.email = request.POST.get('EMAIL')
        user.phone = request.POST.get('PHONE')
        user.save()
        print()
        print("VIEW POST")
        print(request.POST.get('NAME'))
        print(request.POST.get('PHONE'))
        # print(request.POST.get('EMAIL'))
        print(request.POST)
        print(request.user)
        print(dir(request))
        print()
        return render(request, self.template_name)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
