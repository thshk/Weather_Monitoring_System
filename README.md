# Arduino-Based Weather Monitoring and Analysis System 🌦️

An Arduino and Python project that collects environmental readings from multiple sensors, stores them with timestamps, analyses historical data, displays graphs, and uses Google Gemini AI to explain patterns in the collected readings.

## Project Overview

The system uses an Arduino Uno to collect readings from a DHT11 temperature and humidity sensor, a water-level sensor, a raindrop sensor, and an LDR. Arduino sends the readings to a Python program through USB serial communication.

Python provides a menu-driven interface to view current readings, collect and save data, analyse previous records, generate graphs, and request an AI-generated explanation of recent sensor trends.

## Features

- **Current readings:** Displays the latest temperature, humidity, water sensor, raindrop sensor, and light sensor readings.
- **Data collection:** Collects a user-selected number of readings from the Arduino.
- **Timestamped storage:** Saves each valid reading with its date and time in a CSV file.
- **Historical analysis:** Calculates average, maximum, and minimum temperature and humidity, along with selected statistics for the other sensors.
- **Graph generation:** Creates separate time-series graphs for temperature, humidity, water sensor readings, raindrop sensor readings, and LDR readings.
- **Gemini AI analysis:** Sends the latest 10 stored readings to Google Gemini for a simple explanation of observed patterns and possible trend-based conditions.
- **Menu-driven interface:** Makes the program easy to operate through numbered options.
- **Persistent records:** Keeps collected readings in a CSV file so they can be analysed again when the program is restarted.

## Hardware Components

- Arduino Uno
- DHT11 temperature and humidity sensor
- Water-level sensor
- Raindrop sensor
- LDR (Light Dependent Resistor)
- Jumper wires and USB cable
- Breadboard (if required)

## Sensor Connections

The following pin assignments match the example Arduino sketch used with this project:

| Component | Arduino pin |
|---|---|
| DHT11 data | Digital pin 2 |
| Water-level sensor analog output | A0 |
| Raindrop sensor analog output | A1 |
| LDR output | A2 |
| Sensor VCC | 5V (as supported by the module) |
| Sensor GND | GND |

Check the labels and voltage requirements of your specific sensor modules before connecting them.

## Software and Libraries

**Arduino**
- Arduino IDE
- DHT sensor library by Adafruit
- Adafruit Unified Sensor library

**Python**
- Python 3
- PySerial
- Matplotlib
- Google Gen AI SDK (`google-genai`)
- Python built-in `csv`, `time`, and `datetime` modules

Install the Python packages:

```bash
pip install pyserial matplotlib google-genai
```

## Getting Started

### 1. Set up the Arduino

1. Connect the sensors using the pin assignments above.
2. Install the required DHT libraries in Arduino IDE.
3. Upload the Arduino sketch to your Uno.
4. Make sure the sketch sends five comma-separated values in this order:

```text
temperature,humidity,water,rain,light
```

Example serial line:

```text
27.4,68.1,423,710,645
```

The Arduino sketch and Python program must use the same serial baud rate. The example project uses **9600 baud**.

### 2. Configure the Python program

Open `main.py` and update the settings:

- Set `PORT` to the serial port used by your Arduino (for example, `COM3` on Windows).
- Set `BAUD` to the same baud rate as the Arduino sketch.
- Add your Google Gemini API key to `API_KEY`.
- Set `MODEL` to a Gemini model name currently supported by your API key.

Keep your API key private. Do not commit a real API key to a public GitHub repository. For a public project, use a placeholder in the uploaded code and enter your key locally.

### 3. Run the program

Close the Arduino IDE Serial Monitor, connect the Arduino to your computer, and run:

```bash
python main.py
```

Use the menu:

| Option | Function |
|---|---|
| 1 | Current Weather |
| 2 | Start Weather Monitoring |
| 3 | Analyse Previous Data |
| 4 | Show Weather Graphs |
| 5 | Gemini AI Analysis |
| 6 | Exit |

The program creates `weather_data.csv` automatically if it does not already exist.

## How the System Works

1. Sensors measure environmental conditions.
2. Arduino reads the sensor values and sends them to Python over serial communication.
3. Python receives and separates the five values.
4. When monitoring is selected, valid readings are saved in `weather_data.csv` with timestamps.
5. The analysis option reads the saved CSV records and calculates summary statistics.
6. The graph option plots the stored readings against time.
7. The Gemini option sends up to the latest 10 stored readings to the AI model for a text-based trend analysis.

## Benefits and Learning Outcomes

- Demonstrates communication between a microcontroller and a computer.
- Combines electronics, embedded programming, and Python in one project.
- Shows how sensor readings can be collected and stored for later use.
- Makes changes in sensor readings easier to understand through graphs.
- Introduces basic data analysis using real sensor data.
- Demonstrates how an AI API can interpret structured information and generate a natural-language summary.
- Provides a foundation for future improvements such as sensor calibration, dashboards, alerts, and longer-term environmental data analysis.

## Important Notes and Limitations

- The water-level, raindrop, and LDR values are currently **raw sensor readings**, and have to be calibrated accordingly.
- Sensor readings can vary depending on the module, wiring, placement, and surrounding conditions.
- The Gemini output is a **trend-based interpretation of the stored readings**, not a reliable meteorological forecast. Actual forecasting requires suitable weather data and forecasting methods.
- The AI analysis uses only the latest 10 saved records, so its usefulness depends on having meaningful and representative readings.
- The program needs the Arduino connected when using the current-weather and data-collection options. Historical analysis and graphs use the saved CSV file.

## Possible Future Improvements

- Add automatic data collection at configurable intervals.
- Build a graphical dashboard for live readings and historical trends.
- Add alerts when sensor readings cross user-defined thresholds.
- Combine local sensor readings with an external weather service for more informed forecasts.

## Project Purpose

This project explores how Arduino, sensors, Python, data visualisation, and generative AI can work together in a practical environmental monitoring application.
