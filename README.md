# CoefficientCalculator
This is a tool to compute the coefficients of the products of multinomial expressions! The inspiration behind this is [here](http://blog.kaufer.org/combinatorics/2018/12/18/the-thanos-problem.html)

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

## TODO
* Optimize
    * If you only want to find the coefficient of a certain multiterm, you don't need to bother tracking multiterms with higher exponents
    * If you find a set of like terms in an expression, you can use the binomial theorem on them rather than multiply them one by one
        * This would need some abstraction around multiplying expressions together
* Make easier to use