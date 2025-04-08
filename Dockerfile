FROM python:3.11.11-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /RSA_API

COPY ./pyproject.toml /RSA_API/pyproject.toml

COPY ./uv.lock /RSA_API/uv.lock

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project --no-dev

COPY ./app /RSA_API/app

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

ENV PATH="/RSA_API/.venv/bin:$PATH"

EXPOSE 8000

CMD ["fastapi", "run","app/main.py", "--host", "0.0.0.0", "--port", "8000"]
