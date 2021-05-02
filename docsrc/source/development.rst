Development
-----------

Requirements
^^^^^^^^^^^^

.. code-block:: text

    python3 -m pip install pytest coverage pylint sphinx sphinx-autodoc-typehints furo


Install latest development version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Clone the GitHub repository:

   .. code-block:: text

        git clone git@github.com:snkas/discrevpy.git

2. Install locally using ``pip``:

   .. code-block:: text

        cd discrevpy
        python3 -m pip install .


Run tests
^^^^^^^^^

**All tests:**

.. code-block:: text

    python3 -m pytest

**Specific test showing stdout:**

.. code-block:: text

    python3 -m pytest -s -k test_name


Calculate coverage
^^^^^^^^^^^^^^^^^^

Outputs: ``.coverage``, ``coverage.xml`` and ``htmlcov/``

.. code-block:: text

    python3 -m coverage run --branch --omit="tests/*" -m pytest
    python3 -m coverage xml
    python3 -m coverage html


Pylint check
^^^^^^^^^^^^

.. code-block:: text

    python3 -m pylint discrevpy/*.py


Generate documentation
^^^^^^^^^^^^^^^^^^^^^^

Outputs HTML at ``docs/``

.. code-block:: text

    cd docsrc
    make html
