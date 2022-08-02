FROM alpine:3.8

# MECAB 버전 및 파일 경로
ENV MECAB_KO_FILENAME "mecab-0.996-ko-0.9.2"
ENV MECAB_KO_URL "https://bitbucket.org/eunjeon/mecab-ko/downloads/$MECAB_KO_FILENAME.tar.gz"

ENV MECAB_KO_DIC_FILENAME "mecab-ko-dic-2.1.1-20180720"
ENV MECAB_KO_DIC_URL "https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/$MECAB_KO_DIC_FILENAME.tar.gz"

RUN apk add --no-cache libstdc++ ;\
    apk --no-cache add --virtual .builddeps build-base autoconf automake ;\
    wget -O - $MECAB_KO_URL | tar zxfv - ;\
    cd $MECAB_KO_FILENAME; ./configure; make; make install ;cd .. ;\
    wget -O - $MECAB_KO_DIC_URL | tar zxfv - ;\
    cd $MECAB_KO_DIC_FILENAME; sh ./autogen.sh ; ./configure; make; make install ; cd ..; \
    apk del .builddeps ;\
    rm -rf mecab-*
# Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get -y install software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update --fix-missing && \
    apt-get -y install --fix-missing python3.6 && \
    apt-get -y install --fix-missing python3.6-dev && \
    apt-get -y install --fix-missing python3-pip && \
    python3.6 -m pip install pip --upgrade

ENV HOME .

ADD . /usr/src/app/
WORKDIR /usr/src/app/


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
