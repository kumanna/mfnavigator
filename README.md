# Mutual Fund NAVigator

This project is designed to create a database and provide analytics
for Indian mutual fund data.


## Installation

1. Install Python and create a virtualenv. Use the virtualenv.

2. Install the requisite dependencies:

```
pip3 install -r requirements.txt
```

3. Install the appropriate PostgreSQL package for your
   distribution. On Debian and Ubuntu, you can do

```
sudo apt-get install postgresql postgresql-client
```

## The database

To initialize the PostgreSQL data:

1. Create the project database `mfnavigator`. On Debian or Ubuntu, you can do this by:

```
createdb -O <username> mfnavigator
```

2. Then run
```
python3 manage.py makemigrations
python3 manage.py migrate

```
