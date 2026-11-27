import serial
import csv
import time
import matplotlib.pyplot as plt
from google import genai

from datetime import datetime



PORT = "COM3"

FILE = "weather_data.csv"

API_KEY = "GEMINI_API_KEY"
MODEL = "gemini-3.8-flash"

file = open(FILE, "w", newline="")
writer = csv.writer(file)

writer.writerow([
    "Time",
    "Temperature",
    "Humidity",
    "Water",
    "Rain",
    "Light"
])

file.close()



def connect_arduino():

    arduino = serial.Serial(PORT, 9600, timeout=5)

    time.sleep(2)

    return arduino



def get_weather(arduino):

    line = arduino.readline().decode("utf-8").strip()

    if line == "":
        return {}

    values = line.split(",")

    if len(values) != 5:
        return {}

    try:

        weather = {
            "temperature": float(values[0]),
            "humidity": float(values[1]),
            "water": float(values[2]),
            "rain": float(values[3]),
            "light": float(values[4])
        }

        return weather

    except ValueError:

        return {}



def save_data(weather):

    file = open(FILE, "a", newline="")

    writer = csv.writer(file)

    writer.writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        weather["temperature"],
        weather["humidity"],
        weather["water"],
        weather["rain"],
        weather["light"]
    ])

    file.close()



def current_weather():

    arduino = connect_arduino()

    print("\nReading weather...")

    weather = get_weather(arduino)

    while weather == {}:
        weather = get_weather(arduino)

    arduino.close()

    print("\n----- CURRENT WEATHER -----")

    print("Temperature:", weather["temperature"], "C")
    print("Humidity:", weather["humidity"], "%")
    print("Water Level (raw):", weather["water"])
    print("Rain Sensor (raw):", weather["rain"])
    print("Light Sensor (raw):", weather["light"])

    print("---------------------------")



def start_monitoring():

    arduino = connect_arduino()

    print("\nWeather monitoring started!")

    number = int(input("How many readings do you want to collect? "))

    for i in range(number):

        weather = get_weather(arduino)

        if weather != {}:

            save_data(weather)

            print("\nReading:", i + 1)

            print("Temperature:", weather["temperature"])
            print("Humidity:", weather["humidity"])
            print("Water:", weather["water"])
            print("Rain:", weather["rain"])
            print("Light:", weather["light"])

        else:

            print("Invalid reading. Skipping.")

    arduino.close()

    print("\nData saved successfully!")



def read_data():

    records = []

    file = open(FILE, "r")

    reader = csv.reader(file)

    for row in reader:

        if len(row) == 6 and row[0] != "Time":
            records.append(row)

    file.close()

    return records



def analyse_weather():

    records = read_data()

    if len(records) == 0:
        print("No data available.")
        return

    temperature = []
    humidity = []
    water = []
    rain = []
    light = []

    for row in records:

        temperature.append(float(row[1]))
        humidity.append(float(row[2]))
        water.append(float(row[3]))
        rain.append(float(row[4]))
        light.append(float(row[5]))

    print("\n----- WEATHER ANALYSIS -----")

    print("Total Readings:", len(records))

    print("\nTemperature")
    print("Average:", sum(temperature) / len(temperature))
    print("Maximum:", max(temperature))
    print("Minimum:", min(temperature))

    print("\nHumidity")
    print("Average:", sum(humidity) / len(humidity))
    print("Maximum:", max(humidity))
    print("Minimum:", min(humidity))

    print("\nWater Level (raw)")
    print("Maximum:", max(water))

    print("\nRain Sensor (raw)")
    print("Average:", sum(rain) / len(rain))

    print("\nLight Sensor (raw)")
    print("Average:", sum(light) / len(light))



def show_graphs():

    records = read_data()

    if len(records) == 0:
        print("No data available.")
        return

    dates = []
    temperature = []
    humidity = []
    water = []
    rain = []
    light = []

    for row in records:

        dates.append(row[0])
        temperature.append(float(row[1]))
        humidity.append(float(row[2]))
        water.append(float(row[3]))
        rain.append(float(row[4]))
        light.append(float(row[5]))

    plt.figure()
    plt.plot(dates, temperature)
    plt.title("Temperature History")
    plt.xlabel("Time")
    plt.ylabel("Temperature (C)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.figure()
    plt.plot(dates, humidity)
    plt.title("Humidity History")
    plt.xlabel("Time")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.figure()
    plt.plot(dates, water)
    plt.title("Water Level History")
    plt.xlabel("Time")
    plt.ylabel("Water Sensor Reading")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.figure()
    plt.plot(dates, rain)
    plt.title("Rain Sensor History")
    plt.xlabel("Time")
    plt.ylabel("Rain Sensor Reading")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.figure()
    plt.plot(dates, light)
    plt.title("Light History")
    plt.xlabel("Time")
    plt.ylabel("LDR Reading")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def ai_analysis():

    records = read_data()

    if len(records) == 0:
        print("No previous data available.")
        return

    # Use the last 10 readings

    previous_data = ""

    start = len(records) - 10

    if start < 0:
        start = 0

    for i in range(start, len(records)):

        previous_data = previous_data + str(records[i]) + "\n"

    prompt = """
    Analyse these previous weather sensor readings:

    """ + previous_data + """

    Explain:
    1. Temperature trends.
    2. Humidity changes.
    3. Rain-related sensor patterns.
    4. Light intensity changes.
    5. Possible upcoming conditions if these trends continue.

    This is only a trend-based estimate, not an actual
    weather forecast. Do not invent missing measurements.

    Explain everything in simple language.
    """

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    print("\n----- GEMINI ANALYSIS -----")
    print(response.text)

# MAIN MENU

while True:

    print("\n==============================")
    print("    WEATHER MONITORING SYSTEM")
    print("==============================")

    print("1. Current Weather")
    print("2. Start Weather Monitoring")
    print("3. Analyse Previous Data")
    print("4. Show Weather Graphs")
    print("5. Gemini AI Analysis")
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        current_weather()

    elif choice == "2":

        start_monitoring()

    elif choice == "3":

        analyse_weather()

    elif choice == "4":

        show_graphs()

    elif choice == "5":

        ai_analysis()

    elif choice == "6":

        print("Program Closed.")
        break

    else:

        print("Invalid choice!")