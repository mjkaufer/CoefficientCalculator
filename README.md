# CoefficientCalculator
This is a tool to compute the coefficients of the products of multinomial expressions!

## Usage
This code runs on python3 – maybe it runs on python2 but I haven't tested

There are three types of classes; `Term`, `MultiTerm`, and `Expression`. 

* `Term` represents something like `x` or `y^5`; it's a symbol raised to an exponent
* `MultiTerm` represents a product of `Term` objects, multiplied by a scalar such as `23 * x * y^5`
    * You can represent a pure scalar with `MultiTerm`; the `Scalar` class is a synonym for an 'empty' `MultiTerm` object
* `Expression` is a sum of `MultiTerm` objects
    * The equation `1 + 3x + 2*x*y` looks like this
    * `Expression([Scalar(1), MultiTerm(Term("x"), 3), MultiTerm([Term("x"), Term("y")], 2)])`

You can compute the product of expressions and then find their coefficients via `Expression.getCoefficient(MultiTerm)`. This is very useful in combinatorics problems

You can find some example usage [here](https://gist.github.com/mjkaufer/75665a52499f09fe8aae900124caa8ad)

## Testing
Just run `python -m unittest test/*` in the main directory