import argparse
import serial
import time

import helper

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dev", help="serial device", required=True)
parser.add_argument("-b", "--baud", help="serial baud rate", type=int, default=19200)

args = parser.parse_args()

ser = serial.Serial(args.dev, args.baud, timeout=1, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)

req = bytes([0x15, 0x05, 0x03, 0xEC, 0xFF, 0x00])
ser.write(req + helper.calc_crc(req))
time.sleep(0.05)
resp = ser.read(8)

if resp != req + helper.calc_crc(req):
    print(f"Invalid response: {resp}")
    exit(-1)

while True:
    req = bytes([0x15, 0x04, 0x13, 0x8A, 0x00, 0x01])
    ser.write(req + helper.calc_crc(req))
    time.sleep(0.05)
    resp = ser.read(8)

    if not resp.startswith(req[:2]):
        print(f"Invalid response: {resp}")
    elif resp[3] & 0x80 == 0:
        print("SPC finished")
        break
    else:
        print("SPC in progress...")

    time.sleep(10)
