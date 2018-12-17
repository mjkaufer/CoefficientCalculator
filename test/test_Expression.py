import unittest
import CoefficientCalculator
from CoefficientCalculator import CoefficientCalculator
from CoefficientCalculator.CoefficientCalculator import Term, MultiTerm, Expression, Scalar

class TestExpression(unittest.TestCase):

    # (1 + 3x + x^2) * x => x + 3x^2 + x^3
    def test_multiply_by_multiterm(self):
        singleMultiTerm = MultiTerm([Term("x")], 1)

        multiTerm1 = Scalar()
        multiTerm2 = MultiTerm(Term("x"), 3)
        multiTerm3 = MultiTerm(Term("x", 2))

        expression = Expression([multiTerm1, multiTerm2, multiTerm3])

        expressionProduct = expression * singleMultiTerm

        self.assertEqual(len(expressionProduct.multiTerms), 3)

        xMultiTerm = expressionProduct.multiTerms[(MultiTerm(Term("x")))]
        xSquaredMultiTerm = expressionProduct.multiTerms[(MultiTerm(Term("x", 2)))]
        xCubedMultiTerm = expressionProduct.multiTerms[(MultiTerm(Term("x", 3)))]

        self.assertEqual(xMultiTerm.constant, 1)
        self.assertEqual(xSquaredMultiTerm.constant, 3)
        self.assertEqual(xCubedMultiTerm.constant, 1)

    # (x-1) * (x+1) => x^2 - 1
    def test_multiply_by_two_expressions(self):

        expression1 = Expression([MultiTerm(Term("x")), Scalar()])
        expression2 = Expression([MultiTerm(Term("x")), Scalar(-1)])

        expressionProduct = expression1 * expression2

        self.assertEqual(len(expressionProduct.multiTerms), 2)

        xSquaredMultiTerm = expressionProduct.multiTerms[(MultiTerm(Term("x^2")))]
        scalarMultiTerm = expressionProduct.multiTerms[Scalar()]
        
        self.assertEqual(xSquaredMultiTerm.constant, 1)
        self.assertEqual(scalarMultiTerm.constant, -1)

    # test getCoefficient
    def test_get_coefficient(self):

        expression1 = Expression([MultiTerm(Term("x")), Scalar()])
        expression2 = Expression([MultiTerm(Term("x")), Scalar(-1)])

        expressionProduct = expression1 * expression2

        self.assertEqual(len(expressionProduct.multiTerms), 2)

        self.assertEqual(expressionProduct.getCoefficient(MultiTerm(Term("x^2"))), 1)
        self.assertEqual(expressionProduct.getCoefficient(MultiTerm(Term("x"))), 0)
        self.assertEqual(expressionProduct.getCoefficient(Scalar()), -1)
        

if __name__ == '__main__':
    unittest.main()