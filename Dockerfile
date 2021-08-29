FROM python:3.9.6 as base

ENV DOCKER_USER_ID 1000
ENV DOCKER_GROUP_ID 1000

ENV PYTHONUNBUFFERED 1

RUN groupadd -g ${DOCKER_GROUP_ID} user \
    && useradd --shell /bin/bash -u $DOCKER_USER_ID -g $DOCKER_GROUP_ID -o -c "" -m user

ADD https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb /tmp/google-chrome-stable_current_amd64.deb

RUN apt update \
    && apt install --no-install-recommends -y /tmp/google-chrome-stable_current_amd64.deb htop \
    && apt-get clean autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

RUN pip install -U pip setuptools pipenv \
    && rm -rf /root/.cache/pip

WORKDIR  /opt/chrome-headless-service/

COPY --chown=user:user ./Pipfile ./Pipfile.lock /opt/chrome-headless-service/

RUN pipenv install --system \
    && pipenv --clear

USER user


FROM base as local

USER root

RUN pipenv install --deploy --system --dev \
    && pipenv --clear

USER user

CMD ["uvicorn", "--host", "0.0.0.0", "application:app", "--reload"]


FROM base as live

COPY --chown=user:user . /opt/chrome-headless-service/

CMD ["gunicorn", "application:app", "--bind", "0.0.0.0", "--workers", "1", "-k", "uvicorn.workers.UvicornWorker", "--access-logfile", "-", "--error-logfile", "-"]
