FROM python:3.8-slim


RUN mkdir /usr/src/app/

ADD . /usr/src/app/


WORKDIR /usr/src/app/


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000





