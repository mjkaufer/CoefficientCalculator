import unittest
import CoefficientCalculator
from CoefficientCalculator import CoefficientCalculator
from CoefficientCalculator.CoefficientCalculator import Term, MultiTerm

class TestMultiTerm(unittest.TestCase):
    
    def test_creation_failure_with_redundant_terms(self):
        term1 = Term("default")
        term2 = Term("default")

        with self.assertRaises(ValueError):
            MultiTerm([term1, term2])

    def test_default_constant(self):
        term1 = Term("default")
        multiTerm = MultiTerm(term1)
        self.assertEqual(multiTerm.constant, 1)

    def test_normal_multiterm(self):
        term1 = Term("bar")
        term2 = Term("foo", 3)

        multiTerm = MultiTerm([term1, term2], 2)

        self.assertEqual(len(multiTerm.terms), 2)
        self.assertEqual(term1 in multiTerm.terms, True)
        self.assertEqual(term2 in multiTerm.terms, True)

    def test_multiterm_addition(self):
        term1 = Term("x")
        term2 = Term("y", 3)


        term3 = Term("x", 2)
        term4 = Term("y")
        
        multiTerm1 = MultiTerm([term1, term2], 6)
        multiTerm2 = MultiTerm([term1, term2], 75)

        with self.assertRaises(ValueError):
            multiTerm3 = MultiTerm([term3, term4], 2)
            multiTerm3 + multiTerm1

        multiSum = multiTerm1 + multiTerm2

        # make sure we don't mutate any exponents while creating or adding
        self.assertEqual(term1.exponent, 1)
        self.assertEqual(term2.exponent, 3)

        # make sure none of the contents change
        for multiTerm in [multiTerm1, multiTerm2, multiSum]:
            self.assertEqual(len(multiTerm.terms), 2)
            self.assertEqual(term1 in multiTerm.terms, True)
            self.assertEqual(term2 in multiTerm.terms, True)

        self.assertEqual(multiTerm1.constant, 6)
        self.assertEqual(multiTerm2.constant, 75)
        self.assertEqual(multiSum.constant, multiTerm1.constant + multiTerm2.constant)

    def test_product_of_identities(self):
        i1 = MultiTerm([])
        i2 = MultiTerm([])

        identityProduct = i1 * i2
        self.assertEqual(len(identityProduct.terms), 0)
        self.assertEqual(identityProduct.constant, 1)

    def test_multiterm_identity_multiplication(self):
        term1 = Term("x")
        term2 = Term("y", 3)
        term3 = Term("z", 4)

        i = MultiTerm([])
        multiTerm = MultiTerm([term1, term2, term3], 4)

        identityProduct = i * multiTerm

        self.assertEqual(term1.exponent, 1)
        self.assertEqual(term2.exponent, 3)
        self.assertEqual(term3.exponent, 4)

        for someMultiTerm in [multiTerm, identityProduct]:
            self.assertEqual(len(someMultiTerm.terms), 3)
            self.assertEqual(someMultiTerm.constant, 4)
            self.assertEqual((someMultiTerm.terms[Term("x")]).exponent, 1)
            self.assertEqual((someMultiTerm.terms[Term("y")]).exponent, 3)
            self.assertEqual((someMultiTerm.terms[Term("z")]).exponent, 4)

    def test_multiterm_multiplication(self):
        term1 = Term("x")
        term2 = Term("y", 3)
        term3 = Term("z", 4)

        term4 = Term("w")
        term5 = Term("x", 2)
        term6 = Term("z", 3)
        
        multiTerm1 = MultiTerm([term1, term2, term3], 6)
        multiTerm2 = MultiTerm([term4, term5, term6], 75)
        multiProduct = multiTerm1 * multiTerm2

        # make sure we don't mutate any exponents while creating or adding
        self.assertEqual(term1.exponent, 1)
        self.assertEqual(term2.exponent, 3)
        self.assertEqual(term3.exponent, 4)
        self.assertEqual(term4.exponent, 1)
        self.assertEqual(term5.exponent, 2)
        self.assertEqual(term6.exponent, 3)

        for term in [term1, term2, term3]:
            self.assertEqual(term in multiTerm1.terms, True)
        self.assertEqual(len(multiTerm1.terms), 3)
        self.assertEqual(multiTerm1.constant, 6)

        for term in [term4, term5, term6]:
            self.assertEqual(term in multiTerm2.terms, True)

        self.assertEqual(len(multiTerm2.terms), 3)
        self.assertEqual(multiTerm2.constant, 75)

        self.assertEqual(multiProduct.constant, multiTerm1.constant * multiTerm2.constant)
        self.assertEqual(len(multiProduct.terms), 4)

        self.assertEqual((multiProduct.terms[Term("w")]).exponent, 1)
        self.assertEqual((multiProduct.terms[Term("x")]).exponent, 3)
        self.assertEqual((multiProduct.terms[Term("y")]).exponent, 3)
        self.assertEqual((multiProduct.terms[Term("z")]).exponent, 7)


if __name__ == '__main__':
    unittest.main()