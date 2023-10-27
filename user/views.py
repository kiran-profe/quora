from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,logout ,login
from .models import Profile
from django.urls import reverse


def register(request):

    if request.user.is_authenticated:
        return HttpResponse('First logout')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user = user)
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegistrationForm()

    context = {
        'form' : form
    }

    return render(request , 'user/register.html',context)


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('web:questions_list'))

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            if user:

                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('web:questions_list'))
                else:
                    return HttpResponse('User is not Active')
            else:
                return HttpResponse('User Not Available')
    else:
        form = LoginForm()

    context = {
        'form' : form
    }

    return render(request ,'user/login.html' ,context )


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('web:questions_list'))
