import argparse
import paho.mqtt.client as mqtt
import serial
import time

import helper

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dev", help="serial device", required=True)
parser.add_argument("-b", "--baud", help="serial baud rate", type=int, default=19200)
parser.add_argument("-m", "--mqtt-server", help="MQTT server address", required=True)
parser.add_argument("-c", "--mqtt-credentials", help="MQTT server credentials [user]:[password]", required=True)
parser.add_argument("-p", "--topic-prefix", help="topic prefix for MQTT", required=True)
parser.add_argument("-i", "--interval", help="polling intervall for CO2 in seconds", default=60)

args = parser.parse_args()

mqttSplitUrl = args.mqtt_server.split(":")

mqttAddress = mqttSplitUrl[0]
mqttPort = 1883

if len(mqttSplitUrl) == 2:
    mqttPort = int(mqttSplitUrl[1])

client = mqtt.Client()

if args.mqtt_credentials:
    splitCredentials = args.mqtt_credentials.split(":")
    username = splitCredentials[0]
    password = None
    if len(splitCredentials) == 2:
        password = splitCredentials[1]
    client.username_pw_set(username, password)

client.connect(mqttAddress, mqttPort, 60)
client.loop_start()

co2Topic = args.topic_prefix + "/co2"

ser = serial.Serial(args.dev, args.baud, timeout=1, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)

while True:
    req = bytes([0x15, 0x04, 0x13, 0x8B, 0x00, 0x01])
    ser.write(req + helper.calc_crc(req))
    time.sleep(0.05)
    resp = ser.read(8)

    if not resp or resp[1] != 0x04:
        print(f"Invalid response: {resp}")
        continue

    co2 = resp[3] * 256 + resp[4]

    print(f"Got new sample: CO2={co2}ppm")
    client.publish(co2Topic, payload=co2, qos=1)

    time.sleep(int(args.interval))
