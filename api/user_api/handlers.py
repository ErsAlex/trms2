from fastapi.routing import APIRouter
from .dependencies import user_service, get_current_user
from .schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from models.models  import User
from fastapi import Depends

router = APIRouter(tags=["users"])

@router.post("/")
async def create_user(
    database: user_service,
    user: UserCreateSchema
    ):
    try:
        async with database.session.begin():
            new_user = await database.create_user(
                session=database.session,
                user_name=user.user_name,
                user_surname=user.user_surname,
                email=user.email,
                password=user.password
                )
        return UserSchema.model_validate(new_user)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.get('/me')
async def get_user(
    current_user: User = Depends(get_current_user)
    ):
    return UserSchema.model_validate(current_user)

@router.patch("/me")
async def update_user(
    database: user_service,
    updated_data: UserUpdateSchema,
    current_user: User = Depends(get_current_user)
    ):
    try:
        data = updated_data.model_dump()
        async with database.session.begin():
            user = await database.update_user(
            session=database.session,
            user_id=current_user.id,
            data=data
            )
            return UserSchema.model_validate(user)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@router.delete("/me")
async def delete_user(
    database: user_service,
    current_user: User = Depends(get_current_user)
    ):
    try:
        async with database.session.begin():
            response = await database.delete_user(
            database.session,
            id=current_user.id
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
        
            
    