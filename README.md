# mail-alerting
Receive a Pushnotification when someone opens your Mailbox (Postbox)

# What you'll need
- ESP32
- Reed switch
- Resistor (300 Ohm - other resistances should work too though)
- Raspberry Pi (Zero)
- Mqtt Broker (can also be installed on the Raspberry Pi)

# How to Setup

1. Replace the code as necessary and described below
2. Wire up the ESP
3. Upload MailAlertingClient.ino to ESP
4. Setup RapberryPi
5. _OPTIONAL: Install Mosquitto MQTT Broker on RasberryPi)_
6. Copy receiverService.py to /home/pi directory
7. Install pip dependencies
8. Copy MailboxReceiverService.service to /etc/systemd/system
9. Make script executable (chmod)
10. Reload systemd & enable service

## Code
1. Clone the repo
2. Replace variable values:  
**Client/MailAlertingClient.ino**  

| Variable         | Default Value | Description                                                                                                          |
| ---------------- | ------------- | -------------------------------------------------------------------------------------------------------------------- |
| wifiSSID         |               | SSID of your Wifi where MQTT Broker is accessible                                                                    |
| wifiPassword     |               | Password of your Wifi                                                                                                |
| MQTT_BROKER_IP   |               | IP of your MQTT Broker (If you run the MQTT Broker on the Raspberry Pi this will be the same IP as the Raspberry IP) |
| MQTT_BROKER_PORT | 1883          | Port of the MQTT broker.                                                                                             |
| MQTT_CLIENT_NAME | maclient      | Client name which the ESP will use to publish                                                                        |
|                  |               |                                                                                                                      |
**ReceiverService/receiverService.py**  

| Variable                          | Default Value                                   | Description                                                                                                                                                                                                                                                                                                              |
| --------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| MQTT_BROKER_IP                    |                                                 | IP of your MQTT Broker (If you run the MQTT Broker on the Raspberry Pi this will be the same IP as the Raspberry IP).                                                                                                                                                                                                    |
| MQTT_BROKER_PORT                  | 1883                                            | Port of the MQTT broker.                                                                                                                                                                                                                                                                                                 |
| DEVICES_FOR_NOTIFICATION          | None                                            | V2Ids of Devices, which should receive a notification on Mailbox open. You can target specific devices by setting this to a arry of ids e.g. `['AB12']`. The default setting will publish to all Devices.                                                                                                                |
| DEVICES_FOR_IMPLICIT_NOTIFICATION | None                                            | V2Ids of Devices, which should receive a notification on a implicit Mailbox open. This is send when the receiver Service receives two closed states without an open state in between. You can target specific devices by setting this to a arry of ids e.g. `['AB12']`. The default setting will publish to all Devices. |
| MAILBOX_OPEN_TEXT                 | Mailbox was opened                              | Text which should get pushed to the devices on Mailbox open.                                                                                                                                                                                                                                                             |
| MAILBOX_STATE_MISSED_TEXT         | Mailbox was opened (explicit open state missed) | Text which should get pushed to the devices on implicit Mailbox open. This is send when the receiver Service receives two closed states without an open state in between.                                                                                                                                                |
| PUSH_NOTIFIER_USER_NAME           |                                                 | UserName of your PushNotifier Account                                                                                                                                                                                                                                                                                    |
| PUSH_NOTIFIER_PASSWORD            |                                                 | Password of your PushNotifier Account                                                                                                                                                                                                                                                                                    |
| PUSH_NOTIFIER_PACKAGE_NAME        |                                                 | Packagename of your PushNotifier App                                                                                                                                                                                                                                                                                     |
| PUSH_NOTIFIER_API_KEY             |                                                 | APIKey of your PushNotifier Account                                                                                                                                                                                                                                                                                      |

## ESP Setup
### Dependencies
- https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html
- https://github.com/knolleary/pubsubclient
- Optional: If using a third party ESP board you might have to install drivers for the board manually

### Wiring
1. Connect a reed switch to the 3V3 PIN and the G13 (GPIO 13) pin.
2. Connect the G13 switch with the resistor to any GND (ground) pin.

## Raspberry Pi Setup
### Dependencies
- https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up
- python 3 (Usualy included with the OS)
- https://pypi.org/project/paho-mqtt/
- https://pypi.org/project/pushnotifier/
- Optional: If you want to host the MQTT broker on the Raspberry Pi https://mosquitto.org/download/

### Raspberry Pi Setup
Install Python dependencies
```console
> pip install paho-mqtt
> pip install pushnotifier
```

Setup systemd to automatically start the receiverService.py
```console
> sudo chmod 744 MailboxReceiverService.service
> sudo chmod +x MailboxReceiverService.service
> sudo systemctl daemon-reload
> sudo systemctl enable MailboxReceiverService.service
> sudo systemctl start MailboxReceiverService.service
```
> NOTE: To Debug the systemd setup you can use `sudo systemctl status MailboxReceiverService.service` for the general status and `journalctl -e -u MailboxReceiverService` for more detailed logs
