# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jobsworthy',
 'jobsworthy.observer',
 'jobsworthy.observer.domain',
 'jobsworthy.observer.repo',
 'jobsworthy.performance',
 'jobsworthy.performance.repo',
 'jobsworthy.repo',
 'jobsworthy.structure',
 'jobsworthy.util']

package_data = \
{'': ['*']}

install_requires = \
['PyMonad>=2.4.0,<3.0.0',
 'azure-identity>=1.11.0,<2.0.0',
 'azure-storage-file-datalake>=12.9.1,<13.0.0',
 'delta-spark>=2.1.0,<3.0.0',
 'dependency-injector>=4.40.0,<5.0.0',
 'pino>=0.6.0,<0.7.0',
 'pyspark>=3.3.0,<4.0.0',
 'rdflib>=6.2.0,<7.0.0',
 'validators>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['infra = _infra.cli:infra_cli']}

setup_kwargs = {
    'name': 'jobsworthy',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Jobsworth\n\nA set of utility functions and classes to aid in build Spark jobs on Azure databricks.\n\n',
    'author': 'Col Perks',
    'author_email': 'wild.fauve@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wildfauve/jobsworth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
