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

"""utils for greenturtle database"""

from sqlalchemy import create_engine
from sqlalchemy import URL


def create_mysql_engine(conf):
    """create a mysql engine"""
    url = URL.create(
        drivername='mysql+pymysql',
        username=conf.db.username,
        password=conf.db.password,
        host=conf.db.host,
        port=conf.db.port,
        database=conf.db.database,
    )

    engine = create_engine(url)

    return engine
