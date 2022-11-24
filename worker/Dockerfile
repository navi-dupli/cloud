# pull official base image
FROM python:3.9-slim-buster

RUN apt-get -y update
RUN apt-get install -y ffmpeg

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POSTGRES_DB=postgres
ENV POSTGRES_PASSWORD=PrQqAPra
ENV POSTGRES_URL=10.108.16.3:432
ENV POSTGRES_USER=postgres
ENV REDIS_SERVER=redis-service
ENV REDIS_PORT=6379
ENV FLASK_ENV=prod
ENV FLASK_DEBUG=0
ENV UPLOAD_FOLDER=uploads/
ENV CONVERTED_FOLDER=converts/
ENV MAIL_NOTIFICATION_ENABLED=FALSE
ENV BUCKET_NAME=miso-bucket-navidupli
ENV TOPIC=converter
ENV PROJECT_ID=despliegue-basico-miso
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credential.json
ENV PORT=8080

#Expose port 8080
EXPOSE 8080

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app/

ENTRYPOINT ["gunicorn","--bind","0.0.0.0:8080","app:app","--workers","1","--threads","8"]