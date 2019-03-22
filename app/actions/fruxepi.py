#!/usr/bin/env python

#FruxePi - CLI

import os
import sys
import Adafruit_DHT as dht
import RPi.GPIO as GPIO
from datetime import datetime, date
from time import strftime
import pymysql
from PIL import Image
import subprocess
import time



# Script Arguments
action = None
action_option = None
action_GPIO = None
action_interval = None


# Database Credentials
host = "db"
user="frxpi"
password="password"
database="frx_db"


# Script Argument Checker
if len(sys.argv) == 5:
    action = sys.argv[1]
    action_option = sys.argv[2]
    action_GPIO = sys.argv[3]
    action_interval = sys.argv[4]
elif len(sys.argv) == 4:
    action = sys.argv[1]
    action_option = sys.argv[2]
    action_GPIO = sys.argv[3]
elif len(sys.argv) == 3:
    action = sys.argv[1]
    action_option = sys.argv[2]


# CLI Menu Function
def CLI_menu():
    # Climate
    if action == "climate":  
        # Return Temperature
        if action_option == "-t" and action_GPIO is not None:  
            fetchTemperature(action_GPIO)
        # Return Raw Temperature
        elif action_option == "-tr" and action_GPIO is not None:
            fetchRawTemperature(action_GPIO)
        # Return Humidity    
        elif action_option == "-h" and action_GPIO is not None: 
            fetchHumidity(action_GPIO) 
        # Return Raw Humidity    
        elif action_option == "-hr" and action_GPIO is not None: 
            fetchRawHumidity(action_GPIO)
        # Diagnostics
        elif action_option == "-d" and action_GPIO is not None: 
            diagnosticsClimate(action_GPIO)
        else:
            print("Invalid Command!")

    # Lights
    elif action == "lights":  
        # Lights ON
        if action_option == "-ON" and action_GPIO is not None: 
            lightsON(action_GPIO)
        # Lights OFF
        elif action_option == "-OFF" and action_GPIO is not None:
            lightsOFF(action_GPIO)
        # Light Relay State    
        elif action_option == "-s" and action_GPIO is not None:
            getGPIOState(action_GPIO) 
        # Diagnostics    
        elif action_option == "-d" and action_GPIO is not None:
            relayDiagnostics(action_GPIO)
        else:
            print("Invalid Command!")

    # Fan
    elif action == "fan":  
        # Fan ON
        if action_option == "-ON" and action_GPIO is not None: 
            fanON(action_GPIO)
        # Fan OFF
        elif action_option == "-OFF" and action_GPIO is not None:
            fanOFF(action_GPIO)
        # Fan Relay State    
        elif action_option == "-s" and action_GPIO is not None:
            getGPIOState(action_GPIO)
        # Run Fan Program    
        elif action_option == "-run" and action_GPIO is not None and action_interval is not None:
            fanProgram(action_GPIO, action_interval)  
        # Diagnostics    
        elif action_option == "-d" and action_GPIO is not None:
            relayDiagnostics(action_GPIO)
        else:
            print("Invalid Command!")

    # Pump
    elif action == "pump":  
        # Pump ON
        if action_option == "-ON" and action_GPIO is not None: 
            pumpON(action_GPIO)
        # Pump OFF
        elif action_option == "-OFF" and action_GPIO is not None:
            pumpOFF(action_GPIO)
        # Pump Relay State    
        elif action_option == "-s" and action_GPIO is not None:
            getGPIOState(action_GPIO)
        # Run Pump Program    
        elif action_option == "-run" and action_GPIO is not None and action_interval is not None:
            pumpProgram(action_GPIO, action_interval)
        # Diagnostics    
        elif action_option == "-d" and action_GPIO is not None:
            relayDiagnostics(action_GPIO)
        else:
            print("Invalid Command!")

    # Moisture
    elif action == "moisture":  
        # Get Moisture
        if action_option == "-m" and action_GPIO is not None: 
            fetchMoisture(action_GPIO)
        # Pump Moisture Raw
        elif action_option == "-mr" and action_GPIO is not None: 
            fetchRawMoisture(action_GPIO)
        # Moisture State    
        elif action_option == "-s" and action_GPIO is not None:
            getGPIOState(action_GPIO) 
        # Diagnostics    
        elif action_option == "-d" and action_GPIO is not None:
            diagnosticsMoisture(action_GPIO)
        else:
            print("Invalid Command!")
    
    # Fetch Grow Data
    elif action == "update":  
        # Update grow data
        if action_option == "-growdata": 
            growData = getGrowData()
            growDataUpdate(growData)
        # Update chart
        elif action_option == "-chart": 
            update_chart()
        else:
            print("Invalid Command!")

    # Maintenance
    elif action == "maint":  
        # Cleanup old data from database
        if action_option == "-cleanup": 
            deleteOldGrowData()
        else:
            print("Invalid Command!")
    
    # Camera
    elif action == "camera":  
        # Capture Photo
        if action_option == "-capture": 
            capturePhoto("candid")
        elif action_option == "-crop":
            capturePhoto("crop")
        # Diagnostics    
        elif action_option == "-d":
            cameraDiagnostics()
        else:
            print("Invalid Command!")
    
    else:
        print("Invalid Command!")

