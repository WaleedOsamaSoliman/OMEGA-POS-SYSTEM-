from django.urls import path
from .views import index , login , requests , logout , panel , admin_requests , marakez


urlpatterns = [

    path("" , index , name = 'index'),
    path("login" , login , name = 'login'),
    path("requests" , requests , name = 'requests'),
    path("admin-requests" , admin_requests , name = 'admin-requests'),
    path("logout" , logout , name = 'logout'),
    path("panel" , panel , name = 'panel'),
    path("marakez" , marakez , name = 'marakez')

]