from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

from .signals import user_logged_in

from .forms import *


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = 'venue:homeUrl'

    # def get(self, request, *args, **kwargs):
    #     print(self.request.GET.get('next'))
    #     return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request
        next_ = request.POST.get('next')
        next_post = request.GET.get('next')
        print('next', next_, next_post)
        redirect_path = next_ or next_post or None
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        auth = authenticate(request, password=password, username=username)
        print(redirect_path)
        print(request.get_host())
        if auth is not None:
            login(request, auth)
            user_logged_in.send(auth.__class__, instance=auth, request=request)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                print("not safe url")
                return redirect('venue:homeUrl')
            return redirect('account:login')
        else:
            print('auth is None')
            return redirect('account:login')

    def form_invalid(self, form):
        # print(form)
        print('form not valid')
        # print(dir(form))
        print(form.errors)
        return super().form_invalid(form)


class RegistrationView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = 'account/registration.html'
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        # current_site = get_current_site(request)
        # mail_subject = "Please Active your account to access Pro."
        # message = render_to_string('account/registration.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
        #     'token': account_activation_token.make_token(user)
        # })
        # to_email = form.clean_data.get('email')
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()
        # print("success")
        return super(RegistrationView, self).form_valid(form)


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
