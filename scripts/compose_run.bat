@echo off

docker-compose run --rm app sh -c "python manage.py collectstatic"