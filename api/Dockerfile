#FROM ubuntu:latest
# For prodcution
FROM python:3.8-buster
ARG DEBIAN_FRONTEND=noninteractive
# Install dependencies
# RUN apt-get update \
#     && apt-get -y upgrade 

# RUN apt-get -y install gfortran \
#     gcc \
#     build-essential \
#     zlib1g-dev \
#     wget \
#     unzip \
#     cmake \
#     libblas-dev \
#     liblapack-dev \
#     libatlas-base-dev \
#     libc-dev

# RUN apt-get -y install    openjdk-11-jre-headless\
#     openjdk-11-jdk 

# the entire magic of the tiangolo containers, without the risk
## START
RUN python -m pip install --no-cache-dir "uvicorn[standard]" gunicorn fastapi

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh
## END

# Set working directory
WORKDIR /app
RUN mkdir /app/data && mkdir /app/log
RUN chown 1001:1001 /app/data && chown 1001:1001 /app/log

# Add app to Docker
COPY . /app

# Install dependencies
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt 

USER "1001:1001"


# Run FastAPI service
CMD ["/start.sh"]