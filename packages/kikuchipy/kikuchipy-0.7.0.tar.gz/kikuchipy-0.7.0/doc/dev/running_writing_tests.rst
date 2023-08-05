Running and writing tests
=========================

All functionality in kikuchipy is tested via the `pytest <https://docs.pytest.org>`_
framework. The tests reside in a ``test`` directory within each module. Tests are short
methods that call functions in kikuchipy and compare resulting output values with known
answers. Install necessary dependencies to run the tests::

    pip install --editable .[tests]

Some useful `fixtures <https://docs.pytest.org/en/latest/explanation/fixtures.html>`_,
like a dummy scan and corresponding background pattern, are available in the
``conftest.py`` file.

.. note::

    Some :mod:`kikuchipy.data` module tests check that data not part of the package
    distribution can be downloaded from the `kikuchipy-data GitHub repository
    <https://github.com/pyxem/kikuchipy-data>`_, thus downloading some datasets of ~15
    MB to your local cache.

To run the tests::

    pytest --cov --pyargs kikuchipy

The ``--cov`` flag makes `coverage.py <https://coverage.readthedocs.io/en/latest/>`_
print a nice report in the terminal. For an even nicer presentation, you can use
``coverage.py`` directly::

    coverage html

Then, you can open the created ``htmlcov/index.html`` in the browser and inspect the
coverage in more detail.

To run only a specific test function or class, .e.g the ``TestEBSD`` class::

    pytest -k TestEBSD

This is useful when you only want to run a specific test and not the full test suite,
e.g. when you're creating or updating a test. But remember to run the full test suite
before pushing!

Docstring examples are tested `with pytest
<https://docs.pytest.org/en/stable/how-to/doctest.html>`_ as well. If you're in the top
directory you can run::

    pytest --doctest-modules --ignore-glob=kikuchipy/*/tests kikuchipy/*.py

Tips for writing tests of Numba decorated functions:

- A Numba decorated function ``numba_func()`` is only covered if it is called in the
  test as ``numba_func.py_func()``.
- Always test a Numba decorated function calling ``numba_func()`` directly, in addition
  to ``numba_func.py_func()``, because the machine code function might give different
  results on different OS with the same Python code. See `this issue
  <https://github.com/pyxem/kikuchipy/issues/496>`_ for a case where this happened.