import redis
import json
import paho.mqtt.publish as publish
import time


class RedisMQTT:

    def __init__(self, redis_host, redis_port, mqtt_host, mqtt_port):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.r = redis.Redis(host=redis_host, port=redis_port)

    def set_data(self, board_id, action_data: str):
        data = "000"
        if action_data.lower() == "water off":
            data = "000"
        elif action_data.lower() == "water on":
            data = "001"

        elif action_data.lower() == "light off":
            data = "010"

        elif action_data.lower() == "light on":
            data = "011"

        elif action_data.lower() == "fan off":
            data = "100"

        elif action_data.lower() == "fan on":
            data = "101"

        elif action_data.lower() == "heater off":
            data = "110"

        elif action_data.lower() == "heater on":
            data = "111"
        else:
            return False

        key = f"{board_id}"
        self.r.set(key, data)
        return True

    def check_and_publish(self):
        while True:
            time.sleep(1)  # sleep for 1 second before checking again
            for key in self.r.scan_iter("*"):
                topic = str(key.decode('utf-8'))
                data = self.r.get(key).decode('utf-8')
                publish.single(f"TWF7GH/S:{topic}", data, hostname=self.mqtt_host, port=self.mqtt_port)
                self.r.delete(key)


if __name__ == '__main__':
    aaa = RedisMQTT('localhost', 6379, 'localhost', 1883)
    aaa.check_and_publish()
