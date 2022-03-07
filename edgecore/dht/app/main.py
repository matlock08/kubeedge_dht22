#!/usr/bin/python
import sys

import time
import argparse
import logging
import logging.config

import Adafruit_DHT
import loadConfigMap 
import edgecloudmessage

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--device', type=str, required=True, help='Device Id for this instance')


################################# main function ##################################################
#### Main function of the capture object module
##################################################################################################
def main():
    args = parser.parse_args()
    device_id = args.device
    broker = '127.0.0.1'
    port = 1883
    
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('dht')
    

    logger.info("Starting for device {}".format(device_id) )
    
    # Load the configuration file, that was mapped from Kubernetes on /opt/kubeedge/deviceProfile.json
    lcm = loadConfigMap.LoadConfigMap(device_id)
    model, devicePin = lcm.load()
    sensor = Adafruit_DHT.DHT22

    # Connect to Local MQTT to update twin properties on cloud via kubeedge edgecore
    ecm = edgecloudmessage.EdgeCloudMessage(device_id, broker, port )
    ecm.connect_mqtt()
    
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, devicePin)
        
        if humidity is not None and temperature is not None:
            logger.info('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            ecm.publishTwinUpdate( temperature, humidity )
            

        time.sleep(60) # wait for 60 seconds
        


if __name__ == '__main__':
    main()