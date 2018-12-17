import unittest
import CoefficientCalculator
from CoefficientCalculator import CoefficientCalculator
from CoefficientCalculator.CoefficientCalculator import Term

class TestTerm(unittest.TestCase):
    
    def test_creation_with_default_exponent(self):
        term = Term("default")
        self.assertEqual(term.exponent, 1)

    def test_creation_with_manual_exponent(self):
        term = Term("hello", 5)
        self.assertEqual(term.exponent, 5)

    def test_hash(self):
        term1 = Term("abc")
        self.assertEqual(hash(term1), hash("abc"))

        term2 = Term("abc", 100)
        self.assertEqual(hash(term1), hash(term2))

    def test_no_exponents_less_than_one(self):
        with self.assertRaises(ValueError):
            Term("abc", 0)
            
        with self.assertRaises(ValueError):
            Term("abc", -1)

if __name__ == '__main__':
    unittest.main()