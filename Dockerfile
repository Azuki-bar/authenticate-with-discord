FROM python:3.10-slim as base
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.13 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # POETRY_VIRTUALENVS_IN_PROJECT=false \
    # POETRY_VIRTUALENV_CREATE=false \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get update && apt-get install -y --no-install-recommends \
curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

FROM base AS runner
RUN poetry config virtualenvs.create false
COPY ./pyproject.toml ./poetry.lock ./main.py /
RUN poetry install --no-dev
CMD ["python", "/main.py"]

