`CMS for urban exploration blog engine`

`=Setup=`

```
pip install virtualenv
virtualenv --python=python3 --prompt="DIG" diggers_venv
source ./diggers_venv/bin/activate
pip install -r ./requirements.txt
pip install ./packages/django-messages-master.zip && pip install ./packages/django-tracking-analyzer-master.zip
cp ./packages/PyBB/0008_auto_20180709_2221.py ./diggers_venv/lib/python3.5/site-packages/pybb/migrations/
cp ./packages/PyBB/django.po ./diggers_venv/lib/python3.5/site-packages/pybb/locale/en/LC_MESSAGES/
./manage.py deploy
gunicorn acis.wsgi -b 0.0.0.0:8000
```