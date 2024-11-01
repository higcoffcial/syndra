FROM python:3.11-slim AS python-image

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION=1.7.1

WORKDIR /requirements
COPY poetry.lock* pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install "poetry==$POETRY_VERSION" \
    && poetry export --without dev --without-hashes -f requirements.txt --output requirements.txt

RUN python -m venv --copies /venv
ENV PATH="/venv/bin:$PATH"
RUN --mount=type=cache,target=/root/.cache/pip \
    /venv/bin/python -m pip install -r requirements.txt

FROM nginx:1.25-bookworm

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked apt-get update -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    libpython3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-image /venv /venv
ENV PATH="/venv/bin:$PATH"
RUN update-alternatives --install /usr/bin/python3 python3 /venv/bin/python 1 \
    && update-alternatives --install /usr/bin/python python /venv/bin/python 1

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY nginx.conf /etc/nginx/nginx.conf

COPY docker_start.sh /docker_start.sh
RUN sed -i "s/\r$//g" /docker_start.sh \
    && chmod +x /docker_start.sh

RUN mkdir -p /syndra/

COPY utils /syndra/utils/
COPY classes /syndra/classes/
COPY main.py /syndra/main.py

WORKDIR /usr/share/nginx/html

CMD ["/docker_start.sh"]