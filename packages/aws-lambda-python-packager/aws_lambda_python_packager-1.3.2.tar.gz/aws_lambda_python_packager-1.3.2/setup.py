# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_lambda_python_packager', 'aws_lambda_python_packager.cli']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp',
 'appdirs',
 'click-log',
 'click-option-group',
 'click>=8',
 'fsspec>=2020.0,!=2022.10.0',
 'packaging',
 'requests',
 'toml>=0.10',
 'wheel']

extras_require = \
{':platform_system == "Windows"': ['python-certifi-win32']}

entry_points = \
{'console_scripts': ['lambda-packager = '
                     'aws_lambda_python_packager.__main__:main']}

setup_kwargs = {
    'name': 'aws-lambda-python-packager',
    'version': '1.3.2',
    'description': 'Description',
    'long_description': '# AWS Lambda Python Packager\n\n[![Checks][checks-shield]][checks-url]\n[![Codecov][codecov-shield]][codecov-url]\n[![PyPi][pypi-shield]][pypi-url]\n\nAn alternate way to package Python functions for AWS Lambda. Works cross-platform and cross-architecture if binary packages are available for all packages.\n\n\n[codecov-shield]: https://img.shields.io/codecov/c/github/mumblepins/aws-lambda-python-packager?style=flat-square\n\n[codecov-url]: https://app.codecov.io/gh/mumblepins/aws-lambda-python-packager\n\n\n[checks-shield]: https://img.shields.io/github/workflow/status/mumblepins/aws-lambda-python-packager/Python%20Publish?style=flat-square\n\n[checks-url]: https://github.com/mumblepins/aws-lambda-python-packager/actions/workflows/python-publish.yml\n\n[pypi-shield]: https://img.shields.io/pypi/v/aws-lambda-python-packager?style=flat-square\n\n[pypi-url]: https://pypi.org/project/aws-lambda-python-packager/\n',
    'author': 'Daniel Sullivan',
    'author_email': 'mumblepins@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mumblepins/aws-lambda-python-packager/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
