from django.shortcuts import render
from attendance.forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login")
def home(request):
    return render(request, 'attendance/home.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid(): # Checks if all form fields is correct
            user = form.save() # Creates new user and saves into database then assigns it to user variable
            login(request, user) # Logs in newly created user
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {"form": form})