# Fetch Moisture
def fetchMoisture(gpioPIN):
    try:
        # Set our GPIO numbering to BCM
        GPIO.setmode(GPIO.BCM)
        # Set the GPIO pin to an input
        GPIO.setup(int(gpioPIN), GPIO.IN)
        # Get Data
        status = GPIO.input(int(gpioPIN))

        if status is not None:
            
            if status == 0:
                print("Soil Dry")
            elif status == 1:
                print("Soil Moist")
                    
        else:
            print('Failed to get reading. Try again!')
            
    except:
        print('Sensor Error!')

# Fetch Moisture Raw
def fetchRawMoisture(gpioPIN):
    try:
        # Set our GPIO numbering to BCM
        GPIO.setmode(GPIO.BCM)

        # Set the GPIO pin to an input
        GPIO.setup(int(gpioPIN), GPIO.IN)

        # Get Data
        status = GPIO.input(int(gpioPIN))

        if status is not None:
            print(status)
        else:
            print('Failed to get reading. Try again!')

    except:
        print('Sensor Error!')

def diagnosticsMoisture(gpioPIN):

    try:
        # Set our GPIO numbering to BCM
        GPIO.setmode(GPIO.BCM)

        # Set the GPIO pin to an input
        GPIO.setup(int(gpioPIN), GPIO.IN)

        # Get Data
        status = GPIO.input(int(gpioPIN))

        if status == 0 or status == 1:
            print("All good - Moisture Sensor Operational!")
        else:
            print("Sensor Error!" + str(status))

    except:
        print("Sensor Error! Script")

# Fetch Temperature
def fetchTemperature(gpioPIN):
    try:
        humidity,temperature = dht.read_retry(dht.DHT22, int(gpioPIN))

        if temperature is not None:
            data_output = str(round(temperature, 2)) + "*C"
            print(data_output)
            return data_output
        else:
            print('Failed to get reading. Try again!')
    except:
        print("Sensor Error!")

# Fetch Raw Temperature
def fetchRawTemperature(gpioPIN):
    try:
        humidity,temperature = dht.read_retry(dht.DHT22, int(gpioPIN))

        if temperature is not None:
            data_output = round(temperature, 2)
            print(data_output)
            return data_output
        else:
            print('Failed to get reading. Try again!')
    except:
        print("Sensor Error!")

# Fetch Humidity
def fetchHumidity(gpioPIN):
    try:
        humidity,temperature = dht.read_retry(dht.DHT22, int(gpioPIN))

        if humidity is not None:
            data_output = str(round(humidity, 2)) + "%"
            print(data_output)
            return data_output
        else:
            print('Failed to get reading. Try again!')
    except:
        print("Sensor Error!")

# Fetch Raw Humidity
def fetchRawHumidity(gpioPIN):
    try:
        humidity,temperature = dht.read_retry(dht.DHT22, int(gpioPIN))

        if humidity is not None:
            data_output = round(humidity, 2)
            print(data_output)
            return data_output
        else:
            print('Failed to get reading. Try again!')
    except:
        print("Sensor Error!")

