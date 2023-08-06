# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['core', 'core.schema']

package_data = \
{'': ['*']}

install_requires = \
['pydantic[dotenv]>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'jax-geneweaver-core',
    'version': '0.0.1',
    'description': 'The core of the Jax-Geneweaver Python library',
    'long_description': "# Geneweaver Core\nThe Geneweaver Core Python library provides shared foundational functionality for the Geneweaver project. \nIt is a dependency of all other Geneweaver Python libraries, and is not intended to be used directly.\n\n## Installation\nThe Geneweaver Core library is available on PyPI and can be installed with pip:\n```bash\npip install geneweaver-core\n```\n\nIf you are using Poetry, you can add the Geneweaver Core library to your project with:\n```bash\npoetry add geneweaver-core\n```\n\n## Overview\nThis package is structured so as to share an import path with other `geneweaver` packages. This allows you to install\nthe package and import it without having to worry about the package name. For example, if you install the `geneweaver-core`\npackage, as well as the `geneweaver-db` package, you can import the `geneweaver` package and access both libraries:\n```python\nfrom geneweaver import core, db\n```\n\nThe Geneweaver Core library provides the following functionality:\n* `geneweaver.core.schema`: Pydantic schema definitions\n* `geneweaver.core.enum`: Enumerations\n\n\n* `geneweaver.core.config`: Configuration management\n  * `GeneweaverBaseSettings`: Base Settings class to inherit from for your own package's configuration classes\n  * `GeneweaverCoreSettings`: Configuration class for Geneweaver Core settings\n\n\n* `geneweaver.core.exc`: Geneweaver shared exceptions\n  * `GeneweaverException`: Base exception class for Geneweaver\n  * `GeneweaverError`: Base error class for Geneweaver\n  * `GeneweaverWarning`: Base warning class for Geneweaver\n\n#### Planned Functionality\n* `geneweaver.core.logging`: Shared logging management\n* `geneweaver.core.utils`: Shared utility functions\n\n\n## Acknowledgements\nThis project was developed by the Computational Systems and Synthetic Biology Center at the Jackson Laboratory in\nconjunction with the Baylor University Computational Biology and Bioinformatics Program.\n\n",
    'author': 'Jax & Baylor Computational Sciences',
    'author_email': 'cssc@jax.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
