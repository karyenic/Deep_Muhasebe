# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    # diÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸er alanlar...
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    email = Column(String, unique=True, index=True)
    firm_id = Column(Integer, ForeignKey("firms.id"))




