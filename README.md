# PySpec

Express expected outcomes with examples.

```python
mug = Mug()
with description(Mug):
    with description('.fill')
        with context('coffee'):
            with specification('fills the mugg with coffee'):
                mug.fill('coffee')
                expect(mug.contents).to(eq('coffee'))
```

## Try it out

    python example_spec.py
    F.F.

    2 failures
    pyspec <class '__main__.BrokenFizzBuzz'> .convert 15 returns fizzbuzz
    Expected fizz to be equal to fizzbuzz
    pyspec <class '__main__.BrokenFizzBuzz'> .convert 5 returns buzz
    Expected 5 to be equal to buzz
