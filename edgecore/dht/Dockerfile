FROM python:3.9-alpine

RUN apk update
RUN apk add gcc musl-dev
RUN mkdir -p /opt/edgecore/dht

#RUN pip3 install --install-option="--force-pi2" Adafruit-DHT
#RUN pip3 install paho-mqtt

WORKDIR /opt/edgecore/dht

COPY ./app/requirements.txt /opt/edgecore/dht/requirements.py
RUN pip3 install -r requirements.py

COPY ./app/*.conf /opt/edgecore/dht/
COPY ./app/*.py /opt/edgecore/dht/
CMD ["python3", "/opt/edgecore/dht/main.py"]