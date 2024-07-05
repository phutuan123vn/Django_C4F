from pprint import pprint
from socketio import AsyncServer, AsyncRedisManager, AsyncNamespace
from asgiref.sync import sync_to_async
from mysite import settings
from chatapp.models import Message
import os

url = "redis://"+ os.getenv("REDIS","localhost") + ":6379"
mgr = AsyncRedisManager(url)
SIO = AsyncServer(
    async_mode="asgi",
    # logger=True,
    # engineio_logger=True,
    client_manager=mgr,
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
)



@SIO.on("connect")
async def connect(sid, env, auth):
    print("SocketIO connect", sid)


@SIO.on("disconnect")
async def disconnect(sid):
    print("SocketIO disconnect")
    

@SIO.on("message")
async def message(sid, data):
    room = data.get('room')
    user = SIO.get_environ(sid)['asgi.scope']['user']
    msg = await save_msg(user=user, **data)
    data = {
        "value": msg.value,
        "username": user.username,
        "date": msg.date.strftime("%Y-%m-%d %H:%M:%S")
    }
    await SIO.emit("message", data, room=room, skip_sid=sid)
    
    
@SIO.on("join")
async def join(sid, room):
    print("SocketIO join", room)
    user = SIO.get_environ(sid)['asgi.scope']['user']
    print("User join", user, room)
    await SIO.enter_room(sid, room)
    # await SIO.emit("message", f"Joined room {room} from server", room=room, skip_sid=sid)
    
@SIO.on("leave")
async def leave(sid,data):
    print("SocketIO leave", data)
    await SIO.leave_room(sid, data)
    # await SIO.emit("message", f"Left room {data}") 
    
@sync_to_async
def save_msg(room, message, user, **kwargs):
    room_id = room.split('room_id_')[-1]
    msg = Message.objects.create(room_id=room_id, value=message, user=user)
    msg.save()
    return msg