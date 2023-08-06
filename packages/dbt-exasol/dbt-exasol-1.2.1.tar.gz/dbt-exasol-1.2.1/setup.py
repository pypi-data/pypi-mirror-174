# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt',
 'dbt.adapters',
 'dbt.adapters.exasol',
 'dbt.include',
 'dbt.include.exasol',
 'tests',
 'tests.functional']

package_data = \
{'': ['*'],
 'dbt.include.exasol': ['macros/*',
                        'macros/materializations/*',
                        'macros/utils/*']}

install_requires = \
['dbt-core==1.2.1',
 'dbt-tests-adapter>=1.2.1,<2.0.0',
 'pyexasol>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'dbt-exasol',
    'version': '1.2.1',
    'description': 'Adapter to dbt-core for warehouse Exasol',
    'long_description': '<p align="center">\n  <a href="https://github.com/tglunde/dbt-exasol/actions/workflows/main.yml">\n    <img src="https://github.com/tglunde/dbt-exasol/actions/workflows/main.yml/badge.svg?event=push" alt="Unit Tests Badge"/>\n  </a>\n  <a href="https://github.com/tglunde/dbt-exasol/actions/workflows/integration.yml">\n    <img src="https://github.com/tglunde/dbt-exasol/actions/workflows/integration.yml/badge.svg?event=push" alt="Integration Tests Badge"/>\n  </a>\n</p>\n\n# dbt-exasol\n**[dbt](https://www.getdbt.com/)** enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications.\n\nPlease see the dbt documentation on **[Exasol setup](https://docs.getdbt.com/reference/warehouse-setups/exasol-setup)** for more information on how to start using the Exasol adapter.\n\n# Known isues\n## Timestamp compatibility\nCurrently we did not see any possible way to make Exasol accept the timestamp format ```1981-05-20T06:46:51``` with a \'T\' as separator between date and time part. To pass the adapter tests we had to change the timestamps in the seed files to have a <space> character instead of the \'T\' (```1981-05-20 06:46:51```).\n## Default case of identifiers\nBy default Exasol identifiers are upper case. In order to use e.g. seeds or column name aliases - you need to use upper case column names. Alternatively one could add column_quote feature in order to have all columns case sensitive.\nWe changed the seeds_base in [files.py](tests/functional/files.py) and [fixtures.py](tests/functional/fixtures.py) in order to reflect this and successfully run the adapter test cases.\nAlso, this issue leads to problems for the [base tests for docs generation](https://github.com/dbt-labs/dbt-core/blob/8145eed603266951ce35858f7eef3836012090bd/tests/adapter/dbt/tests/adapter/basic/test_docs_generate.py), since the expected model is being checked case sensitive and fails therefor for Exasol. This will be the last task in [Issue #24](https://github.com/tglunde/dbt-exasol/issues/24) regarding dbt release 1.2. We will suggest a case insensitive version of this standard test or implement for a following minor release of dbt-exasol.\n\n## Utilities shim package\nIn order to support packages like dbt-utils and dbt-audit-helper, we needed to create the [shim package exasol-utils](https://github.com/tglunde/exasol-utils). In this shim package we need to adapt to parts of the SQL functionality that is not compatible with Exasol - e.g. when \'final\' is being used which is a keyword in Exasol. Please visit [Adaopter dispatch documentation](https://docs.getdbt.com/guides/advanced/adapter-development/3-building-a-new-adapter#adapter-dispatch) of dbt-labs for more information. \n# Reporting bugs and contributing code\n- Please report bugs using the issues\n\n# Release\n## Release 1.2.0\n- support for invalidate_hard_deletes option in snapshots added by jups23\n- added persist_docs support by sti0\n- added additional configuration keys that can be included in profiles.yml by johannes-becker-otto\n- added cross-database macros introduced in 1.2 by sti0\n- added support for connection retries by sti0\n- added support for grants by sti0\n- added pytest functional adapter tests by tglunde\n- tox testing for python 3.7.2 through 3.10 added by tglunde\n \n## Release 1.0.0\n- pyexasol HTTP import csv feature implemented. Optimal performance and compatibility with Exasol CSV parsing\n',
    'author': 'Torsten Glunde',
    'author_email': 'torsten.glunde@alligator-company.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://alligatorcompany.gitlab.io/dbt-exasol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
