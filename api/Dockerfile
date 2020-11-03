FROM python:3.8

# Install dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get install -y \
        gcc \
        build-essential \
        zlib1g-dev \
        wget \
        unzip \
        cmake \
        python3-dev \
        gfortran \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        install libc-dev \
    && apt-get clean

# Set working directory
WORKDIR /app

# Add app to Docker
COPY ./ ./

# Install dependencies
RUN pip install --upgrade pip; \
    pip install --no-cache -r requirements.txt 

WORKDIR /api
# Run FastAPI service
RUN python fastapp.py --reload