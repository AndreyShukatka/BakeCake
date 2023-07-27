from .models import Level, Form, Topping, Berries, Decor, Ready_cakes
from django.views import View
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth import authenticate, login
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.urls import reverse, reverse_lazy

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
    users = User.objects.all()

    def post(self, request, *args, **kwargs):
        users = User.objects.all()
        email = request.POST.get('email')
        if users.filter(email=email) and not users.filter(id=request.user.id, email=email):
            form = UserProfileForm(instance=request.user)
            return render(request, 'lk.html', {'form': form, 'error_email': 'Такой email уже существует!'})
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('lk')
        else:
            print(form.errors)
        return render(request, 'lk.html', {'form': form})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CatalogPage(View):
    template_name = 'catalog.html'

    def get(self, request, *args, **kwargs):
        all_ready_cakes = Ready_cakes.objects.all()
        for a in all_ready_cakes:
            print(a.index_page)
        content = {'cakes': all_ready_cakes}
        return render(request, self.template_name, content)
