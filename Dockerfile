FROM docker:27.2.0

RUN apk add --no-cache python3 py3-pip bash

RUN python --version
RUN pip --version

COPY scripts /scripts
COPY requirements.txt /requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN pip install -r requirements.txt

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

