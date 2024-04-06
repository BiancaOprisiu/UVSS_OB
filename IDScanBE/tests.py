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
import pytest
import coverage
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
    def test_invalid_below_minimum_cnp(self):
        self.assertFalse(check_cnp_is_valid_unvec(999999999999))

    def test_invalid_above_maximum_cnp(self):
        self.assertFalse(check_cnp_is_valid_unvec(10000000000000))


    #Lab 3

    def test_None(self):
        self.assertIsNone(check_cnp_is_valid_unvec(None))

    def test_NotInt(self):
        invalid_CNP = "abc"
        self.assertFalse(check_cnp_is_valid_unvec(invalid_CNP))

    def test_invalid_CNP_with_wrong_length(self):
        invalid_CNP = 123
        self.assertFalse(check_cnp_is_valid_unvec(invalid_CNP))

    def test_S(self):
        invalid_CNP = 9234567890412
        self.assertFalse(check_cnp_is_valid_unvec(invalid_CNP))

    def test_LL(self):
        invalid_CNP = 6934567859012
        self.assertFalse(check_cnp_is_valid_unvec(invalid_CNP))

    def test_ZZ(self):
        invalid_CNP = 6020567896012
        self.assertFalse(check_cnp_is_valid_unvec(invalid_CNP))

    def test_checksum(self):
        invalid_CNP = 6020528879012
        self.assertFalse(check_cnp_is_valid_unvec(invalid_CNP))

    def test_valid_CNP(self):
        valid_CNPs = [6020528324792]
        for cnp in valid_CNPs:
            self.assertTrue(check_cnp_is_valid_unvec(cnp))


if __name__ == '__main__':
    unittest.main()
