from .util import toIdentityDict

class Constant:
    def __init__(self, value=1):
        self.value = value

# Can represent something like x^5
class Term:
    def __init__(self, symbol, exponent=1):
        if exponent < 1:
            raise ValueError("The exponent of a term must be greater than 0!")

        self.symbol = symbol
        self.exponent = exponent

    def __str__(self):
        if self.exponent == 1:
            return str(self.symbol)

        return str(self.symbol) + "^" + str(self.exponent)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.symbol)

    # So technically two terms x^2 and x^3 are "equal", but this is mostly for finding like terms
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        if str(self.symbol) == str(other.symbol):
            return self.exponent < other.exponent

        return str(self.symbol) < str(other.symbol)

    def clone(self):
        return Term(self.symbol, self.exponent)

# Can represent something like 3x or 10xy, 11 * x^2 * y^44, etc.
class MultiTerm:
    def __init__(self, termArray=[], constant=1):
        self.constant = constant

        if isinstance(termArray, dict):
            self.terms = termArray
        else:
            if not isinstance(termArray, list) and not isinstance(termArray, set):
                termArray = [termArray]
            self.terms = toIdentityDict(termArray)

        if len(termArray) != len(self.terms):
            raise ValueError("Constructed term array with redundant terms")
        
        self.__hashString = str(sorted(self.terms))

    def cloneTerms(self):
        return {clonedTerm: clonedTerm for clonedTerm in {term.clone() for term in self.terms}}

    def __hash__(self):
        return hash(self.__hashString)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        output = str(self.constant)
        for term in self.terms:
            output += "*" + str(term)
        return output

    def __repr__(self):
        return self.__str__()

    def __mul__(self, other):
        newConstant = self.constant * other.constant

        # theoretically we don't care if we mutate the original input if all we care
        # about is the end product, but I think it's for the best
        newTerms = self.cloneTerms()

        for otherTerm in other.cloneTerms():
            if otherTerm in newTerms:
                existingTerm = newTerms[otherTerm]
                existingTerm.exponent += otherTerm.exponent
            else:
                newTerms[otherTerm] = otherTerm

        return MultiTerm(newTerms, newConstant)

    def __add__(self, other):
        if str(self.__hashString) != str(other.__hashString):
            raise ValueError("Can't add non-like terms!")
        else:
            return MultiTerm(self.terms, self.constant + other.constant)

def Scalar(num=1):
    return MultiTerm([], num)

# Can represent something like 1 + x + y + 2xy + x^2 + y^2
class Expression:
    def __init__(self, multiTermArray=[]):
        if isinstance(multiTermArray, dict):
            self.multiTerms = multiTermArray
        else:    
            self.multiTerms = toIdentityDict(multiTermArray)

    def multBySingleMultiTerm(self, singleMultiTerm):
        newMultiTerms = {}

        for multiTerm in self.multiTerms.values():
            multiTermProduct = singleMultiTerm * multiTerm
            if multiTermProduct.constant != 0:
                newMultiTerms[multiTermProduct] = multiTermProduct

        return Expression(newMultiTerms)

    def __mul__(self, other):
        if isinstance(other, MultiTerm):
            return self.multBySingleMultiTerm(other)

        result = Expression()

        for multiTerm in other.multiTerms:
            subExpression = self * multiTerm
            result = result + subExpression

        return result

    def __add__(self, other):
        newMultiTerms = {}

        for multiTerm in list(self.multiTerms.keys()) + list(other.multiTerms.keys()):
            if multiTerm in newMultiTerms:
                existingMultiTerm = newMultiTerms[multiTerm]
                existingMultiTerm.constant += multiTerm.constant
            else:
                newMultiTerms[multiTerm] = multiTerm

            if newMultiTerms[multiTerm].constant == 0:
                del newMultiTerms[multiTerm]

        return Expression(newMultiTerms.values())

    def __str__(self):
        return "(" + " + ".join([str(multiTerm) for multiTerm in self.multiTerms.values()]) + ")"

    def __repr__(self):
        return self.__str__()

    def getCoefficient(self, multiTerm):
        if multiTerm not in self.multiTerms:
            return 0
        else:
            return self.multiTerms[multiTerm].constant