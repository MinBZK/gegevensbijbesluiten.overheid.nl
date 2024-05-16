# Backend commands
backend_dev:
	$(MAKE) -C backend dev

test:
	$(MAKE) -C backend test

# Frontend commands
frontend_dev:
	$(MAKE) -C frontend dev

# Type fixing (frontend and backend)
type_fix:
	$(MAKE) -C frontend type_fix
	$(MAKE) -C backend type_fix
	
# Application commands
vernieuwing_inzage_app:
	docker compose --env-file ./backend/.env --env-file ./frontend/.env up -d
