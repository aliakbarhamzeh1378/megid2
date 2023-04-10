import time

import paho.mqtt.client as mqtt
import sentry_sdk
from fluent import event
from fluent import sender


class MqttToFluentd:
    def __init__(self, mqtt_broker, mqtt_topic, fluentd_host='localhost', fluentd_tag='jjjj', sentry_dsn=None):
        # Set up the Fluentd logger
        sender.setup(fluentd_tag, host=fluentd_host, port=24224)

        # Set up the MQTT client
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(mqtt_broker, 1883)
        self.client.subscribe(mqtt_topic)
        # Set up Sentry error tracking
        if sentry_dsn:
            sentry_sdk.init(sentry_dsn)

    def on_message(self, client, userdata, message):

        try:
            # Extract the received message data
            data = message.payload.decode('utf-8')

            # Parse the message data into individual data points
            fanVal, heaterVal, waterPumpVal, lightVal, humidityValue, tempValue, soilMoistureValue, lightValue, silo3, silo4, la, sn, lo, ew = data.split(
                ',')

            # convert string values to appropriate data types

            print(fanVal, heaterVal, waterPumpVal, lightVal, humidityValue, tempValue, soilMoistureValue, lightValue, silo3, silo4, la, sn, lo, ew)

            # Create a dictionary to represent the message
            message_dict = {
                'fanVal': int(fanVal),
                'heaterVal': int(heaterVal),
                'waterPumpVal': int(waterPumpVal),
                'lightVal': int(lightVal),
                'humidityValue': int(humidityValue),
                'tempValue': int(tempValue),
                'soilMoistureValue': int(soilMoistureValue),
                'lightValue': int(lightValue),
                'silo3': int(silo3),
                'silo4': int(silo4),
                'la': str(la),
                'lo': str(lo),
                'sn': str(sn),
                'ew': str(ew),
                'time': time.time(),
                'slave_id': str(message.topic).split(":")[1]
            }
            # Send the message to Fluentd logger
            event.Event('', message_dict)
        except Exception as e:
            # Log the exception and continue processing messages
            print(f"Error processing message: {str(e)}")
            if sentry_sdk:
                sentry_sdk.capture_exception(e)

    def start(self):
        # Start the MQTT client loop
        self.client.loop_forever()


# Example usage:
mqtt_to_fluentd = MqttToFluentd('localhost', '#')
mqtt_to_fluentd.start()
