SaaS CO
===============
This wraps some aws datawrangler code

Installing
============

.. code-block:: bash

    pip install saas-co

Usage
=====

.. code-block:: bash

    >>> from src.cur import athena, assume_role
    >>> session = assume_role(accountId = '123456789', 
                      roleName = 'power-user', 
                      region = 'us-east-1',
                      sessionName = 'test')
    >>> athena(session, 'cur_db', 'select * from cur_db.data limit 10')
    '...'
