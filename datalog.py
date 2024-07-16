import serial
import pandas as pd
from datetime import datetime
import os

# Prompt the user to enter the serial port
print("===FOSTEREUM===")
print("DATALOG2 TYPE XLSX")
serial_port = input("Enter the serial port (e.g., COM5): ")

# Configure the serial port and baud rate
try:
    ser = serial.Serial(serial_port, 115200)  # Change 'COM5' to the appropriate serial port
except serial.serialutil.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
    exit(1)

# Define the base file path
base_path = 'data.xlsx'

# Function to get the next available file name
def get_next_file_path(base_path):
    if not os.path.exists(base_path):
        return base_path
    base, ext = os.path.splitext(base_path)
    i = 1
    while os.path.exists(f"{base}{i}{ext}"):
        i += 1
    return f"{base}{i}{ext}"

# Determine the file path to save the Excel file
file_path = get_next_file_path(base_path)

# Load existing data if file exists, else create a new DataFrame
if os.path.exists(base_path):
    existing_data = pd.read_excel(base_path)
else:
    existing_data = pd.DataFrame(columns=["Time", "Humidity", "PPM", "Soil Moisture 1", "Soil Moisture 2"])

try:
    new_rows = []
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Raw data: {line}")
            # Parse the data
            parts = line.split()
            if len(parts) == 14:  # Update this based on the actual data format
                # Parse the actual values from the output
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                humidity = parts[2]
                temperature = parts[5]
                soil_moisture_1 = parts[8]
                soil_moisture_2 = parts[11]
                mq135_value = parts[14]
                
                # Append to the DataFrame
                new_data = {
                    "Time": timestamp,
                    "Humidity": humidity,
                    "PPM": mq135_value,
                    "Soil Moisture 1": soil_moisture_1,
                    "Soil Moisture 2": soil_moisture_2
                }
                new_rows.append(new_data)
                print(f"Data appended: {new_data}")

            if len(new_rows) >= 10:  # Adjust the batch size as needed
                print(f"Appending {len(new_rows)} rows to the DataFrame.")
                existing_data = pd.concat([existing_data, pd.DataFrame(new_rows)], ignore_index=True)
                new_rows = []
                # Save to Excel file
                try:
                    print(f"Saving data to {file_path}.")
                    existing_data.to_excel(file_path, index=False)
                    print(f"Data saved to {file_path}")
                except Exception as e:
                    print(f"Error saving data to Excel file: {e}")

except KeyboardInterrupt:
    print("Interrupted")
    ser.close()
except serial.serialutil.SerialException as e:
    print(f"Serial port error: {e}")
finally:
    if ser.is_open:
        ser.close()
    # Save the final batch of data
    if new_rows:
        print(f"Appending final {len(new_rows)} rows to the DataFrame.")
        existing_data = pd.concat([existing_data, pd.DataFrame(new_rows)], ignore_index=True)
    try:
        print(f"Saving final data to {file_path}.")
        existing_data.to_excel(file_path, index=False)
        print(f"Final data saved to {file_path}")
    except Exception as e:
        print(f"Error saving final data to Excel file: {e}")
