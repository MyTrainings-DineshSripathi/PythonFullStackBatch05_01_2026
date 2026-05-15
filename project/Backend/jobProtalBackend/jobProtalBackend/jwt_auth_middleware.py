from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from jwt import InvalidTokenError
from rest_framework_simplejwt.tokens import UntypedToken


class JwtAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "websocket":
            return await self.app(scope, receive, send)

        scope["user"] = await self.get_user(scope)

        return await self.app(scope, receive, send)

    async def get_user(self, scope):
        try:
            query_string = scope.get("query_string", b"").decode()
            params = parse_qs(query_string)

            token = params.get("token", [None])[0]

            if not token:
                print("❌ No token provided")
                return AnonymousUser()

            # Validate token
            validated_token = UntypedToken(token)

            # Handle different token formats
            # user_id = (
            #     validated_token.get("user_id")
            #     or validated_token.get("userId")
            #     or validated_token.get(settings.SIMPLE_JWT.get("USER_ID_CLAIM", "user_id"))
            # )
            
            user_id = (
                validated_token.get("userId")   # ✅ your main field
                or validated_token.get("user_id")
            )
            
            print(validated_token)

            if not user_id:
                print("❌ user_id not found in token")
                return AnonymousUser()

            User = get_user_model()
            user = await database_sync_to_async(User.objects.get)(userId=user_id)

            print(f"✅ Authenticated user: {user}")
            return user

        except InvalidTokenError:
            print("❌ Invalid token")
            return AnonymousUser()

        except Exception as e:
            print(f"❌ Middleware error: {str(e)}")
            return AnonymousUser()

# OLD AUTH

# from urllib.parse import parse_qs
# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
# from django.conf import settings
# from jwt import InvalidTokenError
# from rest_framework_simplejwt.tokens import UntypedToken


# class JwtAuthMiddleware:
#     def __init__(self, app):
#         self.app = app

#     async def __call__(self, scope, receive, send):
#         # Only process websocket connections
#         if scope["type"] != "websocket":
#             return await self.app(scope, receive, send)

#         # Get user from JWT token
#         user = await self.get_user(scope)
#         scope['user'] = user

#         return await self.app(scope, receive, send)

#     async def get_user(self, scope):
#         query_string = scope.get('query_string', b'').decode('utf-8')
#         params = parse_qs(query_string)
#         token = None

#         if 'token' in params:
#             token = params['token'][0]

#         if not token:
#             return AnonymousUser()

#         try:
#             raw_token = token.strip()
#             validated_token = UntypedToken(raw_token)
#             user_id_claim = settings.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')
#             user_id = validated_token.get(user_id_claim) or validated_token.get('user_id')
#             if user_id is None:
#                 return AnonymousUser()

#             field_name = settings.SIMPLE_JWT.get('USER_ID_FIELD', 'id')
#             User = get_user_model()
#             user = await database_sync_to_async(User.objects.get)(**{field_name: user_id})
#             return user
#         except Exception:
#             return AnonymousUser()
#             return user
#         except (InvalidTokenError, Exception):
#             return AnonymousUser()

