# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def home(request):
	return render_to_response('website/index.html', {}, context_instance = RequestContext(request))