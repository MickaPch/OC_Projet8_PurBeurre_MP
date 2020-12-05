"""User"""
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.validators import validate_email, ValidationError
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from .forms import ConnectionForm, NewForm
from .backends import AuthenticateBackend
from .models import User

# Session for authenticate
# from django.contrib.sessions.models import Session


class LoginView(TemplateView):
    """View to login User"""

    template_name = "/"
    
    form_user = ConnectionForm()
    
    def post(self, request, **kwargs):

        print(type(request))

        user_login = request.POST.get('user_login', False)
        password = request.POST.get('pwd', False)
        user = authenticate(username=user_login, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
        elif user is not None:
            return render(request, 'user/check_email.html')
        else:
            return render(request, 'user/new_account.html')
        

class LogoutView(TemplateView):
    """Logout User"""

    template_name = "/"

    def get(self, request, **kwargs):

        logout(request)

        return redirect(self.template_name)


@login_required
def user_account(request):
    """Show user account page"""

    return render(request, 'user/user.html', locals())

def new_account(request):
    """Show new user account page"""

    form_new = NewForm()

    print(User.objects.all())

    return render(request, 'user/new_account.html', locals())

def create_new(request):
    """Create a new user"""

    print('create new user')
    data = {'ok': False}

    print(request)

    if request.method == "POST":
        form_new = NewForm(request.POST)
        print(form_new)
        if form_new.is_valid():
            email = form_new.cleaned_data["email"]
            pwd = form_new.cleaned_data["pwd"]
            pwd_confirm = form_new.cleaned_data["pwd_confirm"]
            firstname = form_new.cleaned_data["firstname"]
            lastname = form_new.cleaned_data["lastname"]
            if User.objects.filter(email=email).count() == 0:
                try:
                    print(email)
                    print(pwd)
                    user = User.objects.create_user(
                        email,
                        pwd,
                        first_name=firstname,
                        last_name=lastname
                    )
                    user.save()
                    data['ok'] = True
                except forms.ValidationError:
                    print('Pas possible')
            else:
                print('utilisateur déjà pris')
            if user is not None:
                login(request, user)
                user_account(request)
        else:
            print('Form is invalid')
            try:
                validate_email(form_new.cleaned_data["email"])
            except:
                data['email'] = False
            try:
                pwd = form_new.cleaned_data["pwd"]
                pwd_confirm = form_new.cleaned_data["pwd_confirm"]
                assert pwd == pwd_confirm
            except:
                data['pwd'] = False

    else:
        form_new = NewForm()
        user = AnonymousUser()

    print(data)

    return JsonResponse(data)

@csrf_exempt
def check_user_login(request):
    user_login = request.POST.get("user_login")

    if User.objects.filter(username=user_login).exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)
@csrf_exempt
def check_email(request):
    email = request.POST.get("email")

    try:
        validate_email(email)
    except ValidationError:
        return HttpResponse("Email non valide")

    if User.objects.filter(email=email).exists():
        return HttpResponse("email pris")
    else:
        return HttpResponse("email disponible")
