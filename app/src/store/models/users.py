from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.store.db import Base
from src.store.hashing_password import verify_password, get_password_hash


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))


    def __init__(self, first_name, last_name, email, password, *args, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = get_password_hash(password)


    def check_password(self, password):
        return verify_password(self.password, password)

    def to_dict(self):
        return dict([(k, getattr(self, k)) for k in self.__dict__.keys() if not k.startswith("_")])


