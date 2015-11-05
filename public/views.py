from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from models import Subscribers
from django.contrib import messages
import re
# Create your views here.


def index(request):
    return render_to_response('public/index.html', context_instance=RequestContext(request))


def subscribe(request):
    email = request.POST['email']
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not email_regex.match(email):
        messages.error(request, 'email is not correct !')
    else:
        new_subscriber, created = Subscribers.objects.get_or_create(email=email)
        messages.success(request, 'you are successfully subscribed !')
    return HttpResponseRedirect(reverse('public:index'))
