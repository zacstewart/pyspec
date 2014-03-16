from pyspec import description, specification
from pyspec.expectations import expect, eq

with description(True):
    with specification('is false'):
        expect(True).to(eq(False))
