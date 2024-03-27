# Equivalence Class Partitioning (ECP):
# Gültige Eingaben:
# CNP-Nummern mit gültigen Strukturen und Werten.
# CNP-Nummern mit unterschiedlichen Gültigkeitsprüfungen.
#
# Ungültige Eingaben:
# CNP-Nummern mit ungültigen Strukturen (falsche Länge, ungültige Zeichen usw.).
# CNP-Nummern mit ungültigen Werten (falsche Prüfsumme, ungültige Geburtsdaten usw.).
#
# Boundary Value Analysis (BVA):
# Gültige Grenzwerte:
# Die kleinste gültige CNP-Nummer.
# Die größte gültige CNP-Nummer.
#
# Ungültige Grenzwerte:
# CNP-Nummern, die eine Stelle unter oder über dem kleinsten
# bzw. größten gültigen CNP liegen.

import unittest

from testCNP import check_cnp_is_valid_unvec


class TestCheckCNPValidity(unittest.TestCase):
    # Equivalence Class Partitioning (ECP) Tests
    def test_valid_cnp(self):
        self.assertTrue(check_cnp_is_valid_unvec(6020528324792))

    def test_invalid_cnp_invalid_structure(self):
        self.assertFalse(check_cnp_is_valid_unvec(12345678901))

    def test_invalid_cnp_invalid_values(self):
        self.assertFalse(check_cnp_is_valid_unvec(1234567890124))

    # Boundary Value Analysis (BVA) Tests
    def test_valid_minimum_cnp(self):
        self.assertTrue(check_cnp_is_valid_unvec(1000000000000))

    def test_valid_maximum_cnp(self):
        self.assertTrue(check_cnp_is_valid_unvec(9999999999999))

    def test_invalid_below_minimum_cnp(self):
        self.assertFalse(check_cnp_is_valid_unvec(999999999999))

    def test_invalid_above_maximum_cnp(self):
        self.assertFalse(check_cnp_is_valid_unvec(10000000000000))

if __name__ == '__main__':
    unittest.main()
