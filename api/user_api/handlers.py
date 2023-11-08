from fastapi.routing import APIRouter
from .dependencies import user_service
from .schemas import UserCreateSchema, UserSchema
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException

router = APIRouter(tags=["users"])

@router.post("/")
async def create_user(
    database: user_service,
    user: UserCreateSchema
    ):
    try:
        async with database.transaction() as session:
            new_user = database.create_user(
                session,
                user.user_name,
                user.user_surname,
                user.email,
                user.password
                )
        return UserSchema.moddel_validate(new_user)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
