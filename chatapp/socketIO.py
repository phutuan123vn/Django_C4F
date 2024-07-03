import daphne.server
import socketio
from asgiref.sync import sync_to_async
from mysite import settings
from mysite.asgi import SIO



@SIO.on("connect")
async def connect(sid, env, auth):
    # chat_id = auth["chat_id"] 
    print("SocketIO connect" , sid, env, auth)
    SIO.enter_room(sid, 2)
    await SIO.emit("connect", f"Connected as {sid}") 
    await SIO.emit("message", f"Connected as {sid}")


@SIO.on("disconnect")
async def disconnect(sid):
    print("SocketIO disconnect")
    

@SIO.on("message")
async def message(sid, data):
    print("SocketIO message receive", data)
    await SIO.emit("message", data + ' from server')
    
