import serial
import pandas as pd
from datetime import datetime

# Configure the serial port and baud rate
ser = serial.Serial('COM5', 115200)
#                      ^COM port

# Create a DataFrame to store the data
data = pd.DataFrame(columns=["Timestamp", "Humidity (%)", "Temperature (C)", "Soil Moisture 1", "Soil Moisture 2", "MQ135 Value"])

# File path to save the Excel file
file_path = 'F:/Fostereum/data.xlsx'

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(line)
            # Parse the data
            parts = line.split(',')
            if len(parts) == 6:
                timestamp, humidity, temperature, soil_moisture_1, soil_moisture_2, mq135_value = parts
                # Append to the DataFrame
                data = data.append({
                    "Timestamp": timestamp,
                    "Humidity (%)": humidity,
                    "Temperature (C)": temperature,
                    "Soil Moisture 1": soil_moisture_1,
                    "Soil Moisture 2": soil_moisture_2,
                    "MQ135 Value": mq135_value
                }, ignore_index=True)
                # Save to Excel file
                data.to_excel(file_path, index=False)

except KeyboardInterrupt:
    print("Interrupted")
    ser.close()
