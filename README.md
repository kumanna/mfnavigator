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

3. Now, you need to create the AMCs. Currently, this has been done
manually and will be automated soon.

4. To import NAVs to the database, you can run this:

```
python3 manage.py importnavs --amcid <amcid> --amfinumber <mfnumber> --mfname <mfname> --navfile <amfi_nav_file>
```

For example, for Birla Sun Life Frontline Equity - Growth, we can run
```
python3 manage.py importnavs --amcid 3 --amfinumber 103174 --mfname "Birla Sun Life Frontline Equity Fund-Growth" --navfile BSLNAVs.txt
```
where `BSLNAVs.txt` is downloaded from the AMFI website.
