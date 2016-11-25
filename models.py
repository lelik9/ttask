# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Kpi(Base):
    __tablename__ = 'kpi'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(VARCHAR(length=255), unique=True, nullable=False)
    value = Column(Integer(), nullable=False)


class Results(Base):
    __tablename__ = 'results'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    ts = Column(TIMESTAMP(), default=datetime.now(), nullable=False)
    name = Column(VARCHAR(length=255), nullable=False)
    value = Column(Integer(), nullable=False)