from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.store.db import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model


    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()


    async def get_all(self, db: Session, *, skip: int = 0, limit: int = 5000) -> List[ModelType]:
        return (
            db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()
        )


    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)

        await self._add_obj_to_database(db, db_obj)

        return db_obj


    async def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in

        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        await self._add_obj_to_database(db, db_obj)

        return db_obj


    async def delete(self, db: Session, *, id: int):
        db.query(self.model).filter(self.model.id == id).delete()
        db.commit()


    async def _add_obj_to_database(self, db: Session, obj):
        db.add(obj)
        db.commit()
        db.refresh(obj)


