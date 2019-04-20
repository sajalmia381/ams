from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

# Registration
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.http import HttpResponse

from .signals import user_logged_in

from .forms import *

from django.contrib import messages


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    # success_url = 'page:index'

    def form_valid(self, form):
        request = self.request
        next_ = request.POST.get('next')
        next_post = request.GET.get('next')
        redirect_path = next_ or next_post or None
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        auth = authenticate(request, password=password, username=username)
        if auth is not None:
            login(request, auth)
            user_logged_in.send(auth.__class__, instance=auth, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                pass
                # return redirect('page:index')
            return redirect('account:login')
        else:
            # messages.add_message(request, messages.error, 'Password Or Username not Valid')
            return redirect('account:login')

    def form_invalid(self, form):
        print(form)
        return redirect('account:login')


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
