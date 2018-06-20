import json
import urllib

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import contactForm
from .decorators import check_recaptcha

# Create your views here.
def home(request):
    title = 'Home'
    context = {'title': title, }
    template = 'home.html'
    return render(request, template, context)

def contact(request):
    title = 'Contact'
    confirm_message = None
    template = 'contact.html'

    if request.method == 'POST' :
        form = contactForm(request.POST or None)

        if(form.is_valid()):
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                messages.success(request, 'Terima kasih sudah mengubungi kami')
                name = form.cleaned_data['name']
                comment = form.cleaned_data['comment']
                subject = 'Message from mysite'
                emailFrom = form.cleaned_data['email']
                message = '{}, by {} ; from email : {}'.format(comment, name, emailFrom)
                emailTo = [settings.EMAIL_HOST_USER]
                send_mail(subject, message, emailFrom,
                          emailTo, fail_silently=False
                          )
                title = 'Thanks!'
                confirm_message = 'Terima kasih sudah menghubungi kami, kami akan segera menghubungi kamu kembali.'
                form = None
            else:
                messages.error(request, 'Invalid captcha!!!')
    else:
        form = contactForm()

    context = {'title': title, 'confirm_message': confirm_message, 'form': form}
    return  render(request, template, context)

@check_recaptcha
def contact__versi_dua(request):
    title = 'Contact'
    confirm_message = None
    template = 'contact.html'

    if request.method == 'POST' :
        form = contactForm(request.POST or None)
        if(form.is_valid() and request.recaptcha_is_valid):
            messages.success(request, 'Terima kasih sudah mengubungi kami')
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            subject = 'Message from mysite'
            emailFrom = form.cleaned_data['email']
            message = '{}, by {} ; from email : {}'.format(comment, name, emailFrom)
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, emailFrom,
                      emailTo, fail_silently=False
                      )
            title = 'Thanks!'
            confirm_message = 'Terima kasih sudah menghubungi kami, kami akan segera menghubungi kamu kembali.'
            form = None
    else:
        form = contactForm()

    context = {'title': title, 'confirm_message': confirm_message, 'form': form}
    return  render(request, template, context)


def about(request):
    title = 'About'
    context = {'title': title, }
    template = 'about.html'
    return  render(request, template, context)