"""Users views."""

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# App
from .forms import ProfileForm


def login_view(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})
        login(request, user)
        return redirect('feed')

    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    """Logout an user."""
    logout(request)
    return redirect('login')


def signup(request):
    """Signup view."""
    if request.method == 'POST':
        pass
    return render(request, 'users/signup.html')


@login_required
def update_profile(request):
    """Update an user's profile."""

    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']
            profile.save()

            return redirect('update_profile')
    else:
        form = ProfileForm()
    return render(request=request, template_name='users/update_profile.html',
                  context={'profile': profile, 'user': request.user, 'form': form})
