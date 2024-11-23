from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.user import User, UserCreate, PasswordChange, UserUpdate
from app.services.user import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    update_user,
    change_password
)

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    注册新用户
    """
    # 检查邮箱是否已被注册
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册",
        )
    
    # 检查用户名是否已被使用
    user = await get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被使用",
        )
    
    # 创建新用户
    user = await create_user(db, user_in)
    return user 

@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取当前用户信息
    """
    return current_user

@router.put("/me", response_model=User)
async def update_user_info(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新当前用户信息
    """
    # 检查邮箱是否被其他用户使用
    if user_in.email and user_in.email != current_user.email:
        user = await get_user_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被使用",
            )
    
    # 检查用户名是否被其他用户使用
    if user_in.username and user_in.username != current_user.username:
        user = await get_user_by_username(db, username=user_in.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该用户名已被使用",
            )
    
    user = await update_user(db, current_user, user_in)
    return user

@router.post("/me/password", response_model=dict)
async def change_user_password(
    *,
    db: AsyncSession = Depends(deps.get_db),
    password_data: PasswordChange,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    修改当前用户密码
    """
    if not await change_password(
        db, current_user, password_data.current_password, password_data.new_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误",
        )
    return {"message": "密码修改成功"}