============================
Logging Utility to Database
============================


Utility to write logging to database in order to gather some application stats.


* Free software: MIT license

Features
--------

* Funciton can be extended to different database in future.
* A helper to log information to InfluxDB2 for further report purpose.
* The functions here catch the errors, if anything goes wrong it still return and won't break main program logic. But the information won't be recorded in InfluxDB.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

============================
Developer's Causion
============================

This package is hosted by pypi public. Do not include any sensitive information in this project.


============================
Usage
============================

Install
--------

Installation

::

    pip install coelog2db


Usage:

::

    import logging
    from log2db.log2db import Log2DB
    from log2db.log2influx import Log2Influx

    log2 = Log2DB.get_instance(Log2Influx,conf=conf["influxdb"],user="cronjob")
    log2.log(log_level=logging.INFO,message="Loading started") # log this message before acture logic starts

    try:
        # main code
        # make sure throw except in your code if you catched them in subprocess

        pass
    except Exception as ex:
            log2.log(logging.ERROR,message="download job failed. " + str(ex))


