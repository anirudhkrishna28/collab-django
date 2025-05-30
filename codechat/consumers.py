# import json
# from channels.generic.websocket import AsyncJsonWebsocketConsumer

# # In-memory code documents (for demo only; use Redis/DB for production)
# code_documents = {}

# class CollabConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         print("✅ Client connected")

#     async def disconnect(self, close_code):
#         print("❌ Client disconnected")

#     async def receive_json(self, content, **kwargs):
#         event = content.get("type")
#         data = content.get("data", {})
#         if event == "join":
#             await self.join(data)
#         elif event == "leave":
#             await self.leave(data)
#         elif event == "code_change":
#             await self.code_change(data)
#         elif event == "offer":
#             await self.offer(data)
#         elif event == "answer":
#             await self.answer(data)
#         elif event == "ice-candidate":
#             await self.ice_candidate(data)

#     async def join(self, data):
#         room = data.get("room")
#         await self.channel_layer.group_add(room, self.channel_name)
#         print(f"🔵 Client joined room: {room}")
#         # Send current code state to new user
#         await self.send_json({"type": "code_update", "code": code_documents.get(room, "")})

#     async def leave(self, data):
#         room = data.get("room")
#         await self.channel_layer.group_discard(room, self.channel_name)
#         print(f"🔴 Client left room: {room}")

#     async def code_change(self, data):
#         room = data.get("room")
#         code = data.get("code")
#         code_documents[room] = code
#         await self.channel_layer.group_send(
#             room,
#             {
#                 "type": "group.code_update",
#                 "code": code,
#                 "sender": self.channel_name
#             }
#         )

#     async def group_code_update(self, event):
#         # Don't send update to self (sender)
#         if event.get("sender") != self.channel_name:
#             await self.send_json({"type": "code_update", "code": event["code"]})

#     async def offer(self, data):
#         room = data.get("room")
#         offer = data.get("offer")
#         await self.channel_layer.group_send(
#             room,
#             {"type": "group.offer", "offer": offer, "sender": self.channel_name}
#         )

#     async def group_offer(self, event):
#         if event.get("sender") != self.channel_name:
#             await self.send_json({"type": "offer", "offer": event["offer"]})

#     async def answer(self, data):
#         room = data.get("room")
#         answer = data.get("answer")
#         await self.channel_layer.group_send(
#             room,
#             {"type": "group.answer", "answer": answer, "sender": self.channel_name}
#         )

#     async def group_answer(self, event):
#         if event.get("sender") != self.channel_name:
#             await self.send_json({"type": "answer", "answer": event["answer"]})

#     async def ice_candidate(self, data):
#         room = data.get("room")
#         candidate = data.get("candidate")
#         await self.channel_layer.group_send(
#             room,
#             {"type": "group.ice_candidate", "candidate": candidate, "sender": self.channel_name}
#         )

#     async def group_ice_candidate(self, event):
#         if event.get("sender") != self.channel_name:
#             await self.send_json({"type": "ice-candidate", "candidate": event["candidate"]})


import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# In-memory code documents (for demo only; use Redis/DB for production)
code_documents = {}
# In-memory chat history per room (for demo only)
chat_messages = {}

class CollabConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("✅ Client connected")

    async def disconnect(self, close_code):
        print("❌ Client disconnected")

    async def receive_json(self, content, **kwargs):
        event = content.get("type")
        data = content.get("data", {})
        if event == "join":
            await self.join(data)
        elif event == "leave":
            await self.leave(data)
        elif event == "code_change":
            await self.code_change(data)
        elif event == "offer":
            await self.offer(data)
        elif event == "answer":
            await self.answer(data)
        elif event == "ice-candidate":
            await self.ice_candidate(data)
        elif event == "chat_message":
            await self.chat_message(data)

    async def join(self, data):
        room = data.get("room")
        await self.channel_layer.group_add(room, self.channel_name)
        print(f"🔵 Client joined room: {room}")
        # Send current code state to new user
        await self.send_json({"type": "code_update", "code": code_documents.get(room, "")})
        # Send chat history to new user
        await self.send_json({"type": "chat_history", "messages": chat_messages.get(room, [])})

    async def leave(self, data):
        room = data.get("room")
        await self.channel_layer.group_discard(room, self.channel_name)
        print(f"🔴 Client left room: {room}")

    async def code_change(self, data):
        room = data.get("room")
        code = data.get("code")
        code_documents[room] = code
        await self.channel_layer.group_send(
            room,
            {
                "type": "group.code_update",
                "code": code,
                "sender": self.channel_name
            }
        )

    async def group_code_update(self, event):
        # Don't send update to self (sender)
        if event.get("sender") != self.channel_name:
            await self.send_json({"type": "code_update", "code": event["code"]})

    async def offer(self, data):
        room = data.get("room")
        offer = data.get("offer")
        await self.channel_layer.group_send(
            room,
            {"type": "group.offer", "offer": offer, "sender": self.channel_name}
        )

    async def group_offer(self, event):
        if event.get("sender") != self.channel_name:
            await self.send_json({"type": "offer", "offer": event["offer"]})

    async def answer(self, data):
        room = data.get("room")
        answer = data.get("answer")
        await self.channel_layer.group_send(
            room,
            {"type": "group.answer", "answer": answer, "sender": self.channel_name}
        )

    async def group_answer(self, event):
        if event.get("sender") != self.channel_name:
            await self.send_json({"type": "answer", "answer": event["answer"]})

    async def ice_candidate(self, data):
        room = data.get("room")
        candidate = data.get("candidate")
        await self.channel_layer.group_send(
            room,
            {"type": "group.ice_candidate", "candidate": candidate, "sender": self.channel_name}
        )

    async def group_ice_candidate(self, event):
        if event.get("sender") != self.channel_name:
            await self.send_json({"type": "ice-candidate", "candidate": event["candidate"]})

    # --- Chat functionality ---
    async def chat_message(self, data):
        room = data.get("room")
        username = data.get("username", "Anonymous")
        message = data.get("message", "")
        print(f"[CHAT_MSG] {room} {username}: {message}")  # <-- DEBUG
        if not message.strip():
            return
        chat_entry = {"username": username, "message": message}
        chat_messages.setdefault(room, []).append(chat_entry)
        await self.channel_layer.group_send(
            room,
            {
                "type": "group.chat_message",
                "username": username,
                "message": message,
            }
        )

    async def group_chat_message(self, event):
        print(f"[BROADCAST] {event}")  # <-- DEBUG
        await self.send_json({
            "type": "chat_message",
            "username": event["username"],
            "message": event["message"]
        })