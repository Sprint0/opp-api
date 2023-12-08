import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from db.database import Base


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
    accounts = relationship("Account", back_populates="user")
    debt_cards = relationship("DebitCard", back_populates="user")
    credit_cards = relationship("CreditCard", back_populates="user")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    balance = Column(Float)
    user = relationship("Users", back_populates="accounts")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id"))
    to_account_id = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    from_account = relationship("Account", foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])


class DebitCard(Base):
    __tablename__ = "debt_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, unique=True)
    expiration_date = Column(String)
    cvv = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="debt_cards")


class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, unique=True)
    expiration_date = Column(String)
    cvv = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="credit_cards")
