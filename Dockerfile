FROM python:3.9

RUN echo python --version
RUN echo pip --version

COPY scripts /scripts
COPY requirements.txt /requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

