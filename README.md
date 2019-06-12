`CMS for urban exploration blog engine`

`=Setup=`

```
pip install virtualenv
virtualenv --python=python3 --prompt="DIG" diggers_venv
source ./diggers_venv/bin/activate
pip install -r ./requirements.txt
pip install ./packages/django-messages-master.zip
./manage.py deploy
gunicorn acis.wsgi -b 0.0.0.0:8000
```