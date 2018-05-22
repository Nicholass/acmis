#/bin/sh

docker-compose up -d
docker-compose exec web python ./manage.py bower_install --allow-root
docker-compose exec web python ./manage.py collectstatic
docker-compose exec web python ./manage.py migrate
docker-compose exec web python ./manage.py deploy