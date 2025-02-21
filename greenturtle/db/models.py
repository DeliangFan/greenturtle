# Copyright (c) 2025 GreenTurtle
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""models for the greenturtle database."""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase


# pylint: disable=too-few-public-methods
class Base(DeclarativeBase):
    """base model"""


# pylint: disable=too-few-public-methods
class Contract(Base):
    """contract model"""
    __tablename__ = 'contract'

    __table_args__ = (
        UniqueConstraint(
            'date',
            'name',
            'variety',
            'source',
            'country',
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, index=True, nullable=False)
    name = Column(String(31), index=True, nullable=False)
    variety = Column(String(31), index=True, nullable=False)
    source = Column(String(31), index=True, nullable=False)
    country = Column(String(31), index=True, nullable=False)
    exchange = Column(String(31))
    group = Column(String(31))
    open = Column(Float, default=None)
    high = Column(Float, default=None)
    low = Column(Float, default=None)
    close = Column(Float, default=None)
    volume = Column(Integer, default=0)
    open_interest = Column(Integer, default=0)
    total_volume = Column(Integer, default=0)
    total_open_interest = Column(Integer, default=0)
    expire = Column(DateTime)


# pylint: disable=too-few-public-methods
class ContinuousContract(Base):
    """continuous contract model"""
    __tablename__ = 'continuous_contract'

    __table_args__ = (
        UniqueConstraint(
            'date',
            'name',
            'variety',
            'source',
            'country',
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, index=True, nullable=False)
    name = Column(String(31), index=True, nullable=False)
    variety = Column(String(31), index=True, nullable=False)
    source = Column(String(31), nullable=False)
    country = Column(String(31), nullable=False)
    exchange = Column(String(31))
    group = Column(String(31))
    open = Column(Float, default=None)
    high = Column(Float, default=None)
    low = Column(Float, default=None)
    close = Column(Float, default=None)
    volume = Column(Integer, default=0)
    open_interest = Column(Integer, default=0)
    total_volume = Column(Integer, default=0)
    total_open_interest = Column(Integer, default=0)
    expire = Column(DateTime)
    adjust_factor = Column(Float, default=None)
