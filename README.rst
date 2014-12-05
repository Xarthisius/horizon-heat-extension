
|License badge|

======================
Horizon Heat Extension
======================

This is a simple Horizon extension for support loading local Heat templates.

Use case
-----------

Heat is cool piece of software, but form for creating Stack back us to the jungle. Please tell me why i would like upload heat template from my local PC ?

This plugin provides simple straightforward features:

* load templates and environments from local FS (where we run the Horizon)
* new panels for managing templates and environments


Installation notes
------------

* add `heat_extension` to INSTALLED_APPS tuple
* add `heat_extension.overrides` to `customization_module` in HORIZON_CONFIG.
* set `HEAT_LOCAL` to True, and now will be searched in default path `/srv/heat/env`

*note: extension expect two directories template and env*

Custom Heat templates dir


.. code-block:: python

    HEAT_LOCAL = True
    HEAT_ROOT = '/srv/heat/env'


Enable using own templates via url, raw or file inputs

.. code-block:: python

    HEAT_ONLY_LOCAL = False


Workflow
----------

* create your template into default dir or set another `HEAT_ROOT` path or git clone your template into /srv/heat/env
* thats all !


Structure of directories
---------

.. code-block:: bash

    $HEAT_ROOT/template/contrail_service_chaing.hot
    $HEAT_ROOT/env/contrail_service_chaing/default.env


Read more
-----

* http://docs.openstack.org/developer/horizon/topics/tutorial.html

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat