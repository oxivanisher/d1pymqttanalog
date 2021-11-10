# d1pymqttanalog
MicroPython based program for sending analog values to mqtt

# Resources
The MQTT lib (umqttsimple.py) is taken from: https://raw.githubusercontent.com/RuiSantosdotme/ESP-MicroPython/master/code/MQTT/umqttsimple.py

## Setup dev env
* https://randomnerdtutorials.com/micropython-esp32-esp8266-vs-code-pymakr/
* https://randomnerdtutorials.com/install-upycraft-ide-windows-pc-instructions/
* https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

## How I upload the stuff
Since I have not yet managed to get this running in PyCharm, I
1) Flash uPython to the device with uPyCraft
1) Connect to it in uPyCraft
1) Open all four files (`boot.py`, `umqttsimple.py`, `main.py` and `config.json`) in uPyCraft
1) Hit DownloadAndRun for all the open files
1) DownloadAndRun `boot.py` and it should connect to the WiFi and show you the MAC address