def diagnosticsClimate(gpioPIN):

    try:
        humidity,temperature = dht.read_retry(dht.DHT22, int(gpioPIN))

        raw_temp = int(temperature)
        raw_humidity = int(humidity)

        if str(raw_temp).isdigit() == True and str(raw_humidity).isdigit() == True:
            print("All good - Climate Sensor Operational!")
        else:
            print("Sensor Error!")

    except:
        print("Sensor Error!")



# Fan ON
def fanON(gpioPIN):
    print("Fan ON")
    os.system("gpio -g mode " + str(gpioPIN) + " out")
    os.system("gpio -g write " + str(gpioPIN) + " 1")

# Fan OFF
def fanOFF(gpioPIN):
    print("Fan OFF")
    os.system("gpio -g mode " + str(gpioPIN) + " out")
    os.system("gpio -g write " + str(gpioPIN) + " 0")

# Fan run program
def fanProgram(gpioPIN, timeInterval):
    fanON(gpioPIN)
    time.sleep(timeInterval)
    fanOFF(gpioPIN)

# Lights ON
def lightsON(gpioPIN):
    print("Lights ON")
    #https://www.instructables.com/id/Super-Simple-Raspberry-Pi-433MHz-Home-Automation/
    
    #a_on
    code =  '1010101111101010110011001'
    #a_off = '1010101111101010110000111'

    short_delay =    0.000175
    long_delay =     0.00055
    extended_delay = 0.0096

    NUM_ATTEMPTS = 20
    TRANSMIT_PIN = str(gpioPIN)

    def transmit_code(code):
        '''Transmit a chosen code string using the GPIO transmitter'''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
        for t in range(NUM_ATTEMPTS):
            for i in code:
                if i == '1':
                    GPIO.output(TRANSMIT_PIN, 1)
                    time.sleep(short_delay)
                    GPIO.output(TRANSMIT_PIN, 0)
                    time.sleep(long_delay)
                elif i == '0':
                    GPIO.output(TRANSMIT_PIN, 1)
                    time.sleep(long_delay)
                    GPIO.output(TRANSMIT_PIN, 0)
                    time.sleep(short_delay)
                else:
                    continue
            GPIO.output(TRANSMIT_PIN, 0)
            time.sleep(extended_delay)
        GPIO.cleanup()

    #os.system("gpio -g mode " + str(gpioPIN) + " out")
    #os.system("gpio -g write " + str(gpioPIN) + " 1")

# Lights OFF
def lightsOFF(gpioPIN):
    print("Lights OFF")
    #os.system("gpio -g mode " + str(gpioPIN) + " out")
    #os.system("gpio -g write " + str(gpioPIN) + " 0")

# Pump ON
def pumpON(gpioPIN):
    print("Pump ON")
    os.system("gpio -g mode " + str(gpioPIN) + " out")
    os.system("gpio -g write " + str(gpioPIN) + " 1")

# Pump OFF
def pumpOFF(gpioPIN):
    print("Pump OFF")
    os.system("gpio -g mode " + str(gpioPIN) + " out")
    os.system("gpio -g write " + str(gpioPIN) + " 0")

# Pump run program
def pumpProgram(gpioPIN, timeInterval):
    pumpON(gpioPIN)
    time.sleep(timeInterval)
    pumpOFF(gpioPIN)

# Get GPIO state
def getGPIOState(gpioPIN):
    state = os.system("gpio -g read " + str(gpioPIN))
    return state

def relayDiagnostics(gpioPIN):
    # Set our GPIO numbering to BCM
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set the GPIO pin to an input
    GPIO.setup(int(gpioPIN), GPIO.IN)

    # Get Data
    state = GPIO.input(int(gpioPIN))
    
    if (state is True):
        print("Relay Operational!")
    else:
        print("Relay Error! Check connections and try again.")

