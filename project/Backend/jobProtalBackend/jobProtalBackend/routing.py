# import os
# import django
# from django.core.asgi import get_asgi_application

# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import re_path

# from .jwt_auth_middleware import JwtAuthMiddleware
# from jobs.consumers import NotificationConsumer

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
# django.setup()

# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,

#     "websocket": JwtAuthMiddleware(
#         URLRouter([
#             re_path(r"^ws/notifications/$", NotificationConsumer.as_asgi()),
#         ])
#     ),
# })

# from django.urls import re_path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from .jwt_auth_middleware import JwtAuthMiddleware
# from jobs.consumers import NotificationConsumer

# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     'http': django_asgi_app,
#     'websocket': JwtAuthMiddleware(
#         URLRouter([
#             re_path(r'^ws/notifications/$', NotificationConsumer.as_asgi()),
#         ])
#     ),
# })
