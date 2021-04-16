FROM ubuntu:latest

# Set working directory
WORKDIR /app

# Add app to Docker
COPY . /app

ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update
RUN apt-get -y upgrade 

RUN apt-get -y install python3 \
    python3-pip 

RUN apt-get -y install gfortran \
    gcc \
    build-essential \
    zlib1g-dev \
    wget \
    unzip \
    cmake \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libc-dev

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --upgrade -r requirements.txt 

WORKDIR /app
# Run FastAPI service
RUN python fastapp.py --reload