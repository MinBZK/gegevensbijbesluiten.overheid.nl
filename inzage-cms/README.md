# **CMS-Beheermodule**

## Inleiding
Vernieuwing Inzage is een initiatief van de overheid om transparantie te bieden over het gebruik van gegevens en de bijbehorende gegevensuitwisseling tussen organisaties voor overheidsbesluiten. Het doel is om informatie hierover op één centrale plek te verzamelen en toegankelijk te maken voor iedereen. Door deze transparantie kunnen fouten sneller worden opgespoord en verbeterd, waardoor de betrouwbaarheid van de gegevens die bij de overheid bekend zijn, wordt vergroot. Dit draagt bij aan het vertrouwen in de overheid.

Dit project is het Content Management Systeem (CMS) dat wordt gebruikt voor het beheren van de content op de Vernieuwing Inzage website (gegevensbijbesluiten.overheid.nl). Het stelt gebruikers in staat om eenvoudig en efficiënt content te creëren, bewerken en publiceren op de website. De applicatie bestaat uit een frontend, backend en database.

## Projectstructuur
- `frontend/`: De Vue.js-applicatie voor de gebruikersinterface.
- `backend/`: De Python (FastAPI) backend-applicatie met de API en database-modellen.
- `backend/app/database`: PostgreSQL-database. Deze wordt opgestart in een Docker-container.

## Vereisten
Zorg ervoor dat je de volgende tools hebt geïnstalleerd:

- [Docker](https://www.docker.com/) - Docker is nodig om de database te draaien in een container.
- [Node.js](https://nodejs.org/) - De versie wordt gespecificeerd in `frontend/.nvmrc`. Het wordt aanbevolen om [Node Version Manager (nvm)](https://github.com/nvm-sh/nvm) te gebruiken om gemakkelijk tussen Node-versies te schakelen. Je kunt de juiste Node-versie activeren met `nvm use`.
- [Python](https://www.python.org/) - De versie wordt gespecificeerd in `backend/.python-version`. Het wordt aanbevolen om [Poetry](https://python-poetry.org/) te gebruiken om tussen virtuele omgevingen van Python te schakelen. Je kunt de juiste Python-versie activeren met `poetry env use <python-version>`.
- [Make](https://www.gnu.org/software/make/) - Make is een hulpprogramma waarmee je handige commando's kunt uitvoeren voor het bouwen, testen en uitvoeren van het project.

## Afhankelijkheden

### Authenticatie en Autorisatie
Voor authenticatie en autorisatie maakt het CMS-Beheermodule gebruik van [Keycloak](https://www.keycloak.org/), een open source identiteit- en toegangsbeheeroplossing. Keycloak is verantwoordelijk voor het beheren van gebruikersaccounts, rollen en machtigingen binnen de applicatie.

In de huidige implementatie is Keycloak echter uitgeschakeld voor de open source-versie van het project. Dit betekent dat er geen authenticatie- of autorisatiecontroles zijn ingebouwd in deze versie. Als u de applicatie wilt gebruiken met een werkende authenticatie- en autorisatiemodule, moet u Keycloak zelf configureren en integreren met de backend-applicatie.

### Clamav scanner
Voor het scannen van bestanden in de bestand accorderingen tabel maakt het CMS-Beheermodule gebruik van [ClamAV](https://www.clamav.net/), een open source anti-virusengine voor het detecteren van virussen, malware, Trojaanse paarden en andere kwaadaardige bedreigingen. ClamAV wordt gebruikt om bestanden te controleren op mogelijke bedreigingen voordat ze worden opgeslagen in de database.

In de huidige implementatie is ClamAV echter niet geconfigureerd voor de open source-versie van het project. Dit betekent dat bestanden niet automatisch worden gescand op bedreigingen. Als u de applicatie wilt gebruiken met een werkende ClamAV-integratie, moet u ClamAV zelf configureren en integreren met de backend-applicatie.

## Installatie

### Omgevingsvariabelen
De omgevingsvariabelen worden gelezen uit een `.env`-bestand in backend. Hierin staan de gegevens zoals de database- en API-gegevens.

0. Maak een kopie van het `.env.example`-bestand in zowel backend en hernoem het naar `.env`:
   ```
   cd backend && cp .env.example .env
   ```

### Backend (met Poetry)
[Poetry](https://python-poetry.org/) is een tool voor afhankelijkheidsbeheer en verpakking in Python. Het wordt gebruikt om de Python-pakketten voor de backend te beheren en de virtuele omgeving te maken.

#### Linux/Windows
1. Open een terminal en navigeer naar de backend-directory met:
   ```
   cd backend
   ```
2. Installeer de vereiste Python-pakketten:
   ```
   poetry install
   ```
3. Activeer de virtuele omgeving:
   ```
   poetry shell
   ```

### Frontend
1. Open een terminal en navigeer naar de frontend-directory met:
   ```
   cd frontend
   ```
2. Installeer de vereiste Node.js-pakketten:
   ```
   npm install
   ```

## Uitvoeren

### Database opzetten in een container
0. Initialiseer de database in een container via Docker:
   ```
   make db_dev
   ```
   Dit commando start een PostgreSQL-database in een Docker-container. [DbGate](https://dbgate.org) is een database-client om gemakkelijk verbinding te maken met de database.

### Zonder containers
1. Voer database-migraties uit:
   ```
   make migration_head
   ```
   Open de DbGate database-client in je browser op `http://localhost:8092`.
2. Start de backend-server in development-modus:
   ```
   make backend_dev
   ```
   Open de API-docs in je browser op `http://localhost:8000/api-docs`.
3. Start de frontend-server in een nieuwe terminal:
   ```
   make frontend_dev
   ```
   Open de applicatie in je browser op `http://localhost:8080`.

### Met containers
1. Start de volledige applicatie (backend, frontend en database) in Docker-containers:
   ```
   make cms_app
   ```
   Dit commando bouwt Docker-images voor de backend, frontend en database, en start ze in containers. De frontend is nu beschikbaar op `http://localhost:8080`. De backend Swagger-docs is nu beschikbaar op `http://localhost:8000/api-docs`. De DbGate-client is nu beschikbaar op `http://localhost:8092`.

### Overige
- Reset database en start DbGate client opnieuw op:
   ```
   make dev_db_reset
   ```
- Formatteren en linting:
   ```
   make type_fix
   ```
- Unittest uitvoeren:
   ```
   make test
   ```

### Handige commando's
- Pre-commit hooks vanuit backend folder:
   - `poetry run pre-commit install` installeert de pre-commit hooks in de Git-hook scripts van het project.
   - `poetry run pre-commit autoupdate` zorgt ervoor dat de pre-commit hooks up-to-date zijn met de nieuwste versies.
   - `poetry run pre-commit run --all-files -v` voert alle geïnstalleerde pre-commit hooks uit op alle bestanden in het project.
- Migraties runnen vanuit backend folder:
   - Nieuwe migratie maken: `poetry run alembic -c alembic/alembic.ini revision -m "account tabel aanmaken"`
   - Laatste migratie terugdraaien: `poetry run alembic -c alembic/alembic.ini downgrade -1`
   - Alle migraties ongedaan maken: `poetry run alembic -c alembic/alembic.ini downgrade base`
   - Alle migraties uitvoeren: `poetry run alembic -c alembic/alembic.ini upgrade head`