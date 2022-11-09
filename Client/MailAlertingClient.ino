#include "PubSubClient.h"
#include "WiFi.h"

const char* ssid = "<SSID>";
const char* password =  "<WIFI_Password>";
const char* MQTT_BROKER_IP = "<MQTT_BROKER_IP>"
const int MQTT_BROKER_PORT = 1883
const char* MQTT_CLIENT_NAME = "maclient"

const int SENSOR_PIN = 13;
const char* STATUS_TOPIC = "mailbox/state";

WiFiClient wifiClient;
PubSubClient client(wifiClient);
bool wifiStarted = false;
bool highStateSent = false;

void setup() {
  // Serial.begin(115200);
  pinMode(SENSOR_PIN, INPUT);
  client.setServer(MQTT_BROKER_IP, MQTT_BROKER_PORT);
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_13,0); //1 = High, 0 = Low
  wifiStarted = false;
  highStateSent = false;
}

void loop() {

  if(!wifiStarted){
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      // Serial.println("Connecting to WiFi..");
    }
    wifiStarted = true;
  }

  int currentState = digitalRead(SENSOR_PIN);
  if (client.connect(MQTT_CLIENT_NAME)) {
    if(currentState == LOW){
      if(!highStateSent){
        // Serial.println("SENDING LOW");
        client.publish(STATUS_TOPIC, "LOW", true);
        highStateSent = true;
      }
    } else {
      // Serial.println("SENDING HIGH");
      client.publish(STATUS_TOPIC, "HIGH", true);
      // Serial.println("Going to sleep now");
      delay(1000);
      esp_deep_sleep_start();
    }
  }
}
