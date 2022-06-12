from typing import Optional, Union, Any, Dict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.store.models.users import User
from src.crud.base import CrudBase
from src.schemas.users import UserCreate, UserUpdate


class UserCrud(CrudBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()


    async def create(self, db: Session, *, obj_in: UserCreate) -> User:
        create_data = obj_in.dict()
        db_obj = User(**create_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


    async def update(self, db: Session, *, current_email: str, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:

        if not db_obj:
            raise HTTPException(
                status_code=400, detail=f"User with ID: {obj_in.id} not found.."
            )

        current_user = await self.get_by_email(db=db, email=current_email)

        if db_obj.id != current_user.id:
            raise HTTPException(
                status_code=403, detail="You can only update your info.."
            )

        if isinstance(obj_in, dict):
            update_data = obj_in

        else:
            update_data = obj_in.dict(exclude_unset=True)

        return await super().update(db, db_obj=db_obj, obj_in=update_data)


