# Create your views here.

import json

import pymysql_sa
pymysql_sa.make_default_mysql_dialect()

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings as cfg
from webapp.models_sepe import SepeProvince, SepeTown, SepeRegistry
from webapp.models_justizia import Municipio, PartidoJudicial, Desahucio

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


ENGINE_STR = 'mysql://%s:%s@%s/rhok_desahucios' % (cfg.DESAHUCIOS_USER, cfg.DESAHUCIOS_PASSWORD, cfg.DESAHUCIOS_HOST)
ENGINE     = create_engine(ENGINE_STR, convert_unicode=True, pool_recycle=3600)
session    = scoped_session(sessionmaker(bind = ENGINE))

def index(request):
	return render_to_response('website/index.html', {}, context_instance = RequestContext(request))

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
        gender   = request.GET.get('gender',   'all').lower()
        age      = request.GET.get('age',      'all').lower()

        province = session.query(SepeProvince).filter_by(name = province_name).first()
        if province is None:
            return HttpResponse("Province not found")


        if town_name.lower() == 'all':
            towns = session.query(SepeTown).filter_by(province = province).all()
            data = []
            for town in towns:
                registries = session.query(SepeRegistry).filter_by(town = town).all()

                town_results = []

                for registry in registries:
                    field = _get_field(gender, age)
                    if not isinstance(field, basestring):
                        return field

                    particular_data = getattr(registry, field)
                    town_results.append({
                        'year'       : registry.year,
                        'month'      : registry.month,
                        'unemployed' : particular_data
                    })
                data.append({
                    'town'    : town.name,
                    'results' : town_results
                })
            return HttpResponse(json.dumps(data))
                            
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

def show_desahucios(request, province_name, year, month):
    try:
        province = session.query(SepeProvince).filter_by(name = province_name).first()
        if province is None:
            return HttpResponse("Province not found")
        towns = session.query(SepeTown).filter_by(province = province).all()
        data = []
        for town in towns:
            municipio = session.query(Municipio).filter_by(nombre = town.name).first()
            if municipio is not None:
                desahucios = session.query(Desahucio).filter(Desahucio.municipio == municipio, sqlalchemy.extract('year', Desahucio.fecha) == int(year), sqlalchemy.extract('month', Desahucio.fecha) == int(month)).count()
                registry = session.query(SepeRegistry).filter_by(town = town, year = int(year), month = int(month)).first()
                if registry is not None:
                    data.append({
                        'town'       : town.name,
                        'desahucios' : desahucios,
                        'unemployed' : registry.total,
                    })
        return HttpResponse(json.dumps(data))
    finally:
        session.remove()

def show_desahucios_anyo(request, province_name, year):
    try:
        province = session.query(SepeProvince).filter_by(name = province_name).first()
        if province is None:
            return HttpResponse("Province not found")
        towns = session.query(SepeTown).filter_by(province = province).all()
        data = []
        for town in towns:
            municipio = session.query(Municipio).filter_by(nombre = town.name).first()
            if municipio is not None:
                desahucios = session.query(Desahucio).filter(Desahucio.municipio == municipio, sqlalchemy.extract('year', Desahucio.fecha) == int(year)).count()
                registries = session.query(SepeRegistry).filter_by(town = town, year = int(year)).all()
                total = 0
                for registry in registries:
                    total += registry.total

                data.append({
                        'town'       : town.name,
                        'desahucios' : desahucios,
                        'unemployed' : registry.total,
                    })
        return HttpResponse(json.dumps(data))
    finally:
        session.remove()

def _get_field(gender, age):
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
    return field

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
    
                field = _get_field(gender, age)
                if not isinstance(field, basestring):
                    return field

                particular_data = getattr(registry, field)
                
                data.append({
                    entity_name : entity.name,
                    'unemployment' : particular_data
                })
        
        return HttpResponse(json.dumps(data))
    finally:
        session.remove()

def show_unemployment_graph(request):
    return render_to_response('website/show_unemployment_chart.html', {}, context_instance = RequestContext(request))

def show_eviction_graph(request):
    return render_to_response('website/show_eviction_chart.html', {}, context_instance = RequestContext(request))

