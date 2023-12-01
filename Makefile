PROJECT_NAME=donkeytravel

.PHONY:	up
up:
	docker-compose down --volumes --rmi all
	docker compose up --build

.PHONY:	down
down:
	docker compose	down -v

.PHONY: migrate
migrate:
	docker compose run web python manage.py migrate

.PHONY: makemigrations
makemigrations:
	docker compose run web python manage.py makemigrations

.PHONY: collectstatic
collectstatic:
	docker compose run web python manage.py collectstatic --noinput

.PHONY: reset
reset:
	docker-compose down --volumes --rmi all

.PHONY:	start
start:
	docker compose	up

.PHONY:	stop
stop:
	docker compose	down

.PHONY: admin
admin:
	docker compose run web python manage.py createsuperuser

.PHONY: test
test: 
	docker compose run web python manage.py test