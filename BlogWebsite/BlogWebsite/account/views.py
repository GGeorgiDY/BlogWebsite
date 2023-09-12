from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm


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
