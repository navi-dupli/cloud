# pull official base image
FROM python:3.9-slim-buster

RUN apt-get -y update
RUN apt-get install -y ffmpeg

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app/
RUN mkdir -p /storage/uploads
RUN mkdir -p /storage/converts

#permisos de ejecucion
RUN chmod +x -R /app/entrypoint

#gunicorn --bind 0.0.0.0:5000 manage:app
#ENTRYPOINT ["gunicorn","--bind","0.0.0.0:2000","app:app"]
#ENTRYPOINT ["/app"]