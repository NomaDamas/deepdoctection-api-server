FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND noninteractive
ENV DEEPDOCTECTION_CACHE="/root/.cache/deepdoctection"

WORKDIR /home/repo
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/NomaDamas/deepdoctection-api-server.git
WORKDIR /home/repo/deepdoctection-api-server

RUN apt-get update && \
    apt-get install -y poppler-utils \
                   python3-pip \
                   python3-opencv \
                   tesseract-ocr

RUN mkdir -p $DEEPDOCTECTION_CACHE

ARG PYTORCH='1.13.1'
ARG TORCH_VISION='0.14.1'
ARG CUDA='cu117'

RUN [ ${#PYTORCH} -gt 0 ] && VERSION='torch=='$PYTORCH'.*' ||  VERSION='torch'; python3 -m pip install --no-cache-dir -U $VERSION --extra-index-url https://download.pytorch.org/whl/$CUDA
RUN [ ${#TORCH_VISION} -gt 0 ] && VERSION='torchvision=='$TORCH_VISION'.*' ||  VERSION='torchvision'; python3 -m pip install --no-cache-dir -U $VERSION --extra-index-url https://download.pytorch.org/whl/$CUDA

RUN python3 -m pip install -U pip setuptools
RUN python3 -m pip install --no-cache-dir ".[source-pt]"

RUN python3 setup.py install

# python3 app.py
EXPOSE 8000

CMD uvicorn app:app --host 0.0.0.0 --port 8000
# Run this using 'docker run -it -d -p <YOUR PORT>:8000 --gpus all <IMAGE NAME>
