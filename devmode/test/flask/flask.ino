#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* hh = "BMW";
const char* hhp = ".,Byan12345";
const char* ho = "SKHOOD 5G EXT";
const char* hop = "Bismillah1378";
const char* of = "XTNET";
const char* ofp = "Xst45ansr";

const char* ssid = (ho);
const char* password = (hop);  // Change to your password

// Flask server URL
const char* srv1 = "http://192.168.246.88:5000/sensor_data";
const char* srv2 = "http://192.168.0.202:5000/sensor_data";
const char* serverUrl = (srv2);

void setup() {
  Serial.begin(115200); // Baud rate

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println("Server URL connected to: " + String(serverUrl));
}

void loop() {
  // Message to send
  String payload = "{\"message\": \"test\"}";

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

  // Wait 5 seconds before sending the next message
  delay(5000);
}
