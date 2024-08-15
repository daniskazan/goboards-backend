
docker_compose_path = "docker-compose.local.yml"


lint:

	ruff format --check src tests

dc-up:
	docker compose -f $(docker_compose_path) up -d
dc-down:
	docker compose -f $(docker_compose_path) down

server:
	python src/main.py