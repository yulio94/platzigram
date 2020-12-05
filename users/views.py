"""Users views."""

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
# Forms
from users.forms import SignupForm

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile


class LoginView(auth_views.LoginView):
    """Login users view"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout users view"""
    template_name = 'users/logged_out.html'


@login_required
def logout_view(request):
    """Logout an user."""
    logout(request)
    return redirect('users:login')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update user view"""
    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self, queryset=None):
        """Return user's profile"""
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile"""
        username = self.request.user.username
        return reverse('users:detail',
                       kwargs={'username': username})


class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view"""

    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context


class SignupView(FormView):
    """User sign up view"""
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data"""
        form.save()
        return super().form_valid(form)
