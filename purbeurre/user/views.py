"""User"""
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email, validate_slug
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

import json

from .forms import ConnectionForm, NewForm
from .backends import AuthenticateBackend
from .models import User, Newsletter
from .validators import validate_username, UsernameValidator

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

    data = {'ok': False}

    if request.method == "POST":
        form_new = NewForm(request.POST)
        if form_new.is_valid():
            email = form_new.cleaned_data["email"]
            pwd = form_new.cleaned_data["pwd"]
            pwd_confirm = form_new.cleaned_data["pwd_confirm"]
            user_login = form_new.cleaned_data["user_login"]
            firstname = form_new.cleaned_data["firstname"]
            lastname = form_new.cleaned_data["lastname"]
            newsletter = form_new.cleaned_data["newsletter"]
            if User.objects.filter(email=email).count() == 0:
                try:
                    user = User.objects.create_user(
                        email,
                        password=pwd,
                        username=user_login,
                        first_name=firstname,
                        last_name=lastname
                    )
                    user.save()
                    data['ok'] = True
                    print('New user OK')
                    print(user)
                except ValidationError:
                    data['ok'] = False
                try:
                    user_newsletter = Newsletter.objects.update_or_create(
                        user,
                        newsletter
                    )
                    print('Newsletter OK')
                    print(user_newsletter)
                except:
                    data['ok'] = False
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

    try:
        # UsernameValidator(user_login)
        # print(user_validate)
        # validate_slug(user_login)
        validate_username(user_login)
        print(user_login)
    except ValidationError:
        print('incorrect format')
        return HttpResponse('Incorrect login format')

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

@csrf_exempt
def check_pwd(request):
    pwd = request.POST.get("pwd")

    try:
        validate_password(pwd)
    except ValidationError as err:
        return HttpResponse(json.dumps(err.messages))
    else:
        return HttpResponse("Mot de passe OK")
