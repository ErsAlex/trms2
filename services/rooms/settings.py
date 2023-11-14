from common.database.settings import BaseDatabaseSettings

class RoomDatabaseSettings(BaseDatabaseSettings):
    
    db_dsn: str = "postgresql+asyncpg://postgres:Weekend4532@localhost:5432/new_trms"
    
    # can assign, invite, promote, update rooms
    ROOM_ADMIN: str = "ROOM_ADMIN"
    # can assign task to users, create tasks and invite users
    ROME_LEAD: str = "ROME_LEAD"
    # can only take tasks
    ROOM_USER: str = "ROOM_USER"
