
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path

# from channels.security.websocket import AllowedHostsOriginValidator
# from app.consumers import LongRunningTaskConsumer,TaskConsumer

# application = ProtocolTypeRouter(
#     {   
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(
#             URLRouter(
#                 [
#                     # path("ws/task_status/", LongRunningTaskConsumer.as_asgi()),
#                     path("ws/task_status/", TaskConsumer.as_asgi()),
#                 ]
#             )
#         ),
#         )
#     }
# )


from django.urls import path

from app.consumers import TaskConsumer,LongRunningTaskConsumer

ws_urlpatterns =[
    path('ws/task_status/', LongRunningTaskConsumer.as_asgi()),
]