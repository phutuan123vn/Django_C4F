from pprint import pprint
from socketio import AsyncServer, AsyncRedisManager
from asgiref.sync import sync_to_async
from mysite import settings


mgr = AsyncRedisManager("redis://localhost:6379/0")
SIO = AsyncServer(
    async_mode="asgi",
    logger=True,
    engineio_logger=True,
    client_manager=mgr,
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
)



@SIO.on("connect")
async def connect(sid, env, auth):
    # chat_id = auth["chat_id"] 
    pprint(env)
    scope = env['asgi.scope']
    pprint(scope)
    session = scope.get("session", None)
    session = dir(session) 
    print(session)
    pprint(session)
    print("SocketIO connect" , sid, env, auth)
    # SIO.enter_room(sid, 2)
    # await SIO.emit("connect", f"Connected as {sid}") 
    # await SIO.emit("message", f"Connected as {sid}")


@SIO.on("disconnect")
async def disconnect(sid):
    print("SocketIO disconnect")
    

@SIO.on("message")
async def message(sid, data):
    print("SocketIO message receive", data)
    await SIO.emit("message", data + ' from server')
    
    
@SIO.on("join")
async def join(sid, data):
    print("SocketIO join", data)
    await SIO.enter_room(sid, data)
    await SIO.emit("message", f"Joined room {data}")
    
@SIO.on("leave")
async def leave(sid,data):
    print("SocketIO leave", data)
    await SIO.leave_room(sid, data)
    await SIO.emit("message", f"Left room {data}")
    
