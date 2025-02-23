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

"""api to access the database."""

import sqlalchemy
from sqlalchemy.orm import Session

from greenturtle.constants.future import types
from greenturtle.db import models


# pylint: disable=too-few-public-methods
class DBManager:
    """Database manager."""
    def __init__(self, db_conf):
        url = sqlalchemy.URL.create(
            drivername='mysql+pymysql',
            username=db_conf.username,
            password=db_conf.password,
            host=db_conf.host,
            port=db_conf.port,
            database=db_conf.database,
        )
        self.engine = sqlalchemy.create_engine(url)

    def create_all(self):
        """create all tables."""
        models.Base.metadata.create_all(self.engine)


class DBAPI:
    """Database API."""

    def __init__(self, db_conf):
        url = sqlalchemy.URL.create(
            drivername='mysql+pymysql',
            username=db_conf.username,
            password=db_conf.password,
            host=db_conf.host,
            port=db_conf.port,
            database=db_conf.database,
        )
        self.engine = sqlalchemy.create_engine(url)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def contract_create(self,
                        date,
                        name,
                        variety,
                        source,
                        country,
                        exchange,
                        group,
                        values):

        """create contract to the database."""

        contract = self.contract_get_by_constraint(
            date, name, variety, source, country)
        if contract:
            return contract

        contract_ref = models.Contract()
        contract_ref.update(values)
        contract_ref.id = None
        contract_ref.date = date
        contract_ref.name = name
        contract_ref.variety = variety
        contract_ref.source = source
        contract_ref.country = country
        contract_ref.exchange = exchange
        contract_ref.group = group

        with Session(self.engine) as session:
            session.add(contract_ref)
            session.commit()

        return contract_ref

    def contract_update_by_id(self, contract_id, values):
        """update contract to the database."""
        with Session(self.engine) as session:
            session.query(models.Contract).filter_by(
                id=contract_id).update(values)
            session.commit()

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def contract_get_by_constraint(self,
                                   date,
                                   name,
                                   variety,
                                   source,
                                   country):

        """get the contract from the database by constraint."""

        with Session(self.engine) as session:
            query = session.query(models.Contract).filter(
                models.Contract.date == date,
                models.Contract.name == name,
                models.Contract.variety == variety,
                models.Contract.source == source,
                models.Contract.country == country
            )
            return query.first()

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def contract_get_all_by_name_source_country(self, name, source, country):
        """get all contracts by name, source and country."""

        with Session(self.engine) as session:
            query = session.query(models.Contract).filter(
                models.Contract.name == name,
                models.Contract.source == source,
                models.Contract.country == country
            )
            return query.all()

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def contract_get_all_by_variety_source_country(self,
                                                   variety,
                                                   source,
                                                   country):
        """get all contracts by variety, source and country."""
        with Session(self.engine) as session:
            query = session.query(models.Contract).filter(
                models.Contract.variety == variety,
                models.Contract.source == source,
                models.Contract.country == country
            )
            return query.all()

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def contract_get_all_by_date_variety_source_country(self,
                                                        date,
                                                        variety,
                                                        source,
                                                        country):
        """get all contracts by variety, source and country."""
        with Session(self.engine) as session:
            query = session.query(models.Contract).filter(
                models.Contract.date == date,
                models.Contract.variety == variety,
                models.Contract.source == source,
                models.Contract.country == country
            )
            return query.all()

    def contract_get_all_by_exchange_from_akshare_cn(self, exchange):
        """get all contracts by exchange from akshare and country cn."""
        with Session(self.engine) as session:
            query = session.query(models.Contract).filter(
                models.Contract.exchange == exchange,
                models.Contract.source == types.AKSHARE,
                models.Contract.country == types.CN,
            )
            return query.all()

    def contract_get_all_by_name_from_csi_us(self, name):
        """get all contracts by name from csi data and country us."""
        return self.contract_get_all_by_name_source_country(
            name, types.CSI, types.US)

    def contract_get_all_by_name_from_akshare_cn(self, name):
        """get all contracts by name from akshare and country cn."""
        return self.contract_get_all_by_name_source_country(
            name, types.AKSHARE, types.CN)

    def contract_get_all_by_variety_from_csi_us(self, variety):
        """get all contracts by variety from csi data and country us."""
        return self.contract_get_all_by_variety_source_country(
            variety, types.CSI, types.US)

    def contract_get_all_by_variety_from_akshare_cn(self, variety):
        """get all contracts by variety from akshare and country cn."""
        return self.contract_get_all_by_variety_source_country(
            variety, types.AKSHARE, types.CN)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def continuous_contract_create(self,
                                   date,
                                   name,
                                   variety,
                                   source,
                                   country,
                                   exchange,
                                   group,
                                   values):

        """create continuous contract to the database."""

        continuous_contract = self.continuous_contract_get_by_constraint(
            date, name, variety, source, country)
        if continuous_contract:
            return continuous_contract

        continuous_contract_ref = models.ContinuousContract()
        continuous_contract_ref.update(values)
        continuous_contract_ref.id = None
        continuous_contract_ref.date = date
        continuous_contract_ref.name = name
        continuous_contract_ref.variety = variety
        continuous_contract_ref.source = source
        continuous_contract_ref.country = country
        continuous_contract_ref.group = group
        continuous_contract_ref.exchange = exchange

        with Session(self.engine) as session:
            session.add(continuous_contract_ref)
            session.commit()

        return continuous_contract_ref

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def continuous_contract_get_by_constraint(self,
                                              date,
                                              name,
                                              variety,
                                              source,
                                              country):

        """get the continuous contract from the database by constraint."""
        with Session(self.engine) as session:
            query = session.query(models.ContinuousContract).filter(
                models.ContinuousContract.date == date,
                models.ContinuousContract.name == name,
                models.ContinuousContract.variety == variety,
                models.ContinuousContract.source == source,
                models.ContinuousContract.country == country
            )
            return query.first()

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def continuous_contract_get_all_by_name_source_country(self,
                                                           name,
                                                           source,
                                                           country):

        """get all contracts by name, source and country."""
        with Session(self.engine) as session:
            query = session.query(models.ContinuousContract).filter(
                models.ContinuousContract.name == name,
                models.ContinuousContract.source == source,
                models.ContinuousContract.country == country
            )
            return query.all()

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def continuous_contract_get_all_by_variety_source_country(self,
                                                              variety,
                                                              source,
                                                              country):
        """get all continuous contracts by variety, source and country."""
        with Session(self.engine) as session:
            query = session.query(models.ContinuousContract).filter(
                models.ContinuousContract.variety == variety,
                models.ContinuousContract.source == source,
                models.ContinuousContract.country == country
            )

            return query.all()

    def continuous_contract_get_all_by_name_from_csi_us(self, name):
        """
        get all continuous contracts by name from csi data and country us.
        """
        return self.continuous_contract_get_all_by_name_source_country(
            name, types.CSI, types.US)

    def continuous_contract_get_all_by_name_from_akshare_cn(self, name):
        """
        get all continuous contracts by name from akshare and country cn.
        """
        return self.continuous_contract_get_all_by_name_source_country(
            name, types.AKSHARE, types.CN)

    def continuous_contract_get_all_by_variety_from_csi_us(self, variety):
        """
        get all continuous contracts by variety from csi data and country us.
        """
        return self.continuous_contract_get_all_by_variety_source_country(
            variety, types.CSI, types.US)

    def continuous_contract_get_all_by_variety_from_akshare_cn(self, variety):
        """
        get all continuous contracts by variety from akshare and country cn.
        """
        return self.continuous_contract_get_all_by_variety_source_country(
            variety, types.AKSHARE, types.CN)
