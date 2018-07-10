`CMS for urban exploration blog engine`

`=Setup=`

```shell
docker-compose up
docker-compose exec web ./manage.py deploy
```

`==VirtualEnv for Developmentcode hinting==`

```shell
pip install virtualenv
virtualenv --python=python3 --prompt="DIG" diggers_venv
. ./diggers_venv/bin/activate
pip install -r ./requirements.txt
pip install ./packages/django-messages-master.zip && pip install ./packages/django-tracking-analyzer-master.zip
```