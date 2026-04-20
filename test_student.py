import unittest
from proj1 import *
#proj1.py should contain your data class and function definitions
#these do not contribute positivly to your grade.
#but your grade will be lowered if they are missing
class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        self.rect = GlobeRect(lo_lat=10.0, hi_lat=20.0, west_long=30.0, east_long=40.0)
        self.region = Region(rect=self.rect, name="Broland", terrain="other")
        self.rc = RegionCondition(region=self.region, year=2025, pop=1000, ghg_rate=5000.0)

    def test_emissions_per_capita(self):
        self.assertAlmostEqual(emissions_per_capita(self.rc), 5.0)

    def test_area_returns_float(self):
        self.assertIsInstance(area(self.rect), float)

    def test_emissions_per_square_km(self):
        result = emissions_per_square_km(self.rc)
        self.assertIsInstance(result, float)

    def test_densest_single(self):
        self.assertEqual(densest([self.rc]), "Broland")

    def test_project_condition_year(self):
        projected = project_condition(self.rc, 5)
        self.assertEqual(projected.year, 2030)

    def test_project_condition_type(self):
        projected = project_condition(self.rc, 5)
        self.assertIsInstance(projected, RegionCondition)

if __name__ == '__main__':
    unittest.main()
