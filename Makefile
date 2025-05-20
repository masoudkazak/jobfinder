build:
	docker-compose up --build -d
up:
	docker-compose up -d
down:
	docker-compose down
down-v:
	docker-compose down -v
api-logs:
	docker logs -f karsaz
shell:
	docker exec -it karsaz python manage.py shell_plus
makemigrations:
	docker exec -it karsaz python manage.py makemigrations
