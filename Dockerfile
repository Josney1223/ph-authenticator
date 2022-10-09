FROM debian

RUN apt-get -y update
RUN apt-get -y install python3-pip

WORKDIR /app
COPY . /app

RUN pip install -r /app/dependencies.txt

EXPOSE 2000
CMD ["uwsgi", "--ini", "/app/wsgi.ini"]