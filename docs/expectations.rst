============
Expectations
============

Expectations are a way to defined expected outcomes using examples. They may be
used outside of PySpec by importing ``pyspec.expections``.

The basic usage pattern of PySpec Expectations is::

    expect(actual).to(matcher(expected))
    expect(actual).not_to(matcher(expected))

What are matchers?
==================

Matchers are objects that have the following methods:

- .. function:: match(expected, actual)
- .. function:: failure_message
- .. function:: failure_message_when_negated

Built-in matchers
=================

PySpec Expectations comes with several matchers for testing common outcomes.

Object equivalence
------------------

Passes if ``actual == expected``::

    expect(actual).to(eq(expected))

Object identity
------------------

Passes if ``actual is expected``::

    expect(actual).to(be(expected))

Comparison
----------

Passes if ``actual > expected``::

    expected(actual).to(be_gt(expected))

Passes if ``actual < expected``::

    expect(actual).to(be_lt(expected))

Passes if ``actual >= expected``::

    expect(actual).to(be_gte(expected))

Passes if ``actual <= expected``::

    expect(actual).to(be_lte(expected))

Passes if ``(actual <= expected + delta) and (actual >= expected - delta)``::

    expect(actual).to(be_within(delta).of(expected))

Passes if ``re.match(pattern, actual) is not None``::

    expect(actual).to(match(pattern))

API
===

.. automodule:: pyspec.expectations
    :members:
