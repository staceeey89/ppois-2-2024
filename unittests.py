import unittest
from EncryptionDevice import EncryptionDevice
from Algorythm import Algorythm
from KeyClass import Key
from Data import Data
from unittest.mock import patch
from io import StringIO


class EncryptionDeviceTest(unittest.TestCase):
    def test_data_storing(self):
        device = EncryptionDevice(Algorythm("Caesar", Key(3)))
        expected_output: str = "Original Data:  abcdef\n"
        device.set_data(Data("abcdef"))
        with patch('sys.stdout', new=StringIO()) as fake_out:
            device.show_original_data()
            actual_output: str = fake_out.getvalue()
        self.assertEqual(expected_output, actual_output)

    def test_data_no_storing(self):
        device = EncryptionDevice(Algorythm("Caesar", Key(3)))
        expected_output: str = "There is no data\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            device.show_original_data()
            actual_output: str = fake_out.getvalue()
        self.assertEqual(expected_output, actual_output)

    def test_encrypting(self):
        device = EncryptionDevice(Algorythm("Caesar", Key(3)))
        expected_output: str = ("data encrypted\n")
        device.set_data(Data("abc"))
        with patch('sys.stdout', new=StringIO()) as fake_out:
            device.encrypt_data()
            actual_output: str = fake_out.getvalue()
        self.assertEqual(actual_output, expected_output)

    def test_encrypting_no_data(self):
        device = EncryptionDevice(Algorythm("Caesar", Key(3)))
        expected_output: str = "There is no data for encrypting\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            device.encrypt_data()
            actual_output: str = fake_out.getvalue()
        self.assertEqual(actual_output, expected_output)

    def test_data_deciphering(self):
        device = EncryptionDevice(Algorythm("Caesar", Key(3)))
        device.set_data(Data("abc"))
        expected_output: str = ("Deciphered Data:  abc\n")
        device.encrypt_data()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            device.decipher_data()
            actual_output: str = fake_out.getvalue()
        self.assertEqual(expected_output, actual_output)

    def test_security_correct(self):
        device = EncryptionDevice(Algorythm("Caesar", Key(3)))
        with patch('builtins.input', return_value="12qw"):
            result = device.security()
        self.assertTrue(result)

    def test_security_incorrect(self):
        device = EncryptionDevice(Algorythm("Caesar", Key(3)))
        with patch('builtins.input', return_value="purr purr purr"):
            result = device.security()
        self.assertFalse(result)

    def test_analyze_algorithm(self):
        expected_output: str = "Code was broken in  23 iterations\n"
        device = EncryptionDevice(Algorythm("Caesar", Key(3)))
        device.set_data(Data("abc"))
        device.encrypt_data()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            device.analyze_algorythm()
            actual_output: str = fake_out.getvalue()
        self.assertEqual(expected_output, actual_output)

    def test_analyze_algorithm_no_data(self):
        expected_output: str = "lack of data \n"
        device = EncryptionDevice(Algorythm("Caesar", Key(3)))
        with patch('sys.stdout', new=StringIO()) as fake_out:
            device.analyze_algorythm()
            actual_output: str = fake_out.getvalue()
        self.assertEqual(expected_output, actual_output)


class AlgorithmTests(unittest.TestCase):
    def test_caesar_encryption(self):
        algo = Algorythm("Caesar", Key(3))
        expected_value: str = "def"
        actual_value: str = algo.caesar_encryption("abc", bool(0))
        self.assertEqual(expected_value, actual_value)


    def test_caesar_analyze(self):
        algo = Algorythm("Caesar", Key(3))
        expected_value: int = 23
        actual_value: int = algo.caesar_analyze("def", "abc")
        self.assertEqual(expected_value, actual_value)


if __name__ == '__main__':
    unittest.main()
