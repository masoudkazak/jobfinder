build:
	docker compose up --build -d
up:
	docker compose up -d
down:
	docker compose down
down-v:
	docker compose down -v
django-logs:
	docker logs -f django-api
fastapi-logs:
	docker logs -f fastapi
shell:
	docker exec -it django-api python manage.py shell_plus
makemigrations:
	docker exec -it django-api python manage.py makemigrations
migrate:
	docker exec -it django-api python manage.py migrate
superuser:
	docker exec -it django-api python manage.py createsuperuser
psql:
	docker exec -it postgres \
  	bash -c "PGPASSWORD=$$POSTGRES_PASSWORD psql -U $$POSTGRES_USER -d $$POSTGRES_DB"
pytest:
	docker exec django-api pytest . --reuse-db
ruff:
	docker exec django-api ruff check .
