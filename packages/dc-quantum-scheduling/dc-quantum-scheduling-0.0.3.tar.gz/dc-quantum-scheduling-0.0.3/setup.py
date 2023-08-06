# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dc_quantum_scheduling', 'dc_quantum_scheduling.qiskit']

package_data = \
{'': ['*']}

install_requires = \
['pytz', 'qiskit', 'requests', 'retry']

setup_kwargs = {
    'name': 'dc-quantum-scheduling',
    'version': '0.0.3',
    'description': '',
    'long_description': "# Scheduling software for qiskit -- Client\n\n## Attention: this is a work-in-progess implementation. \nWhat this means: it basically works. But: \n\n 1. edge cases are not covered \n 2. even broad cases aren't entirely covered!! \n 3. in code documentation is not there\n 4. no usage or API documentation exists\n 5. CI/CD is not setup\n\n__So__: use at your own risk. \n\n# Contributing\nWe welcome contributions - simply fork the repository of this plugin, and then make a pull request containing your contribution. All contributers to this plugin will be listed as authors on the releases.\n\nWe also encourage bug reports, suggestions for new features and enhancements!\n\n# Authors\nCarsten Blank\n\n# Support\n\nSource Code: https://github.com/carstenblank/dc-quantum-scheduling\n\nIssue Tracker: https://github.com/carstenblank/dc-quantum-scheduling/issues\n\nIf you are having issues, please let us know by posting the issue on our Github issue tracker.\n\n# License\nThe dc-quantum-scheduling is free and open source, released under the Apache License, Version 2.0.",
    'author': 'Carsten BLank',
    'author_email': 'blank@data-cybernetics.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/carstenblank/dc-quantum-scheduling',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
