FROM ubuntu:18.04

# Python
RUN apt-get update \
    sudo apt install software-properties-common \
    sudo add-apt-repository ppa:deadsnakes/ppa \
    sudo apt install python3.8 \
    wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz \
    tar xvfz mecab-0.996-ko-0.9.2.tar.gz \
    cd mecab-0.996-ko-0.9.2 \
    ./configure \
    make \
    make check \
    sudo make install \
    sudo ldconfig \
    wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz \tar xvfz mecab-ko-dic-2.1.1-20180720.tar.gz \cd mecab-ko-dic-2.1.1-20180720  \
    ./configure \
    make \
    sudo make install \
    sudo apt install curl \
    sudo apt install git \
    bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh) \
    pip install mecab-python \

ADD . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir /usr/src/app/
WORKDIR /usr/src/app/


EXPOSE 8000




