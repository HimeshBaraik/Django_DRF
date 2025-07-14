import unittest
from testing01 import Superhero


class TestSuperHero(unittest.TestCase):

    # def setUp(self):
    #     return super().setUp()

    def test_stringify(self):
        superhero = Superhero(name="Superman", strength_level=50)
        self.assertEqual(str(superhero), "Superman")
    
    def test_is_stronger_than(self):
        superhero1 = Superhero(name="Superman", strength_level=50)
        superhero2 = Superhero(name="Batman", strength_level=25)

        self.assertTrue(superhero1.is_stronger_than(superhero2))
        self.assertFalse(superhero2.is_stronger_than(superhero1))
