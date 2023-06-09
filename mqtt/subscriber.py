from datetime import datetime
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
            print(data)
            # Parse the message data into individual data points
            waterPumpVal, lightVal, fanVal, heaterVal, POT, tempValue, humidityValue, lightValue, _, soilMoistureValue, la, sn, lo, ew = data.split(
                ',')

            # convert string values to appropriate data types

            print(fanVal, heaterVal, waterPumpVal, lightVal, POT, tempValue, humidityValue, lightValue, _,
                  soilMoistureValue, la, sn, lo, ew)

            # Create a dictionary to represent the message
            message_dict = {
                'fanVal': str(fanVal),
                'POT': str(POT),
                'heaterVal': str(heaterVal),
                'waterPumpVal': str(waterPumpVal),
                'lightVal': str(lightVal),
                'humidityValue': str(humidityValue),
                'tempValue': str(tempValue),
                'soilMoistureValue': str(soilMoistureValue),
                'lightValue': str(lightValue),
                '_': str(0),
                'la': str(la),
                'lo': str(lo),
                'sn': str(sn),
                'ew': str(ew),
                'time':datetime.now().isoformat(),
                'slave_id': str(message.topic).split(":")[1]
            }
            # Send the message to Fluentd logger
            print(message_dict)
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
mqtt_to_fluentd = MqttToFluentd('broker.emqx.io', 'TWF7GH/#')
mqtt_to_fluentd.start()
