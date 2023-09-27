from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterUserForm, LoginUserForm, UpdateUserForm, CustomProfileForm
from .models import CustomProfile

from mainapp.views import SidebarData


class RegisterUserView(SidebarData, CreateView):
    form_class = RegisterUserForm
    template_name = 'authentication/auth/register.html'

    def form_valid(self, form):
        user = form.save()
        CustomProfile.objects.create(user=user, profile_pic='default_profile_pic.jpg')
        login(self.request, user)

        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration'

        return context


class LoginUserView(SidebarData, LoginView):
    form_class = LoginUserForm
    template_name = 'authentication/auth/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'

        return context


def logout_user(request):
    logout(request)
    return redirect('login')


class ProfilePageView(SidebarData, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'authentication/user/profile_page.html'
    context_object_name = 'user_info'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['change_profile_pic_form'] = CustomProfileForm()

        return context


class UpdateUserView(SidebarData, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    context_object_name = 'form'
    template_name = 'authentication/user/update_user.html'
    login_url = reverse_lazy('home')
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update your personal information'

        return context

    def get_success_url(self):
        return reverse_lazy('profile_page', kwargs={'username': self.object.username})


class UserDeleteView(SidebarData, LoginRequiredMixin, DeleteView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    success_url = reverse_lazy('register')
    login_url = reverse_lazy('home')


class ChangeProfilePicView(SidebarData, LoginRequiredMixin, UpdateView):
    model = CustomProfile
    form_class = CustomProfileForm
    login_url = reverse_lazy('home')
    pk_url_kwarg = 'user_id'

    def get_success_url(self):
        return reverse_lazy('profile_page', kwargs={'username': self.object.user.username})

