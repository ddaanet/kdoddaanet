from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import (
    LoginForm,
    UserEditForm,
    UserRegistrationForm,
)


def user_login(request):
    """Login view."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd["username"],
                password=cd["password"],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request):
    """Dashboard view."""
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request):
    """Register a new user."""
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            return redirect("register_done")
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


def register_done(request):
    """Registration complete."""
    return render(request, "account/register_done.html")


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect("dashboard")
    else:
        user_form = UserEditForm(instance=request.user)
    return render(
        request,
        "account/edit.html",
        {
            "user_form": user_form,
        },
    )

def logout_done(request):
    """Logout complete."""
    return render(request, "registration/logged_out.html")
