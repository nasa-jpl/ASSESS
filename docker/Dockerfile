FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update -y
RUN apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
RUN apt-get install build-essential checkinstall -y
RUN apt-get install wget -y
RUN apt-get install openjdk-8-jdk -y
RUN apt-get install curl -y
RUN wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
RUN tar -xvf Python-2.7.10.tgz
WORKDIR ./Python-2.7.10
RUN ./configure
RUN make
RUN checkinstall -y
RUN apt-get install python-pip python-dev build-essential -y
RUN pip install --upgrade pip
RUN apt-get install git -y

WORKDIR /
RUN git clone https://github.com/nasa-jpl/ASSESS.git
WORKDIR /ASSESS/webapp/standards_extraction
RUN ./build.sh
WORKDIR /ASSESS/webapp
RUN pip install -r requirements.txt
RUN pip install -U textblob
RUN curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python
