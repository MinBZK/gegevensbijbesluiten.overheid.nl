# **Vernieuwing-inzage-overzicht**

## Inleiding
Vernieuwing Inzage is een initiatief van de overheid om transparantie te bieden over het gebruik van gegevens en de bijbehorende gegevensuitwisseling tussen organisaties voor overheidsbesluiten. Het doel is om informatie hierover op één centrale plek te verzamelen en toegankelijk te maken voor iedereen. Door deze transparantie kunnen fouten sneller worden opgespoord en verbeterd, waardoor de betrouwbaarheid van de gegevens die bij de overheid bekend zijn, wordt vergroot. Dit draagt bij aan het vertrouwen in de overheid.

Dit project is de burger-website gegevensbijbesluiten.overheid.nl, waar de informatie over gegevensgebruik en -uitwisseling voor overheidsbesluiten wordt gepresenteerd. De applicatie bestaat uit een frontend en backend

## Projectstructuur
- `frontend/`: De Nuxt.js-applicatie gebaseerd op Vue.js voor de gebruikersinterface.
- `backend/`: De Python (FastAPI) backend-applicatie met de API en database-modellen.

## Vereisten
Zorg ervoor dat je de volgende tools hebt geïnstalleerd:

- [Docker](https://www.docker.com/) - Docker is nodig om de frontend en backend te draaien in een container.
- [Node.js](https://nodejs.org/) - De versie wordt gespecificeerd in `frontend/.nvmrc`. Het wordt aanbevolen om [Node Version Manager (nvm)](https://github.com/nvm-sh/nvm) te gebruiken om gemakkelijk tussen Node-versies te schakelen. Je kunt de juiste Node-versie activeren met `nvm use`.
- [Python](https://www.python.org/) - De versie wordt gespecificeerd in `backend/.python-version`. Het wordt aanbevolen om [Poetry](https://python-poetry.org/) te gebruiken om tussen virtuele omgevingen van Python te schakelen. Je kunt de juiste Python-versie activeren met `poetry env use <python-version>`.
- [Make](https://www.gnu.org/software/make/) - Make is een hulpprogramma waarmee je handige commando's kunt uitvoeren voor het bouwen, testen en uitvoeren van het project.

## Afhankelijkheden
### Database
Deze applicatie maakt gebruik van een PostgreSQL-database voor het opslaan van gegevens over overheidsbesluiten, gegevensgebruik en -uitwisseling. De database wordt beheerd door het CMS-beheermodule, een apart systeem voor het beheren van de content op gegevensbijbesluiten.overheid.nl.

Instructies voor het instellen en configureren van de database kunnen worden gevonden in de [README van het CMS-beheermodule](https://github.com/MinBZK/gegevensbijbesluiten.overheid.nl/tree/main/inzage-cms).

### Preditor
Preditor wordt gebruikt om statische content op de website te beheren. De content wordt opgeslagen in een JSON-bestand en wordt opgehaald door de frontend. De content wordt beheerd door het CMS-beheermodule.

In de huidige implementatie is Preditor echter niet geconfigureerd voor de open source-versie van het project. De content wordt opgeslagen in de frontend en backend, en wordt niet dynamisch opgehaald vanuit Preditor. De content kan worden aangepast in de frontend door de JSON-bestanden in `frontend/locals/nl.json` en `backend/app/data/static_content_default.json` te bewerken.

## Installatie

### Omgevingsvariabelen
De omgevingsvariabelen worden gelezen uit een `.env`-bestand in backend. Hierin staan de gegevens zoals de database- en API-gegevens.

0. Maak een kopie van het `.env.example`-bestand in zowel backend en hernoem het naar `.env`:
   ```
   cd backend && cp .env.example .env && cd ../frontend && cp .env.example .env
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

### Zonder containers
1. Start de backend-server in development-modus:
   ```
   make backend_dev
   ```
   Open de API-docs in je browser op `http://localhost:8001/api-docs`.
2. Start de frontend-server in een nieuwe terminal:
   ```
   make frontend_dev
   ```
   Open de applicatie in je browser op `http://localhost:3000`.

### Met containers
1. Start de volledige applicatie (backend, frontend en database) in Docker-containers:
   ```
   make vernieuwing_inzage_app
   ```
   Dit commando bouwt Docker-images voor de backend, frontend, en start ze in containers. De frontend is nu beschikbaar op `http://localhost:3000`. De backend Swagger-docs is nu beschikbaar op `http://localhost:8001/api-docs`.

### Overige
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