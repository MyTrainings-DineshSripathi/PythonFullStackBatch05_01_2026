from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope.get("user")

        print("🔌 WebSocket connect attempt")
        print("👤 User:", user)

        # Reject anonymous users
        if user is None or user.is_anonymous:
            print("❌ Anonymous user - connection rejected")
            await self.close()
            return

        # Accept connection
        await self.accept()
        print("✅ WebSocket connected")

        # Optional: join user-specific group
        # self.group_name = f"user_{user.userId}"
        self.group_name = f"user_{getattr(user, 'userId', 'unknown')}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        print("🔌 WebSocket disconnected")

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        print("📩 Message received:", text_data)

        # Echo (for testing)
        await self.send(text_data=json.dumps({
            "message": "Message received successfully"
        }))

    async def send_notification(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({
            "notification": message
        }))
        
        
# OLD ONE

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         user = self.scope.get('user')
#         if user is None or user.is_anonymous:
#             await self.close()
#             return

#         self.group_name = f'user_{user.userId}'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         if hasattr(self, 'group_name'):
#             await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def send_notification(self, event):
#         await self.send(text_data=json.dumps({
#             'event': event['event'],
#             'payload': event['payload'],
#         }))
