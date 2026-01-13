import unittest
from src.utils.validators import validate_target, parse_ports

class TestValidators(unittest.TestCase):
    
    def test_validate_target_valid(self):
        self.assertTrue(validate_target("192.168.1.1"))
        self.assertTrue(validate_target("10.0.0.0/24"))
        
    def test_validate_target_invalid(self):
        self.assertFalse(validate_target("999.999.999.999"))
        self.assertFalse(validate_target("not_an_ip"))

    def test_parse_ports_single(self):
        self.assertEqual(parse_ports("80"), [80])

    def test_parse_ports_list(self):
        self.assertEqual(parse_ports("80, 443"), [80, 443])

    def test_parse_ports_range(self):
        self.assertEqual(parse_ports("20-22"), [20, 21, 22])

    def test_parse_ports_mixed(self):
        expected = [20, 21, 22, 80]
        self.assertEqual(parse_ports("20-22, 80"), expected)

    def test_parse_ports_invalid(self):
        self.assertEqual(parse_ports("invalid, 70000"), [])

if __name__ == '__main__':
    unittest.main()
