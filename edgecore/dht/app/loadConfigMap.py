import json
import logging

class LoadConfigMap:
    

    def __init__(self, device_id, deviceProfile= "/opt/kubeedge/deviceProfile.json" ):
        self.logger = logging.getLogger('dht')
        self.deviceModel = None
        self.devicePin = None

        with open(deviceProfile) as f:
            config = json.load(f)

            for device in config["deviceInstances"]:
                if device["id"] == device_id:
                    self.deviceModel = device["model"]
                    break

            if self.deviceModel != None:
                for model in config["deviceModels"]:
                    if model["name"] == self.deviceModel:
                        for property in model["properties"]:
                            # For DHT11 Pin Number
                            if property["name"] == "sensor-pin-number":
                                self.devicePin = int(property["defaultValue"])
                                break

            
        self.logger.info("Configured {} Model {} Pin {} ".format(device_id, self.deviceModel, self.devicePin) )
        

    def load(self):
        return self.deviceModel, self.devicePin