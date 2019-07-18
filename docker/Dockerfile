FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y --fix-missing
RUN apt-get install libffi-dev -y
RUN apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
RUN apt-get install build-essential checkinstall -y
RUN apt-get install wget -y
RUN apt-get install openjdk-8-jdk -y
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
RUN tar -xvf Python-3.6.0.tgz
WORKDIR ./Python-3.6.0
RUN ./configure
RUN make
RUN checkinstall -y
RUN apt-get install python3-pip python3-dev build-essential -y
RUN pip3 install --upgrade pip
RUN apt-get install git -y

WORKDIR /
ADD . /ASSESS
WORKDIR /ASSESS/webapp/standards_extraction
RUN ./build.sh
WORKDIR /ASSESS/webapp
RUN pip install -r requirements.txt
RUN python3 -m textblob.download_corpora

