FROM python:3.8.3-slim-buster

# set work directory


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src
# install dependencies

COPY ./requirements.txt /user/requirements.txt

RUN pip install -r /user/requirements.txt

# copy project
COPY ./src /user/src

EXPOSE 8000
#
CMD python /user/src/manage.py migrate --noinput && python /user/src/manage.py runserver 0.0.0.0:8000