FROM python:3.10

RUN python --version
RUN pip --version

COPY scripts /scripts
COPY requirements.txt /requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN pip install --break-system-packages -r requirements.txt

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

