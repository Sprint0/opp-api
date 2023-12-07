from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
import datetime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    surname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String)
    accounts = relationship('Account', back_populates='user')


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    balance = Column(Float)
    user = relationship('Users', back_populates='accounts')


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    from_account_id = Column(Integer, ForeignKey('accounts.id'))
    to_account_id = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    from_account = relationship("Account", foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])
