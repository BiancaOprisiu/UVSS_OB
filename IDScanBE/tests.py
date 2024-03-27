# # Equivalence Class Partitioning (ECP):
# # Gültige Eingaben:
# # Bilder mit einem oder mehreren Gesichtern.
# # Bilder mit gut lesbaren Texten.
# # Bilder mit unterschiedlichen Lichtverhältnissen.
#
# # Ungültige Eingaben:
# # Bilder ohne Gesichter.
# # Bilder ohne lesbaren Text.
# # Beschädigte oder stark verzerrte Bilder.
#
# # Boundary Value Analysis (BVA):
# # Gültige Grenzwerte:
# # Ein Bild mit einem Gesicht.
# # Ein Bild mit minimal lesbarem Text.
#
# # Ungültige Grenzwerte:
# # Ein Bild ohne Gesichter.
# # Ein leeres Bild.
# # Ein Bild mit extrem unlesbarem Text.
#
# # Testfälle:
# # Gültige Eingabe - Ein Bild mit einem Gesicht und lesbarem Text.
# # Gültige Eingabe - Ein Bild mit mehreren Gesichtern und lesbarem Text.
# # Ungültige Eingabe - Ein Bild ohne Gesichter.
# # Ungültige Eingabe - Ein leeres Bild.
#
# import unittest
# from FaceRecognition import getInfoFromCI
#
#
# class TestGetInfoFromCI(unittest.TestCase):
#
#     def test_valid_input_with_face_and_text(self):
#         # Mock a sample image with a face and readable text
#         sample_image = "MockImg.jpeg"
#         personal_info = getInfoFromCI(sample_image)
#
#         # Assert that personal_info is not empty
#         self.assertNotEqual(personal_info, {})
#
#     # def test_valid_input_without_face(self):
#     #     # Mock a sample image without a face
#     #     sample_image = "sample_image_without_face.jpg"
#     #     personal_info = getInfoFromCI(sample_image)
#     #
#     #     # Assert that personal_info is empty
#     #     self.assertEqual(personal_info, {})
#
#     def test_invalid_input_with_empty_image(self):
#         # Mock an empty image
#         empty_image = "empty_image.jpg"
#
#         # Assert that getInfoFromCI raises an exception
#         with self.assertRaises(Exception):
#             getInfoFromCI(empty_image)
#
#
#
# if __name__ == '__main__':
#     unittest.main()

import unittest

from testCNP import check_cnp_is_valid_unvec


class TestCheckCNPValidity(unittest.TestCase):
    # Equivalence Class Partitioning (ECP) Tests
    def test_valid_cnp(self):
        self.assertTrue(check_cnp_is_valid_unvec(6020528324792))

    def test_invalid_cnp_invalid_structure(self):
        self.assertFalse(check_cnp_is_valid_unvec(12345678901))  # Invalid length

    def test_invalid_cnp_invalid_values(self):
        self.assertFalse(check_cnp_is_valid_unvec(1234567890124))  # Invalid checksum

    # Boundary Value Analysis (BVA) Tests
    def test_valid_minimum_cnp(self):
        self.assertTrue(check_cnp_is_valid_unvec(1000000000000))

    def test_valid_maximum_cnp(self):
        self.assertTrue(check_cnp_is_valid_unvec(9991231231239))

    def test_invalid_below_minimum_cnp(self):
        self.assertFalse(check_cnp_is_valid_unvec(999999999999))

    def test_invalid_above_maximum_cnp(self):
        self.assertFalse(check_cnp_is_valid_unvec(10000000000000))

if __name__ == '__main__':
    unittest.main()
