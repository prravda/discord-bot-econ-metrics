FROM python:3.9-slim

RUN apt-get update && apt-get install -y gcc wget libmariadb3 libmariadb-dev
RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

CMD ["python3", "main.py"]

