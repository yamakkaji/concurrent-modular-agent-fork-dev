from os import path as osp
from paho.mqtt import client as mqtt
import queue

class MessageClient():
    def __init__(self, 
                 agent_name, 
                 module_name, 
                 mqtt_broker: str = "localhost", 
                 mqtt_port: int = 1883, 
                 mqtt_qos: int = 2):
        self.agent_name = agent_name
        self.module_name = module_name
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.connect(mqtt_broker, mqtt_port)
        my_mqtt_topic = self._make_mqtt_topic(module_name)
        self._mqtt_qos = mqtt_qos
        self.mqtt_client.subscribe(my_mqtt_topic, qos=self._mqtt_qos)
        self.message_queue = queue.Queue()
        
        def on_message(client, userdata, msg):
            self.message_queue.put(msg.payload.decode())

        self.mqtt_client.on_message = on_message        
        
        self.mqtt_client.loop_start()

    def _make_mqtt_topic(self, module_name):
        return f"{__package__}/{osp.splitext(osp.basename(__file__))[0]}/{self.agent_name}/{module_name}"

    def send(self, receiver_name, message):
        target_mqtt_topic = self._make_mqtt_topic(receiver_name)
        self.mqtt_client.publish(target_mqtt_topic, message, qos=self._mqtt_qos)
    
    def receive(self, timeout=None):
        try:
            m = self.message_queue.get(block=True, timeout=timeout)
            return m
        except queue.Empty:
            return None
    
    def num_messages(self):
        return self.message_queue.qsize()

    def __del__(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()  
