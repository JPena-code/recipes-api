from fastapi import APIRouter

from app.core.deps.session import User

router = APIRouter()


@router.get('/me')
async def me(current_user: User):
    if not current_user:
        return {'User': 'No user'}
    return current_user
