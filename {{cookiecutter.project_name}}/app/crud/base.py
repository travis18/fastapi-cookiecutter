from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
  def __init__(self, model: Type[ModelType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    **Parameters**

    * `model`: A SQLAlchemy model class
    * `schema`: A Pydantic model (schema) class
    """
    self.model = model

  def get(self, db: Session, id: Any) -> Optional[ModelType]:
    """
        search model by its primary key, only valid with 1 pk
    """
    return db.query(self.model).get(id)

  def get_multi(
    self, db: Session, *, skip: int = 0, limit: int = 100
  ) -> List[ModelType]:
    return db.query(self.model).offset(skip).limit(limit).all()

  def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
    """
    same as created_flush, but commit immediatly
    """
    db_obj = self.create_flush(db, obj_in=obj_in)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def create_flush(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
    """
    create a new record in db, but just flush it instead of commit \n
    useful when you want to create different records on different model and commit in same trasaction
    """
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = self.model(**obj_in_data)  # type: ignore
    db.add(db_obj)
    db.flush()
    return db_obj

  def update(
      self,
      db: Session,
      *,
      db_obj: ModelType,
      obj_in: Union[UpdateSchemaType, Dict[str, Any]]
  ) -> ModelType:
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
      update_data = obj_in
    else:
      update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
      if field in update_data:
          setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def remove(self, db: Session, *, id: int) -> ModelType:
    """
    same as remove_flush, but commit immediatly
    """
    obj = self.remove_flush(db=db, id=id)
    db.commit()
    return obj

  def remove_flush(self, db:Session, *, id: int) -> ModelType:
    """
    delete a record in db, but just flush it instead of commit \n
    useful when you want to delete different records on different model and commit in same trasaction. \n
    be careful of the dependencies between models
    """
    obj = db.query(self.model).get(id)
    db.delete(obj)
    db.flush()
    return obj