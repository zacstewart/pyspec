from pyspec import description, specification
from pyspec.expectations import expect, eq

with description(True):
    with specification('is not false'):
        expect(True).not_to(eq(False))
