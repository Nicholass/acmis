##CMS for urban exploration blog engine
###Setup

Copy .env.example to .env and fill your parameters.

Build container:
```
docker-compose up -d
```

Prepare db with psql:
```
create database diggers;
create user diggers with encrypted password 'securepass';
grant all privileges on database diggers to diggers;
alter database diggers OWNER TO diggers;
exit
```

If you have existing db dump import it to db.
```
psql -U diggers < dump.sql
```

Run following command:
```
docker-compose exec web ./manage.py deploy
```

###VirtualEnv for Development code hinting

```
pip install virtualenv
сd ./app
virtualenv --python=python3.6 --prompt="DIG" diggers_venv
source ./diggers_venv/bin/activate
pip install -r ./requirements.txt
```
