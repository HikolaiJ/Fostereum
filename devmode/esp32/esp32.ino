//FOSTEREUMESP32CODE
//WARNING: Do not change anything if you don't know what your'e doing!

/included libraries
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <time.h>

// PINS
#define DHTPIN 33
#define SOIL_MOISTURE_PIN_1 32
#define MQ135_PIN 34
#define LED 2
#define RELAY2_PIN 18
#define RELAY1_PIN 19
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// WiFi credentials
const char* ssid = ("enter wifi name"); // Wifi Name
const char* password = ("enter password");  // Change to your password

// Flask server URL
const char* serverUrl = ("http://***.***.***:5000/sensor_data");

// NTP client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 25200, 60000); // WIB is UTC +7 (25200 seconds)

void setup() {
  Serial.begin(115200); // Baud rate
  dht.begin();
  pinMode(SOIL_MOISTURE_PIN_1, INPUT);
  pinMode(MQ135_PIN, INPUT);
  pinMode(LED, OUTPUT);
  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);
  digitalWrite(RELAY2_PIN, HIGH); //prevents relay from turning on while initializing
  digitalWrite(RELAY1_PIN, HIGH);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println("Server URL connected to: " + String(serverUrl));
  Serial.println("Initializing...");
  delay(3000);

  // Initialize NTP client
  timeClient.begin();

}

void loop() {
  // Default states
  String lampstate = "0";
  String pumpstate = "0";

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

  // Update the NTP client
  timeClient.update();

  // Read temperature and humidity from DHT22 with error handling
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor after multiple attempts!");
    return;
  }

  // Read the soil moisture sensor values
  int soilMoistureValue1 = analogRead(SOIL_MOISTURE_PIN_1);
  int soilMoisturePercentage = map(soilMoistureValue1, 4095, 0, 0, 100);

  // Read the MQ135 sensor value
  int mq135Value = analogRead(MQ135_PIN);

  // Get the formatted time
  String formattedTime = timeClient.getFormattedTime();

  // Get the formatted date
  time_t rawTime = timeClient.getEpochTime();
  struct tm *timeInfo = localtime(&rawTime);
  char formattedDate[11];
  strftime(formattedDate, sizeof(formattedDate), "%m/%d/%Y", timeInfo);

// Control relay2 for lamp based on time
  if ((timeInfo->tm_hour >= 17 && timeInfo->tm_min >= 20) || (timeInfo->tm_hour >= 18 && timeInfo->tm_hour < 24)) {
    digitalWrite(RELAY1_PIN, LOW);
    lampstate = "1";
  } else {
    digitalWrite(RELAY1_PIN, HIGH);
  }

  // Control relay1 for pump based on soil moisture
  if (soilMoisturePercentage < 31) {
    digitalWrite(RELAY2_PIN, LOW);
    delay(4000); // Relay1 on for 4 seconds
    digitalWrite(RELAY2_PIN, HIGH);
    pumpstate = "1";
  }

  // Prepare JSON payload
  String payload = "{";
  payload += "\"timestamp\": \"" + String(formattedDate) + " " + formattedTime + "\",";
  payload += "\"humidity\": \"" + String(humidity) + "%\",";
  payload += "\"temperature\": \"" + String(temperature) + "C*\",";
  payload += "\"soilMoisture\": \"" + String(soilMoisturePercentage) + "%\",";
  payload += "\"mq135\": \"" + String(mq135Value) + "\",";
  payload += "\"lamp\": \"" + String(lampstate) + "\",";
  payload += "\"pump\": \"" + String(pumpstate) + "\"";
  payload += "}";

  digitalWrite(LED, HIGH);
  delay(350);
  digitalWrite(LED, LOW);

  // Send data to Flask server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi not connected");
  }

  
  // Wait a few seconds between measurements.
  Serial.print("Timestamp: ");
  Serial.print(formattedDate);
  Serial.print(" ");
  Serial.print(formattedTime);
  Serial.print("\tHumidity: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" *C\t");
  Serial.print("Soil Moisture 1: ");
  Serial.print(soilMoisturePercentage);
  Serial.print(" %\t");
  Serial.print("\tMQ135 Value: ");
  Serial.print(mq135Value);
  Serial.print("\tpumpstate: ");
  Serial.print(pumpstate);
  Serial.print("\tlampstate: ");
  Serial.println(lampstate);

  if (pumpstate == "triggered") {
  delay(895650); // Delay for 14.1 minutes if pumpstate is "triggered/1"
} else {
  delay(899650); // Delay for 15 minutes if pumpstate is not "triggered/0"
}

  //if (pumpstate == "triggered") {
  //delay(1650); // Delay for 1.65 seconds if pumpstate is "triggered/1"
//} else {
//  delay(6650); // Delay for 6.65 seconds if pumpstate is not "triggered/0"
//}

  //delay(899650); // delay to send another data for 15 minutes
}
