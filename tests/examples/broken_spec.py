from pyspec import description, specification
from pyspec.expectations import expect, eq

with description(object):
    subject = object()
    with description('.foobar'):
        with specification('is not a thing'):
            expect(subject.foobar).to(eq(None))
