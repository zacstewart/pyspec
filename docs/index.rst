PySpec
==================================

PySpec is a behavior-driven development library in the spirit of RSpec. It enables you
to test your code by specifying expected outcomes in prose-like language:

.. code-block:: python

    mug = Mug()
    with description(Mug):
        with description('.fill')
            with context('coffee'):
                with specification('fills the mug with coffee'):
                    mug.fill('coffee')
                    expect(mug.contents).to(eq('coffee'))

Contents
--------

.. toctree::
   :maxdepth: 2

   expectations


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

