
|License badge|

======================
Horizon Heat Extension
======================

This is a simple Horizon extension for support loading local Heat templates.

Installation notes
------------

* add 'heat_extension' to INSTALLED_APPS tuple
* set HEAT_LOCAL to True, and now will be searched in default path /srv/heat/env``


Custom Heat templates dir

.. code-block:: python

	HEAT_LOCAL = True
    HEAT_ROOT='/srv/heat/env'

Read more
-----

* http://docs.openstack.org/developer/horizon/topics/tutorial.html

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat