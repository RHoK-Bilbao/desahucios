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
    try:
        province = session.query(SepeProvince).filter_by(name = province_name).first()
        if province is None:
            return HttpResponse("Province not found")
        towns = session.query(SepeTown).filter_by(province = province).all()
        return HttpResponse(json.dumps([ town.name for town in towns ]))
    finally:
        session.remove()

def show_province_year_month(request, province_name, year, month):
    try:
        gender   = request.GET.get('gender',   'all').lower()
        age      = request.GET.get('age',      'all').lower()

        if province_name.lower() == 'all':
            entity_name = 'province'
            towns = False
            entities = session.query(SepeProvince).all()
        else:
            towns = True
            entity_name = 'town'
            province = session.query(SepeProvince).filter_by(name = province_name).first()
            if province is None:
                return HttpResponse("Province not found")
            entities = session.query(SepeTown).filter_by(province = province).all()

        data = []
        for entity in entities:
            if towns:
                registry = session.query(SepeRegistry).filter_by(town = entity, year = int(year), month = int(month)).first()
            else:
                registry = session.query(SepeRegistry).filter_by(province = entity, year = int(year), month = int(month)).first()

            if registry is not None:
                if gender == 'all':
                    if age == 'all':
                        field = 'total'
                    elif '25' in age:
                        field = 'less_25'
                    elif '45' in age:
                        field = 'less_45'
                    elif 'older' in age:
                        field = 'older'
                    else:
                        return HttpResponse("invalid age")
                elif gender == 'men':
                    if age == 'all':
                        field = 'men'
                    elif '25' in age:
                        field = 'men_less_25'
                    elif '45' in age:
                        field = 'men_less_45'
                    elif 'older' in age:
                        field = 'men_older'
                    else:
                        return HttpResponse("invalid age")
                elif gender == 'women':
                    if age == 'all':
                        field = 'women'
                    elif '25' in age:
                        field = 'women_less_25'
                    elif '45' in age:
                        field = 'women_less_45'
                    elif 'older' in age:
                        field = 'women_older'
                    else:
                        return HttpResponse("invalid age")
                else:
                    return HttpResponse("invalid gender")

                particular_data = getattr(registry, field)
                
                data.append({
                    entity_name : entity.name,
                    'unemployment' : particular_data
                })
        
        return HttpResponse(json.dumps(data))
    finally:
        session.remove()

def show_unemployment_graph(request, municipio):
    if(municipio):
        pass
    else:
        pass
    return render_to_response('website/show_unemployment_chart.html', {
            '': '',
        },
        context_instance = RequestContext(request))
