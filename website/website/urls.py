from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$',                       'webapp.views.index',           name='index'),
    url(r'^province/(\w+)/$',       'webapp.views.province_json',   name='province_json'),
    url(r'^province/(\w+)/(\w+)/$', 'webapp.views.town_json',       name='town_json'),
    url(r'^province/(\w+)/(\d+)/(\d+)/$',  'webapp.views.show_province_year_month',   name='show_province_year_month'),
    url(r'^provinces/?$',            'webapp.views.list_provinces',  name='list_provinces'),
    url(r'^provinces/(\w+)/?$',      'webapp.views.list_towns',      name='list_towns'),
    url(r'^desahucios/(\w+)/(\d+)/(\d+)/$', 'webapp.views.show_desahucios', name = 'show_desahucios'),
    url(r'^desahucios/(\w+)/(\d+)/$', 'webapp.views.show_desahucios_anyo', name = 'show_desahucios_anyo'),
    url(r'^other_chart/$',           'webapp.views.other_chart',     name='other_chart'),
   

    url(r'^unemployment_graph/$', 'webapp.views.show_unemployment_graph', name = 'show_unemployment_graph'),
    url(r'^eviction_graph/$', 'webapp.views.show_eviction_graph', name = 'show_eviction_graph'),

    # url(r'^website/', include('website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
