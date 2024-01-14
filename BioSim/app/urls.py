from django.urls import path,include
from app import views

urlpatterns = [

    path('',views.index,name="index"),
    path('run-simulation/',views.run_simulation,name="run_sumulation"),
]