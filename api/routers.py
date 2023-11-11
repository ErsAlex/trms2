from .user_api.handlers import router as user_router
from .user_api.auth.login import router as login_router
from api.room_api.rooms.handlers import router as room_router


all_routers = [user_router, login_router, room_router]