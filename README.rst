======================
Horizon Heat Extension
======================

Horizon extension for loading local Heat templates from horizon server.

Use case
-----------

"Heat is cool piece of software, but form for creating Stack back us to the jungle. Please tell me why i would like upload heat template from my local PC?"

This plugin provides following features:

* loads templates and environments from Horizon server local filesystem

Installation notes
------------

* add `heat_extension` to INSTALLED_APPS tuple
* add `heat_extension.overrides` to `customization_module` in HORIZON_CONFIG or include it from other `customization_module`.
* set `HEAT_LOCAL` settings variable to True, and now will be searched in default path `/srv/heat/env`

Custom Heat templates dir

.. code-block:: python

    HEAT_LOCAL = True
    HEAT_ROOT = '/srv/heat/env'

Enable using own templates via url, raw or file inputs

.. code-block:: python

    HEAT_LOCAL_ONLY = False


* create or clone templates in default directory /srv/heat/env or set `HEAT_ROOT` variable to point to  

Template structure
---------

This extensions requires that templates are saved in `template` directory and corresponding 
environments in `environment/<template_name>` directories.

Sample template structure of 1 template with 3 possible environments.

.. code-block:: bash

    $HEAT_ROOT/template/contrail_service_chaing.hot
    $HEAT_ROOT/env/contrail_service_chaing/project01.env
    $HEAT_ROOT/env/contrail_service_chaing/project02.env
    $HEAT_ROOT/env/contrail_service_chaing/lab01.env

Read more
-----

* http://docs.openstack.org/developer/horizon/topics/tutorial.html

|License badge|

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
