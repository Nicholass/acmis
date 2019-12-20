`CMS for urban exploration blog engine`

`=Setup=`

```shell
docker-compose up
docker-compose exec web ./manage.py deploy
docker-compose exec web django-admin compilemessages
```

`==VirtualEnv for Developmentcode hinting==`

```
pip install virtualenv
сd ./app
virtualenv --python=python3 --prompt="DIG" diggers_venv
source ./diggers_venv/bin/activate
pip install -r ./requirements.txt
pip install ./packages/django-messages-master.zip
```
