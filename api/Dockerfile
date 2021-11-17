#FROM python:3.9
#FROM ubuntu:latest
FROM tensorflow/tensorflow:2.2.3-py3
#ARG uid
ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update\
    && apt-get -y upgrade\
    # Stupid base image bug https://stackoverflow.com/a/58503437
    && mkdir -p /usr/share/man/man1\
    && apt-get -y --no-install-recommends install openjdk-11-jre-headless
    # && apt-get clean all\
    # && rm -rf /var/lib/apt/lists/

RUN apt-get install -y build-essential python3 python3-pip libssl-dev libffi-dev gcc 

# the entire magic of the tiangolo containers, without the risk
## START
RUN python3 -m pip install --no-cache-dir "uvicorn[standard]" gunicorn fastapi 

COPY ./gunicorn_conf.py /app/gunicorn.conf.py

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh
## END

# Set working directory
WORKDIR /app
RUN mkdir /app/data && mkdir /app/log
# RUN chown $uid /app/data && chown $uid /app/log

# Add app to Docker
COPY . /app

# Install dependencies
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py
RUN python3.8 -m pip install --no-cache-dir -r requirements.txt 
RUN python3.8 -m pip install --no-cache-dir -r ml_requirements.txt
RUN pip3.8 install jpl.pipedreams==1.0.3
RUN python3.8 -m spacy download en_core_web_sm

# USER "$uid"


# # Run FastAPI service 
# CMD ["/start.sh"]
