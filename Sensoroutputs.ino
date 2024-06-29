#include <DHT.h>
#include "esp_system.h"

// PINS
#define DHTPIN 27
#define SOIL_MOISTURE_PIN_1 15 // GPIO PIN 2 Have input of internal led causing some power consumption using PIN 15 as alternate
#define SOIL_MOISTURE_PIN_2 4
#define MQ135_PIN 34

// DHT TYPE AND INIT
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200); //Baud rate
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

  // Read temperature and humidity from DHT11
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
  }

  // Read the soil moisture sensor values
  int soilMoistureValue1 = analogRead(SOIL_MOISTURE_PIN_1);
  int soilMoistureValue2 = analogRead(SOIL_MOISTURE_PIN_2);

  // Read the MQ135 sensor value
  int mq135Value = analogRead(MQ135_PIN);

  // Print the sensor values to the Serial Monitor
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" *C\t");
  Serial.print("Soil Moisture 1: ");
  Serial.print(soilMoistureValue1);
  Serial.print("\tSoil Moisture 2: ");
  Serial.print(soilMoistureValue2);
  Serial.print("\tMQ135 Value: ");
  Serial.println(mq135Value);

  // Wait a few seconds between measurements.
  delay(2000);
}
