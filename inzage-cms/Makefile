# Backend commands
backend_dev:
	$(MAKE) -C backend dev

test:
	$(MAKE) -C backend test

migration_head:
	$(MAKE) -C backend migration_head

# Frontend commands
frontend_dev:
	$(MAKE) -C frontend dev

# Database commands
db_dev:
	docker network inspect database >/dev/null 2>&1 || docker network create database
	docker compose --env-file ./backend/.env --env-file ./frontend/.env.development up -d dbgate

db_dev_reset:
	docker compose --env-file ./backend/.env --env-file ./frontend/.env.development down && docker volume rm inzage-data && docker compose --env-file ./backend/.env  --env-file ./frontend/.env.development up -d dbgate

# Type fixing (frontend and backend)
type_fix:
	$(MAKE) -C frontend type_fix
	$(MAKE) -C backend type_fix

# Application commands
cms_app:
	docker network inspect database >/dev/null 2>&1 || docker network create database
	docker compose --env-file ./backend/.env --env-file ./frontend/.env.development up -d
