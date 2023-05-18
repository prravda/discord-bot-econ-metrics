FROM python:3.9-slim

RUN apt-get update && apt-get install -y gcc wget libmariadb3 libmariadb-dev
RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app

RUN echo 'installing dependencies...'
RUN pip3 install -r requirements.txt

RUN echo 'installing Korean-compatible font(malgun gothic)'
RUN wget "https://www.wfonts.com/download/data/2016/06/13/malgun-gothic/malgun.ttf"
RUN mv malgun.ttf /usr/share/fonts/truetype/

COPY . /app

CMD ["python3", "main.py"]

