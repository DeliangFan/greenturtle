
Greenturtle depends
- python >= 3.9
- mysql

This document will guide you to install the greenturtle step by step in ubuntu.

Initiate the repo

```
apt install software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt update
```

Install the python3.9, mysql and git.

```
apt install mysql-server git
apt-get install python3.9 python3.9-venv
```

Create the virtual environment
```
mkdir ~/.venvs
python3.9 -m venv ~/.venvs/greenturtle
source .venvs/greenturtle/bin/activate
```

Clone the greenturtle from github and install the python packages

```
git clone git@github.com:DeliangFan/greenturtle.git
pip install -r requirements.txt
```

Config mysql server in /etc/mysql/my.cnf with setting a large wait_timeout and interactive_timeout

```
[mysqld]
wait_timeout = 31536000
interactive_timeout = 31536000
```

Start mysql server

```
systemctl start mysql.service
```

Configure mysql server

```
CREATE DATABASE greenturtle;
CREATE USER 'greenturtle'@'localhost' IDENTIFIED BY '?';
GRANT ALL PRIVILEGES ON greenturtle.* TO 'greenturtle'@'localhost';
```

Copy and configure the greenturlte config file

```
mkdir /etc/greenturtle
cp etc/greenturtle/greenturtle.yaml /etc/greenturtle/
```

Create tables

```
python greenturtle/cmd/sync_db.py
```

[Optional] you need to download the data by download/download.py or insert data to the database directly.