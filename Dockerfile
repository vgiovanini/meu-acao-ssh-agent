FROM python:3.9

RUN apk add --no-cache python3 py3-pip bash

COPY scripts /scripts
COPY requirements.txt /requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

