FROM ubuntu:22.04

ENV TZ=Europe/Moscow
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    curl unzip wget xvfb python3.10 python3-pip locales zip && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

# install google-chrome
RUN CHROME_SETUP=google-chrome.deb && \
    wget -qO $CHROME_SETUP "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    apt install -y ./$CHROME_SETUP && \
    rm $CHROME_SETUP

RUN pip install poetry==1.2.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --no-interaction

# Copying actuall application
COPY . /app/src/

CMD ["python3", "-m", "pytest", "--mode", "headless", "-v"]
