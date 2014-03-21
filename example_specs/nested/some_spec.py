from pyspec.expectations import expect, be
from pyspec import description, specification

with description("Identity"):
    with specification("is the same object"):
        expect(None).to(be(None))
