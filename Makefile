.PHONY: venv migrate run

venv:
	python -m venv venv && \
	venv/bin/pip install --upgrade pip && \
	venv/bin/pip install -r requirements.txt

migrate:
	venv/bin/python manage.py makemigrations
	venv/bin/python manage.py migrate

run:
	venv/bin/python manage.py runserver 0.0.0.0:8000
