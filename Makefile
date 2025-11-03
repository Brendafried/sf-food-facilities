
APP_MODULE=app.main:app
HOST=0.0.0.0
PORT=8002
IMAGE_NAME=sf-food-api

.PHONY: install dev test docker-build docker-run docker-test dc-up dc-down dc-logs

install:
	pip install -r requirements.txt

dev:
	uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

test:
	pytest

# plain docker
docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run --rm -p $(PORT):8002 $(IMAGE_NAME)

# docker compose
dc-up:
	docker compose up --build

dc-down:
	docker compose down

dc-logs:
	docker compose logs -f
