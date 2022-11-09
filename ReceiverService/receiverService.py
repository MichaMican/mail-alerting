#!/usr/bin/env python3

import time
import paho.mqtt.client as mqtt
from pushnotifier import PushNotifier as pn

MQTT_BROKER_IP = "<MQTT_BROKER_IP>"
MQTT_BROKER_PORT = 1883
DEVICES_FOR_NOTIFICATION = None  # ['AB12']
DEVICES_FOR_IMPLICIT_NOTIFICATION = None  # ['AB12']
MAILBOX_OPEN_TEXT = "Mailbox was opened"
MAILBOX_STATE_MISSED_TEXT = "Mailbox was opened (explicit open state missed)"

PUSH_NOTIFIER_USER_NAME = "<PushNotifier UserName>"
PUSH_NOTIFIER_PASSWORD = "<PushNotifier Password>"
PUSH_NOTIFIER_PACKAGE_NAME = "<PushNotifier PackageName>"
PUSH_NOTIFIER_API_KEY = "<PushNotifier APIKey>"

print("Sleeping for 60 seconds to give the mqtt broker time to start")
time.sleep(60)
print("Starting script")

pn = pn.PushNotifier(
    PUSH_NOTIFIER_USER_NAME, PUSH_NOTIFIER_PASSWORD, PUSH_NOTIFIER_PACKAGE_NAME, PUSH_NOTIFIER_API_KEY)

HIGH_STATE = b'HIGH'
LOW_STATE = b'LOW'

last_status = HIGH_STATE
is_first_message = True


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("mailbox/#", 2)


def on_message(client, userdata, msg):
    global last_status
    global is_first_message
    print(msg.topic+" "+str(msg.payload))

    if last_status != msg.payload and msg.payload == LOW_STATE:
        pn.send_text(MAILBOX_OPEN_TEXT, silent=False,
                     devices=DEVICES_FOR_NOTIFICATION)

    # explicit open state was missed
    if last_status == msg.payload and not is_first_message:
        pn.send_text(MAILBOX_STATE_MISSED_TEXT, silent=True,
                     devices=DEVICES_FOR_IMPLICIT_NOTIFICATION)

    last_status = msg.payload
    is_first_message = False


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER_IP, MQTT_BROKER_PORT, 60)
client.loop_forever()
