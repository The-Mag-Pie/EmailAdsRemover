FROM alpine:latest

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add python3 py3-pip
RUN ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /script
COPY ./EmailAdsRemover.py .
ENTRYPOINT [ "python", "EmailAdsRemover.py" ]
