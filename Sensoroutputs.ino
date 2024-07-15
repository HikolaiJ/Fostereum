#include <DHT.h>
#include "esp_system.h"

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

  // Get current time (assuming a real-time clock is set up)
  String timestamp = String(year()) + "-" + String(month()) + "-" + String(day()) + " " + String(hour()) + ":" + String(minute()) + ":" + String(second());

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
