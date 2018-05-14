`CMS for urban exploration blog engine`

`=Setup=`

```shell
virtualenv --python=python3 --prompt="ACIS" acis_venv
. ./acis_venv/bin/activate
pip install -r ./requirements.txt
python manage.py deploy
python manage.py runserver
```

`=Run=`

```shell
. ./acis_venv/bin/activate
python manage.py runserver
```
