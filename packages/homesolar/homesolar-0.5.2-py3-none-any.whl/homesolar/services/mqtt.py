import asyncio

from loguru import logger
from paho.mqtt import client as paho_mqtt

# project's imports
from ..interfaces import database
from ..utils import config
from ..utils.mqtt import MqttTopic

mqtt_client = None
connected_clients = []


def initialize():
    try:
        global mqtt_client
        mqtt_client = paho_mqtt.Client()

        host = config.homesolar_config['MQTT']['host']
        port = config.homesolar_config['MQTT']['port']
        username = config.homesolar_config['MQTT']['username']
        password = config.homesolar_config['MQTT']['password']
        keepalive = config.homesolar_config['MQTT']['keepalive']
        reconnect = config.homesolar_config['MQTT']['reconnect_delay']

        mqtt_client.reconnect_delay_set(max_delay=reconnect)
        mqtt_client.on_message = on_message
        mqtt_client.on_connect = on_connect
        mqtt_client.username_pw_set(username, password)
        mqtt_client.connect(host, port, keepalive)
        mqtt_client.loop_forever()
    except Exception as e:
        logger.exception(f"Something went wrong when initialize client: {e}")


def on_message(current_client: paho_mqtt.Client, userdata, msg):
    # Handles messages on Sensors Topic
    if MqttTopic.SENSORS[:-2] in str(msg.topic):
        sensor_name = str(msg.topic).replace(MqttTopic.SENSORS[:-2] + "/", "")
        data = {
            "name": sensor_name,
            "payload": msg.payload
        }

        asyncio.run(database.write_sensor_data(data))

    # Handles messages on Request Topic
    elif MqttTopic.REQUEST[:-2] in str(msg.topic):
        pass

    # Handles messages on Client Topic
    elif MqttTopic.CLIENT[:-2] in str(msg.topic):
        logger.debug("Client updated")
        client_id = str(msg.topic).replace(MqttTopic.CLIENT[:-2] + "/", "")
        status = str(msg.payload, 'utf-8')
        try:
            if status == "Connected":
                connected_clients.append(client_id)
            else:
                connected_clients.remove(client_id)
        except Exception as e:
            logger.warning(f"Something went wrong when processing clients connection {e}")


def on_connect(current_client: paho_mqtt.Client, userdata, flags, reconnect):
    try:
        current_client.subscribe(MqttTopic.SENSORS)
        current_client.subscribe(MqttTopic.REQUEST)
        current_client.subscribe(MqttTopic.CLIENT)
        message = "Client reconnected successfully" if reconnect else "Client connected successfully"
        logger.info(message)
    except Exception as e:
        logger.exception(f"Something went wrong while trying to subscribes {e}")
