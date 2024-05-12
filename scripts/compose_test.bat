@echo off



docker-compose run --rm app sh -c "poetry run python manage.py test"