def fetchSensorGPIO():

    # SQL query
    sql = "SELECT * FROM technical ORDER BY id ASC"

    # Connect to the database
    connection = pymysql.connect(host, user, password, database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Fetch DB Query
            cursor.execute(sql)
            result = cursor.fetchall() 
    finally:
        connection.close()

    # Format GPIO data for export
    data = {}
    data['climate_GPIO'] = result[0]['gpio_pin']
    data['moisture_GPIO'] = result[1]['gpio_pin']
    data['light_GPIO'] = result[2]['gpio_pin']
    data['fan_GPIO'] = result[3]['gpio_pin']
    data['pump_GPIO'] = result[4]['gpio_pin']
    
    return data

def getGrowData():

    GPIO = fetchSensorGPIO()

    data = {}
    data['timestamp'] = strftime("%Y-%m-%d %H:%M:%S")
    data['temperature'] = fetchRawTemperature(GPIO['climate_GPIO'])
    data['humidity'] = fetchRawHumidity(GPIO['climate_GPIO'])
    data['light_status'] = getGPIOState(GPIO['light_GPIO'])
    data['moisture_status'] = getGPIOState(GPIO['moisture_GPIO'])
    data['fan_status'] = getGPIOState(GPIO['fan_GPIO'])
    data['pump_status'] = getGPIOState(GPIO['pump_GPIO'])

    print(data)
    return data

def growDataUpdate(data):

    dbData = [data['timestamp'], data['temperature'], data['humidity'], data['light_status'], data['moisture_status'], data['fan_status'], data['pump_status']]

    db = pymysql.connect(host, user, password, database)
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO grow_data (date_time, temperature, humidity, light_status, moisture_status, fan_status, pump_status) VALUES(%s, %s, %s, %s, %s, %s, %s)", dbData)        
        db.commit()
        print("Grow Data Updated!")
    except:
        print("Database Error!")
        db.rollback()
        db.close()


def deleteOldGrowData():

    # SQL query
    sql = "DELETE FROM grow_data WHERE date_time < CURDATE()"

    # Connect to the database
    connection = pymysql.connect(host, user, password, database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Fetch DB Query
            cursor.execute(sql)
            connection.commit()
            print("Old Grow Data Deleted")
    except:
        print("Database deletion error. Delete not complete!")
    finally:
        connection.close()


def takePhoto(imgPath, imgName):
    # Filepath
    filePath = str(imgPath) + str(imgName)

    # Take Photo
    os.system("raspistill -w 800 -h 600 -o " + filePath)

    return imgName


def capturePhoto(usage):

    try:

        if usage == "crop":
            # Image Details
            imgName = "crop_bg.jpg"
            imgPath = "/var/www/html/assets/img/"
            
            # Take photo
            print(takePhoto(imgPath, imgName))

        elif usage == "candid":
            # Image Details
            timestamp = "{:%Y%m%d%H%M}".format(datetime.now())
            imgName = "FruxePi_capture_" + str(timestamp) + ".jpg"
            imgPath = "/var/www/html/assets/tmp/"
            
            # Take photo
            print(takePhoto(imgPath, imgName))

        else:
            # Image Details
            imgName = "crop_bg.jpg"
            imgPath = "/var/www/html/assets/img/"

            # Take photo
            print(takePhoto(imgPath, imgName))

    except:
        print("Camera Error!")


def cameraDiagnostics():
    status = os.popen('vcgencmd get_camera').read()
    print(status)
    

# Chart
# Fetch from sql based on string
def fetchData(sql):

    # Connect to the database
    connection = pymysql.connect(host,user,password,database,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
    finally:
        connection.close()


# update chart history function
def update_history(data):

    # Connect to the database
    connection = pymysql.connect(host,user,password,database,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO climate_history (date_time, temperature, humidity) VALUES (%s, %s, %s)"
            cursor.execute(sql, (data['date_time'], round(data['temperature']), round(data['humidity'])))

        connection.commit()
        print("Success!")
    finally:
        connection.close()


def fetch_history():

    tempQueryString = "SELECT AVG(temperature) as temperature, AVG(humidity) as humidity, date_time FROM grow_data WHERE date_time >= now() - interval 1 hour"
    tempData = fetchData(tempQueryString)

    return tempData


# Update Chart
def update_chart():
    
    try:
        # fetch chart data
        hourlyData = fetch_history()

        #update chart
        update_history(hourlyData)
        
        print("Chart Updated!")
    except Exception as e: 
        print("Chart Update Error!")
        print(e)


# RUN
CLI_menu()
