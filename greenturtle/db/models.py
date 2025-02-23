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
from sqlalchemy.sql import func


# pylint: disable=too-few-public-methods
class Base(DeclarativeBase):
    """base model"""

    # pylint: disable=E1102
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in values.items():
            setattr(self, k, v)

    def to_dict(self):
        """attribute to dict."""

        attr_dict = self.__dict__.copy()
        attr_dict.pop("_sa_instance_state", None)
        attr_dict.pop("id", None)
        attr_dict.pop("created_at", None)
        attr_dict.pop("updated_at", None)

        return attr_dict


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
    exchange = Column(String(31), default=None)
    group = Column(String(31), default=None)
    open = Column(Float, default=None)
    high = Column(Float, default=None)
    low = Column(Float, default=None)
    close = Column(Float, default=None)
    volume = Column(Integer, default=None)
    open_interest = Column(Integer, default=None)
    total_volume = Column(Integer, default=None)
    total_open_interest = Column(Integer, default=None)
    turn_over = Column(Float, default=None)
    settle = Column(Float, default=None)
    pre_settle = Column(Float, default=None)
    expire = Column(DateTime, nullable=False)


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
    source = Column(String(31), index=True, nullable=False)
    country = Column(String(31), index=True, nullable=False)
    exchange = Column(String(31), default=None)
    group = Column(String(31), default=None)
    open = Column(Float, default=None)
    high = Column(Float, default=None)
    low = Column(Float, default=None)
    close = Column(Float, default=None)
    volume = Column(Integer, default=None)
    open_interest = Column(Integer, default=None)
    total_volume = Column(Integer, default=None)
    total_open_interest = Column(Integer, default=None)
    turn_over = Column(Float, default=None)
    settle = Column(Float, default=None)
    pre_settle = Column(Float, default=None)
    expire = Column(DateTime, nullable=False)
    adjust_factor = Column(Float, nullable=False)
