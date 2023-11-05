from common.database.settings import BaseDatabaseSettings
from pydantic import AnyUrl

class UserDatabaseSettings(BaseDatabaseSettings):
    db_dsn: str = "postgresql+asyncpg://postgres:Weekend4532@localhost:5432/new_trms"
