from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.htmlform,name='htmlform'),
    path("analyze",views.analyze,name='analyze'),
    path("features",views.features,name='features'),
    path("contactus",views.contact,name='contact'),
    path("aboutus",views.about,name='about'),
]
