FROM tensorflow/tensorflow:latest-py3
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \  
    libffi-dev \ 
    gcc \
    python3-pip \
    software-properties-common

# software-properties-common needed before this
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
    python3.8 \ 
    python3.8-distutils \
    python3-six \
    python3-pip
RUN mv /usr/bin/python3.8 /usr/local/bin/python
COPY . /app
WORKDIR /app
RUN chmod +x /app/start.sh && chmod +x /app/start-reload.sh
RUN mkdir /app/data && mkdir /app/log
# RUN chown $uid /app/data && chown $uid /app/log

# Install dependencies
#RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#RUN python get-pip.py
RUN pip3 --no-cache-dir -r requirements.txt 
RUN pip3 install --upgrade setuptools distlib
RUN pip3 install jpl.pipedreams==1.0.3
RUN python -m spacy download en_core_web_sm
RUN pip3 --no-cache-dir "uvicorn[standard]" gunicorn fastapi

# Run FastAPI service 
CMD ["/app/start.sh"]
