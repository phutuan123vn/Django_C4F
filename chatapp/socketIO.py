from pprint import pprint
from socketio import AsyncServer, AsyncRedisManager, AsyncNamespace
from asgiref.sync import sync_to_async
from mysite import settings


mgr = AsyncRedisManager("redis://localhost:6379/0")
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
    room = data.get("room")
    message = data.get("message")
    print("SocketIO message", message, room)
    data = {
        "message": message,
        "room": room,
        "user": SIO.get_environ(sid)['asgi.scope']['user'].username
    }
    await SIO.emit("message", data, room=room, skip_sid=sid)
    
    
@SIO.on("join")
async def join(sid, room):
    print("SocketIO join", room)
    user = SIO.get_environ(sid)['asgi.scope']['user']
    print("User join", user, room)
    await SIO.enter_room(sid, room)
    await SIO.emit("message", f"Joined room {room} from server", room=room, skip_sid=sid)
    
@SIO.on("leave")
async def leave(sid,data):
    print("SocketIO leave", data)
    await SIO.leave_room(sid, data)
    await SIO.emit("message", f"Left room {data}")
    
