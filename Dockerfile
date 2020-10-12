FROM python:3.9.0

ENV DOCKER_USER_ID 1000
ENV DOCKER_GROUP_ID 1000

ENV PYTHONUNBUFFERED 1

RUN groupadd -g ${DOCKER_GROUP_ID} user \
    && useradd --shell /bin/bash -u $DOCKER_USER_ID -g $DOCKER_GROUP_ID -o -c "" -m user

ADD https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb /tmp/google-chrome-stable_current_amd64.deb

RUN apt update \
    && apt install --no-install-recommends -y /tmp/google-chrome-stable_current_amd64.deb \
    && apt-get clean autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

ADD https://chromedriver.storage.googleapis.com/LATEST_RELEASE /tmp/chromedriver-latest-release

RUN cd /tmp \
    && wget https://chromedriver.storage.googleapis.com/`cat /tmp/chromedriver-latest-release`/chromedriver_linux64.zip \
    && mkdir /opt/chromedriver \
    && unzip chromedriver_linux64.zip -d /opt/chromedriver \
    && rm chromedriver_linux64.zip

COPY ./requirements.txt /opt/chrome-headless-service/

WORKDIR  /opt/chrome-headless-service/

RUN pip install -U pip setuptools \
    && pip install  -r /opt/chrome-headless-service/requirements.txt \
    # --require-hashes doesn't work without cache
    && rm -rf /root/.cache/pip

USER user
