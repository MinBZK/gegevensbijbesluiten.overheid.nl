FROM python:3.11.7-slim

ENV YOUR_ENV=production \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2

WORKDIR /backend

# Expensive operations first
RUN apt-get update
RUN apt-get -y install sudo
RUN sudo apt-get -y install gcc g++ python3-dev
RUN pip install "poetry==$POETRY_VERSION" 

ADD ./backend/app /backend/app

# Dynamic operations last
COPY ./backend/poetry.lock /backend/poetry.lock
COPY ./backend/pyproject.toml /backend/pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-interaction --no-ansi

# Expose port
EXPOSE 8000:8000