FROM ubuntu:18.04

COPY ./requirements.txt requirements.txt
COPY ./app.py app.py

RUN apt update && apt install python3.7 python3-pip -y
RUN apt install -y g++ build-essential apt-utils gcc gdb && python3.7 -m pip install cython

RUN python3.7 -m pip install -r requirements.txt
RUN python3.7 -m textblob.download_corpora
RUN python3.7 -m pip install curl
RUN python3.7 -m spacy download en_core_web_sm

EXPOSE 5000

CMD python3.7 ./app.py
