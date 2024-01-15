from django.urls import path

from app.consumers import TaskConsumer,LongRunningTaskConsumer

ws_urlpatterns =[
    path('ws/task_status/<str:sim_id>/', LongRunningTaskConsumer.as_asgi()),
]