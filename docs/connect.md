### Connecting Sensors and Relays to GPIO pins
Please be aware that there are multiple ways of referring to the pins on the Raspberry Pi GPIO board. When connecting peripherals to the Raspberry Pi please refer to the pins by their GPIO names, this is known as BCM naming (Broadcom Pin Number). A handy reference for pin numbering can be accessed on the Raspberry Pi by opening a terminal window and running the command `pinout` or check out [pinout.xyz](https://pinout.xyz/) which is another great visual tool.

You may connect the peripherals using any configuration you wish, however, the FruxePi application uses these pins as default. Pins can easily be changed from the dashboard when enabling or disabling peripherals. 

#### Climate Sensor

Connect the DHT22 sensor using the following GPIO pin configuration.
- 3v3 Power (Physical pin 1)
- Ground (Physical pin 6)
- Data (Physical pin 3)  

#### Moisture Probe

Connect the TE215 moisture probe using the following GPIO pin configuration.
- 3v3 Power (Physical pin 1)
- Ground (Physical pin 6)
- Data (Physical pin 13)

#### Relays

The FruxePi uses a 5V 3-channel relay to control the lights, fans and water pump, which are connected to their respective AC power plug. Relays can be connected in any configuration (1/2/3 channel).    

For many, this is step arguably the trickiest part of setting up the FruxePi. A power strip controlled by the Raspberry Pi is a common project found online and many tutorials are available which can offer guidance on how to wire a relay power outlet appropriately. A few tutorials we found particularly helpful were:

- [Web Controlled 8-Channel Powerstrip](https://www.instructables.com/id/Web-Controlled-8-Channel-Powerstrip/)

> It goes without saying, but for some reason we still have it say it. Please be careful and exercise the utmost caution when working with high voltage electricity. Err on the side of caution and get some help if you're confused or lost in the process. Let's all be safe people! 

**Lights**
</br>Connect the fan relay using the following GPIO pin configuration.
- 3v3 Power (Physical pin 1)
- Ground (Physical pin 6)
- Data (Physical pin 13)

**Fans**
</br>Connect the fan relay using the following GPIO pin configuration.
- 3v3 Power (Physical pin 1)
- Ground (Physical pin 6)
- Data (Physical pin 13)

**Pump**
</br>Connect the pump relay using the following GPIO pin configuration.
- 3v3 Power (Physical pin 1)
- Ground (Physical pin 6)
- Data (Physical pin 13)

---

#### Enable Sensors & Relays

Enabling and disabling sensors is easy from the dashboard using the slide toggle. You may also run the diagnostics function to test if the peripherals are connected properly.