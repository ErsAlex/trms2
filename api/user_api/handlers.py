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


@router.get('/me')
async def get_user(
    current_user: User = Depends(get_current_user)
    ):
    return UserSchema.moddel_validate(current_user)

@router.patch("/me")
async def update_user(
    database: user_service,
    updated_data: UserUpdateSchema,
    current_user: User = Depends(get_current_user)
    ):
    try:
        data = updated_data.model_dump()
        async with database.transaction() as session:
            user = await database.update_user(
            session=session,
            user_id=current_user.id,
            data=data
            )
            return UserSchema.moddel_validate(user)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@router.delete("/me")
async def delete_user(
    database: user_service,
    current_user: User = Depends(get_current_user)
    ):
    try:
        async with database.transaction() as session:
            response = await database.delete_user(
            session,
            id=current_user.id
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
        
            
    