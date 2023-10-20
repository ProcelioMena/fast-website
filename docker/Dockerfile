FROM python:3.11-slim-bullseye as python

ARG CRAFT_PYPI_URL
ARG APP_HOME=/app
ARG ENV
ENV ENV ${ENV}
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev \
  gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN addgroup --system serveruser && adduser --system --ingroup serveruser serveruser

COPY --chown=serveruser:serveruser ./src/ ${APP_HOME}
WORKDIR ${APP_HOME}

COPY --chown=serveruser:serveruser docker/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

RUN chown serveruser:serveruser ${APP_HOME}
USER serveruser
ENTRYPOINT ["/entrypoint"]
