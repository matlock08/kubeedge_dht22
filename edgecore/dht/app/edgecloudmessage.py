import json
import random
import logging
from paho.mqtt import client as mqtt_client

class EdgeCloudMessage:
    DeviceETPrefix            = "$hw/events/device/"
    TwinETUpdateSuffix        = "/twin/update"
    TwinETUpdateDetalSuffix   = "/twin/update/delta"
    DeviceETStateUpdateSuffix = "/state/update"
    TwinETCloudSyncSuffix     = "/twin/cloud_updated"
    TwinETGetResultSuffix     = "/twin/get/result"
    TwinETGetSuffix           = "/twin/get"

    def __init__(self, device_id, broker, port ):
        self.logger = logging.getLogger('dht')
        self.twin_update_topic = self.DeviceETPrefix + device_id + self.TwinETUpdateSuffix # Update Cloud Event Topic
        
        self.client_id = f'edgecore-dht-app-{random.randint(0, 1000)}'
        # self.username = 'emqx'
        # self.password = 'public'

        self.broker = broker
        self.port = port
        


    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.logger.info("Connected to MQTT Broker!")
            else:
                self.logger.info("Failed to connect, return code {} ".format(rc) )

        # Set Connecting Client ID
        self.client = mqtt_client.Client(self.client_id)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        return self.client


    def publishTwinUpdate(self, temperature, humidity ):
        
        msg = json.dumps( {"event_id":"","timestamp":0,"twin":{"temperature":{"actual":{"value": str(temperature) },"metadata":{"type":"Updated"}},"humidity":{"actual":{"value": str(humidity)  },"metadata":{"type":"Updated"}} } } )

        result = self.client.publish(self.twin_update_topic, msg)
        
        # result: [0, 1]
        status = result[0]

        if status == 0:
            self.logger.info("Send {} to topic {} ".format(msg, self.twin_update_topic) )
        else:
            self.logger.error("Failed to send message to topic {} ".format(self.twin_update_topic) )
    

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            self.logger.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(self.topic)
        client.on_message = on_message