import crc
import struct

width = 16
poly = 0x8005
init_value = 0xFFFF
final_xor_value = 0x00
reverse_input = True
reverse_output = True

configuration = crc.Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)


def calc_crc(data: bytes) -> bytes:
    crc_calculator = crc.CrcCalculator(configuration, True)
    return struct.pack("<H", crc_calculator.calculate_checksum(data))
