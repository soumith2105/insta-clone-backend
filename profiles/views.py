from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    UserCreationForm, UserChangeForm
)
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.views.generic import CreateView, UpdateView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class CreateProfileView(CreateView):
    template_name = 'profiles/signup_form.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save(commit=True)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect("/posts")


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profiles/update_profile.html'
    form_class = UserChangeForm

    def get_object(self):
        if self.request.user.is_authenticated:
            obj = get_object_or_404(UserProfile, username=self.request.user)
            return obj
        else:
            return redirect('/posts')

    def form_valid(self, form):
        form.save()
        return redirect('/posts')


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'profiles/update_profile.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = PasswordChangeForm(request.user or None)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('/posts')

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = PasswordChangeForm(request.user or None, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('/posts')
        else:
            return redirect('/posts')


class ProfileDetailView(DetailView):
    template_name = 'profiles/profile_info.html'
    context_object_name = 'profile'
    model = UserProfile

    def get_object(self):
        username = self.kwargs['username']
        obj = get_object_or_404(UserProfile, username=username)
        return obj

