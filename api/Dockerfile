FROM tensorflow/tensorflow:latest-py3
ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update\
    && apt-get -y upgrade\
    && mkdir -p /usr/share/man/man1\
    && apt-get -y --no-install-recommends install openjdk-11-jre-headless
    #&& apt-get clean all\
    #&& rm -rf /var/lib/apt/lists/

RUN apt-get install -y build-essential python3 python3-pip libssl-dev libffi-dev gcc 

COPY ./gunicorn_conf.py /app/gunicorn.conf.py

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

WORKDIR /app
RUN mkdir /app/data && mkdir /app/log
# RUN chown $uid /app/data && chown $uid /app/log

# Add app to Docker
COPY . /app

# Install dependencies
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN apt install -y python3.8
RUN mv /usr/bin/python3.8 /usr/local/bin/python
RUN python get-pip.py
RUN python -m pip install --no-cache-dir -r requirements/requirements.txt 
RUN python -m pip install --no-cache-dir -r requirements/ml_requirements.txt
RUN pip3 install jpl.pipedreams==1.0.3
RUN python -m spacy download en_core_web_sm
RUN python -m pip install --no-cache-dir "uvicorn[standard]" gunicorn fastapi


# Run FastAPI service 
CMD ["/start.sh"]
