# PySpec

[![Build Status](https://travis-ci.org/zacstewart/pyspec.png)](https://travis-ci.org/zacstewart/pyspec)

[Documentation](http://pyspec.readthedocs.org/)

Express expected outcomes with examples.

```python
mug = Mug()
with description(Mug):
    with description('.fill')
        with context('coffee'):
            with specification('fills the mug with coffee'):
                mug.fill('coffee')
                expect(mug.contents).to(eq('coffee'))
```

## Try it out

    git clone git@github.com:zacstewart/pyspec.git
    cd pyspec
    python setup.py install
    pyspec example_specs/
    F.F.E.F.

    3 failures, 1 errors

    pyspec.core <class 'pyspec.core.BrokenFizzBuzz'> .convert 15 returns fizzbuzz
    Expected fizz to be equal to fizzbuzz

    pyspec.core <class 'pyspec.core.BrokenFizzBuzz'> .convert 5 returns buzz
    Expected 5 to be equal to buzz

    pyspec.core normal assertions are treated as failures and not errors
    False wasn't True!

    pyspec.core <class 'pyspec.core.BrokenFizzBuzz'> .floop does not exist
    'BrokenFizzBuzz' object has no attribute 'floop'
