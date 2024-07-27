#include <DHT.h>
#include "esp_system.h"

// PINS
#define DHTPIN 33
#define SOIL_MOISTURE_PIN_1 32
#define MQ135_PIN 34
#define RELAY_PIN_1 18 // Relay for soil moisture
#define RELAY_PIN_2 19 // Relay for temperature

// DHT TYPE AND INIT
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200); // Baud rate
  dht.begin();
  pinMode(SOIL_MOISTURE_PIN_1, INPUT);
  pinMode(MQ135_PIN, INPUT);
  pinMode(RELAY_PIN_1, OUTPUT); // Set relay pin 1 as output
  pinMode(RELAY_PIN_2, OUTPUT); // Set relay pin 2 as output
  digitalWrite(RELAY_PIN_1, HIGH); // Turn off relay 1 initially
  digitalWrite(RELAY_PIN_2, HIGH); // Turn off relay 2 initially
}

void loop() {
  // Check for incoming serial data
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove any leading/trailing whitespace

    if (command.equalsIgnoreCase("Stop")) {
      Serial.println("Stopping and restarting...");
      delay(100); 
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

  // Read the MQ135 sensor value
  int mq135Value = analogRead(MQ135_PIN);
  int soilMoisturePercentage = map(soilMoistureValue1, 4095, 0, 0, 100);

  // Print the sensor values to the Serial Monitor
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" *C\t");
  Serial.print("Soil Moisture: ");
  Serial.print(soilMoisturePercentage);
  Serial.print(" %\t");
  Serial.print("\tMQ135 Value: ");
  Serial.println(mq135Value);

  // Control the relays based on the conditions
  if (soilMoisturePercentage < 25) {
    digitalWrite(RELAY_PIN_1, LOW); // Turn on relay 1
  } else {
    digitalWrite(RELAY_PIN_1, HIGH); // Turn off relay 1
  }

  if (temperature < 25) {
    digitalWrite(RELAY_PIN_2, LOW); // Turn on relay 2
  } else {
    digitalWrite(RELAY_PIN_2, HIGH); // Turn off relay 2
  }

  // Wait a few seconds between measurements.
  delay(5000);
}
