from src.project_on_image import convert_to_spherical_coordinates
import numpy as np
import unittest
from math import pi, sqrt, atan


class TestConvertToSphericalCoordinates(unittest.TestCase):
    def test_convert_to_spherical_coordinates(self):
        self.assertListEqual(convert_to_spherical_coordinates(np.array([1, 0, 0])).tolist(), [1, 0, 0])
        self.assertListEqual(convert_to_spherical_coordinates(np.array([1, 1, 0])).tolist(), [sqrt(2), 0, pi / 4])
        self.assertListEqual(convert_to_spherical_coordinates(np.array([1, 0, 1])).tolist(), [sqrt(2), pi / 4, 0])
        self.assertListEqual(convert_to_spherical_coordinates(np.array([-1, -1, -1])).tolist(),
                             [sqrt(3), -atan(1 / sqrt(2)), -3 * pi / 4])
