# Create your views here.

import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings as cfg
from webapp.models_sepe import SepeProvince, SepeTown, SepeRegistry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import pymysql_sa
pymysql_sa.make_default_mysql_dialect()

ENGINE_STR = 'mysql://%s:%s@%s/rhok_desahucios' % (cfg.DESAHUCIOS_USER, cfg.DESAHUCIOS_PASSWORD, cfg.DESAHUCIOS_HOST)
ENGINE     = create_engine(ENGINE_STR, convert_unicode=True, pool_recycle=3600)
session    = scoped_session(sessionmaker(bind = ENGINE))

def index(request):
	return render_to_response('website/index.html', {}, context_instance = RequestContext(request))

def line_chart(request):
	return render_to_response('website/line_chart.html', {}, context_instance = RequestContext(request))

def other_chart(request):
	return render_to_response('website/other_chart.html', {}, context_instance = RequestContext(request))

def focus_context(request):
	return render_to_response('website/focus_context.html', {}, context_instance = RequestContext(request))

def province_json(request, province_name): 
    try:
        province = session.query(SepeProvince).filter_by(name = province_name).first()
        if province is None:
            return HttpResponse("Province not found")
        
        data = []
        for registry in province.registries:
            data.append({
                'month'      : registry.month,
                'year'       : registry.year,
                'unemployed' : registry.total,
            })
    finally:
        session.remove()

    return HttpResponse(json.dumps(data))

def town_json(request, province_name, town_name): 
    try:
        province = session.query(SepeProvince).filter_by(name = province_name).first()
        if province is None:
            return HttpResponse("Province not found")

        town = session.query(SepeTown).filter_by(name = town_name, province = province).first()
        if town is None:
            return HttpResponse("Town not found")
       
        data = []
        for registry in town.registries:
            data.append({
                'month'      : registry.month,
                'year'       : registry.year,
                'unemployed' : registry.total,
            })
    finally:
        session.remove()

    return HttpResponse(json.dumps(data))

def list_provinces(request):
    try:
        provinces = session.query(SepeProvince).all()
        return HttpResponse(json.dumps([ province.name for province in provinces ]))
    finally:
        session.remove()

def list_towns(request, province_name):
    print "En list_towns"
    try:
        province = session.query(SepeProvince).filter_by(name = province_name).first()
        if province is None:
            return HttpResponse("Province not found")
        towns = session.query(SepeTown).filter_by(province = province).all()
        return HttpResponse(json.dumps([ town.name for town in towns ]))
    finally:
        session.remove()

