# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lois']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lois',
    'version': '0.0.1',
    'description': 'The fastest and  user friendly way to EDA',
    'long_description': '# lois\npython package to generate data science report\n\n#### Purpose of the package\n+  The purpose of this package is to provide to data scientist and data analyst a faster way to analyze their data by automating the EDA\n\n\n#### Features\n+  EDA automation\n\n\n### Getting Started\nThe package can be found on pypi hence you can install it using pip\n\n#### Installation\n\n```bash\npip install lois\n```\n### Usage\n```python|jupyter notebook\n\n>>> import pandas as pd\n>>> from lois import lois_ds_report\n>>> data=pd.read_csv("your data path")\n>>> lois_ds_report(data,target_variable="sex", report_complexity="simple" )\n```\n\n\n### Contribution\nContribution are welcome.\nNotice a bug ? let us know. Thanks you\n\n### Author\n+ Main Maitainer : Charles TCHANAKE\n+ email : datadevfernolf@gmail.com ',
    'author': 'Charles TCHANAKE',
    'author_email': 'datadevfernolf@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/charleslf2/lois.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
