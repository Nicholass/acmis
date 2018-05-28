`CMS for urban exploration blog engine`

`=Setup=`

```shell
docker-compose up
docker-compose exec web ./manage.py deploy
```

`==VirtualEnv for Developmentcode hinting==`

```shell
virtualenv --python=python3 --prompt="ACIS" acis_venv
. ./acis_venv/bin/activate
pip install -r ./requirements.txt
```