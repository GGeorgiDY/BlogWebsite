from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # this is the way we get data from a valid from
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            # this way we will authenticate the user and create that user object
            account = authenticate(email=email, password=raw_password)
            # this way we will automatically login the user
            login(request, account)
            return redirect('home')
        else:
            # here we will pass the form to the template to display the errors
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            # this is how I get access to the email and password
            email = request.POST['email']
            password = request.POST['password']
            # here I authenticate the user
            user = authenticate(email=email, password=password)

            # if everything is okay, login the user
            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, "account/login.html", context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(
            # set initial properties. These are the values that are going to be displayed in the form as soon the user
            # visit his profile. His current username and email.
            initial={
                    "email": request.user.email,
                    "username": request.user.username,
                }
            )

    context['account_form'] = form

    return render(request, "account/account.html", context)