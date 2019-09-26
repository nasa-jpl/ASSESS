FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update -y
RUN apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libffi-dev libc6-dev libbz2-dev python3 -y
RUN apt-get install build-essential checkinstall -y
RUN apt-get install wget -y
RUN apt-get install openjdk-8-jdk -y
RUN apt-get install curl -y
RUN wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
RUN apt-get install python3-pip python3-dev build-essential -y
RUN pip3 install --upgrade pip
RUN apt-get install git -y
RUN apt-get install unzip

WORKDIR /
RUN git clone https://github.com/nasa-jpl/ASSESS.git
WORKDIR /ASSESS
RUN git checkout new_design
WORKDIR /ASSESS/webapp/standards_extraction
RUN ./build.sh
WORKDIR /ASSESS
RUN pip3 install -r requirements.txt
RUN pip3 install -U textblob
RUN curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python3
RUN python3 -m textblob.download_corpora
RUN python3 -m spacy download en
WORKDIR /ASSESS/webapp/standards
RUN unzip \*.zip
RUN unzip ../models/graph.zip