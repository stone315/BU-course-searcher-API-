from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index),
    re_path(r'api/(?P<sem>(?:Fall|Summer|Spring))/(?P<year>[0-9]{4})/(?P<keyword>[a-zA-Z_]+)/(?P<credit>[012345+any]+)/(?P<school>[A-Z_]{3})/(?P<major>[A-Z_]{2})/(?P<time>[MTWRF_]+)(?:/(?P<condition>(?:Class_Closed|Class_Full)))?/$',views.api, name='api')
]


# sem : Fall/Summer/Spring
# year: any 4 digits
# keyword: Any string and replace space(' ') with + , ____ for no keyworld
# credits: 0,1,2,3,4,5+, any
# school: ___(for no input),CAS,ENG ...
# major: AA,AH,ME...., __(for no input)
# time: Any combination of M,T,W,R,F and _(for no input)
# condition (optional input) : Class_Closed or Class_Full