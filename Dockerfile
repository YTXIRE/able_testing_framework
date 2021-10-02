FROM debian

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3-pip -y

WORKDIR /app

RUN chmod 777 /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD pytest --alluredir=allure-results