from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from .forms import contactForm
# Create your views here.
def home(request):
    context = locals()
    template = 'home.html'
    return render(request, template, context)

def contact(request):
    form = contactForm(request.POST or None)

    if(form.is_valid()):
        print(form.cleaned_data['email'])
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        subject = 'Message from mysite'
        message = '{} {}'.format(comment, name)
        emailFrom = form.cleaned_data['email']
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail( subject, message, emailFrom,
                   emailTo, fail_silently=False
        )
    context = locals()
    template = 'contact.html'
    return  render(request, template, context)

def about(request):
    context = locals()
    template = 'about.html'
    return  render(request, template, context)