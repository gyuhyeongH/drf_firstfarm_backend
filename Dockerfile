FROM ubuntu:18.04

# Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get -y install software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update --fix-missing && \
    apt-get -y install --fix-missing python3.8 && \
    apt-get -y install --fix-missing python3.8-dev && \
    apt-get -y install --fix-missing python3-pip && \
    python3.8 -m pip install pip --upgrade

ENV HOME .

# mecab start
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl
RUN apt-get install python3-setuptools
RUN apt-get install -y default-jdk default-jre
# mecab end

ADD requirements.txt ${HOME}

RUN pip install -r requirements.txt

# mecab start
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
RUN update-alternatives --config python3
RUN cd ${HOME} && \
    curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash -s
# mecab end

RUN export LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8

ADD . /usr/src/app/

WORKDIR /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000



