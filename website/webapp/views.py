# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def index(request):
	return render_to_response('website/index.html', {}, context_instance = RequestContext(request))

def line_chart(request):
	return render_to_response('website/line_chart.html', {}, context_instance = RequestContext(request))

def other_chart(request):
	return render_to_response('website/other_chart.html', {}, context_instance = RequestContext(request))

def focus_context(request):
	return render_to_response('website/focus_context.html', {}, context_instance = RequestContext(request))