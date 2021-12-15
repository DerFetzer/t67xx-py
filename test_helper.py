from unittest import TestCase
import helper


class Test(TestCase):
    def test_calc_crc(self):
        data = bytes([0x15, 0x04, 0x13, 0x8B, 0x00, 0x01])
        exp_crc = bytes([0x46, 0x70])

        calc_crc = helper.calc_crc(data)

        self.assertEqual(exp_crc, calc_crc)
