# Makefile - ChatFlow Docker Development

.PHONY: help build up down restart logs migrate createsuperuser test clean health backup restore

help:
	@echo "ChatFlow Docker Management"
	@echo ""
	@echo "🚀 Getting Started:"
	@echo "  make build              - Build all Docker images"
	@echo "  make up                 - Start all services"
	@echo "  make down               - Stop all services"
	@echo ""
	@echo "📊 Monitoring:"
	@echo "  make logs               - View logs from all services"
	@echo "  make logs-backend       - View backend logs"
	@echo "  make logs-frontend      - View frontend logs"
	@echo "  make logs-db            - View database logs"
	@echo "  make logs-redis         - View redis logs"
	@echo "  make health             - Check services health"
	@echo ""
	@echo "🔧 Database:"
	@echo "  make migrate            - Run database migrations"
	@echo "  make createsuperuser    - Create admin user"
	@echo "  make dbshell            - Access database shell"
	@echo "  make backup             - Backup database"
	@echo "  make restore            - Restore database from backup"
	@echo ""
	@echo "🧪 Testing & Debugging:"
	@echo "  make shell              - Python shell in backend"
	@echo "  make bash-backend       - Bash shell in backend"
	@echo "  make bash-frontend      - Bash shell in frontend"
	@echo "  make test-api           - Test API endpoint"
	@echo ""
	@echo "🗑️  Cleanup:"
	@echo "  make clean              - Remove containers (keeps volumes)"
	@echo "  make clean-all          - Remove everything (DESTRUCTIVE)"
	@echo "  make clean-cache        - Clear Redis cache"
	@echo ""

# Build
build:
	docker-compose build

build-backend:
	docker-compose build backend

build-frontend:
	docker-compose build frontend

build-nocache:
	docker-compose build --no-cache

# Lifecycle
up:
	docker-compose up -d

up-build:
	docker-compose up --build -d

down:
	docker-compose down

restart:
	docker-compose restart

restart-backend:
	docker-compose restart backend

restart-frontend:
	docker-compose restart frontend

stop:
	docker-compose stop

start:
	docker-compose start

# Logs
logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f db

logs-redis:
	docker-compose logs -f redis

logs-tail:
	docker-compose logs --tail=100

# Status
ps:
	docker-compose ps

health:
	@echo "Checking service health..."
	@docker-compose exec -T db pg_isready -U postgres || echo "DB: UNHEALTHY"
	@docker-compose exec -T redis redis-cli ping || echo "Redis: UNHEALTHY"
	@docker-compose exec -T backend python manage.py check || echo "Backend: UNHEALTHY"
	@echo "All services checked."

# Database
migrate:
	docker-compose exec backend python manage.py migrate

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

dbshell:
	docker-compose exec db psql -U postgres -d chatflow_db

showmigrations:
	docker-compose exec backend python manage.py showmigrations

makemigrations:
	docker-compose exec backend python manage.py makemigrations

# Backup & Restore
backup:
	@mkdir -p backups
	docker-compose exec db pg_dump -U postgres chatflow_db > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up."

restore:
	@read -p "Enter backup file name: " file; \
	docker-compose exec -T db psql -U postgres chatflow_db < $$file; \
	echo "Database restored."

# Testing
shell:
	docker-compose exec backend python manage.py shell

bash-backend:
	docker-compose exec backend bash

bash-frontend:
	docker-compose exec frontend sh

test-api:
	@echo "Testing API endpoint..."
	@curl -X GET http://localhost:8000/api/ -H "Content-Type: application/json" | jq . || echo "API test failed"

test-redis:
	@echo "Testing Redis connection..."
	@docker-compose exec redis redis-cli ping

test-db:
	@echo "Testing Database connection..."
	@docker-compose exec db pg_isready -U postgres

test-websocket:
	@echo "Testing WebSocket endpoint..."
	@curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
		-H "Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==" \
		-H "Sec-WebSocket-Version: 13" \
		http://localhost:8000/ws/ 2>&1 | head -20

# Django commands
static:
	docker-compose exec backend python manage.py collectstatic --noinput

check:
	docker-compose exec backend python manage.py check

# Redis
redis-shell:
	docker-compose exec redis redis-cli

redis-flush:
	docker-compose exec redis redis-cli FLUSHALL
	@echo "Redis cache cleared."

redis-keys:
	docker-compose exec redis redis-cli KEYS "*"

# Cleanup
clean:
	docker-compose rm -f

clean-all: clean
	docker-compose down -v
	@echo "All containers and volumes removed."

clean-cache:
	docker-compose exec redis redis-cli FLUSHALL
	@echo "Cache cleaned."

clean-images:
	docker image prune -f

# Development
dev-migrate:
	docker-compose exec backend python manage.py migrate

dev-createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

dev-reset:
	@echo "Resetting development environment..."
	docker-compose down -v
	docker-compose up -d
	make migrate
	@echo "Environment reset. Run 'make createsuperuser' to create admin user."

# Advanced
update-requirements:
	docker-compose build --no-cache backend

update-dependencies:
	docker-compose build --no-cache frontend

update-all: update-requirements update-dependencies

prune:
	docker system prune -a --volumes

# Status dashboard
status: ps health
	@echo ""
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "Admin: http://localhost:8000/admin"
	@echo ""

# Default
.DEFAULT_GOAL := help
