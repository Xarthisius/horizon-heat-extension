======================
Horizon Heat Extension
======================

Horizon extension for loading local Heat templates directly from horizon server.

Use case
-----------

"Heat is cool piece of software, but form for creating Stack back us to the jungle. Please tell me why i would like upload heat template from my local PC?"

This plugin provides following features:

* loads templates and environments from Horizon server local filesystem

Installation notes
------------

* add `heat_extension` to INSTALLED_APPS tuple
* add `heat_extension.overrides` to `customization_module` in HORIZON_CONFIG or include it from other `customization_module`
* the default path for templates is `/srv/heat/env`, but can be set by `HEAT_ROOT` variable

Example settings variables with forCustom Heat templates dir

.. code-block:: python

    HEAT_ROOT = '/srv/heat/env'

* create or clone templates in default directory /srv/heat/env or set `HEAT_ROOT` variable to point to custom directory
* the name of the launched stack is <template_name>_<env_name>

Template structure
---------

This extensions requires that templates are saved in `template` directory and corresponding 
environments in `environment/<template_name>` directories.

Sample template structure with 1 template and 3 possible environments, please note the extensions as they need to match as well.

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
