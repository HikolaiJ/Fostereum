#include <WiFi.h>
#include <DHT.h>
#include "time.h"

// Replace with your network credentials
const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

// NTP server to request time
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 0;
const int daylightOffset_sec = 3600;

// PINS
#define DHTPIN 27
#define SOIL_MOISTURE_PIN_1 15
#define SOIL_MOISTURE_PIN_2 4
#define MQ135_PIN 34

// DHT TYPE AND INIT
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200); // Baud rate
  dht.begin();
  pinMode(SOIL_MOISTURE_PIN_1, INPUT);
  pinMode(SOIL_MOISTURE_PIN_2, INPUT);
  pinMode(MQ135_PIN, INPUT);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize NTP
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

String getFormattedTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return "N/A";
  }
  char timeStringBuff[50];
  strftime(timeStringBuff, sizeof(timeStringBuff), "%Y-%m-%d %H:%M:%S", &timeinfo);
  return String(timeStringBuff);
}

void loop() {
  // Check for incoming serial data
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove any leading/trailing whitespace

    if (command.equalsIgnoreCase("Stop")) {
      Serial.println("Stopping and restarting...");
      delay(100);  // Give some time for the message to be sent before restarting
      esp_restart();  // Trigger a reset
    }
  }

  // Read temperature and humidity from DHT22
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;  // Skip the rest of the loop
  }

  // Read the soil moisture sensor values
  int soilMoistureValue1 = analogRead(SOIL_MOISTURE_PIN_1);
  int soilMoistureValue2 = analogRead(SOIL_MOISTURE_PIN_2);

  // Read the MQ135 sensor value
  int mq135Value = analogRead(MQ135_PIN);

  // Get current time
  String timestamp = getFormattedTime();

  // Print the sensor values to the Serial Monitor
  Serial.print(timestamp);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(soilMoistureValue1);
  Serial.print(",");
  Serial.print(soilMoistureValue2);
  Serial.print(",");
  Serial.println(mq135Value);

  // Wait a few seconds between measurements
  delay(10000);
}
