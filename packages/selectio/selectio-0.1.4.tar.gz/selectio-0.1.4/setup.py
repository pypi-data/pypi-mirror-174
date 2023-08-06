try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setupp
from os import path
import io

PYPI_VERSION = '0.1.4'

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

packages = find_packages()

if __name__ == "__main__":
    setup(name = 'selectio',
          author            = "Sebastian Haan",
          url               = "https://github.com/sebhaan/selectio",
          version           = PYPI_VERSION ,
          description       = "Multi-model Feature Importance Scoring and Auto Feature Selection",
          long_description  = long_description,
          long_description_content_type='text/markdown',
          license           = 'MIT',
          install_requires  = ['scikit_learn>=1.0',
                                'numpy>=1.21',
                                'pandas>=1.3.5',
                                'pyyaml>=6.0',
                                'scipy>=1.7.3',
                                'matplotlib>=3.5',
                                ],
          python_requires   = '>=3.8',
          packages          = packages,
          package_data      = {'selectio': ['settings/settings_featureimportance.yaml']},
          include_package_data=True,
          classifiers       = ['Programming Language :: Python :: 3',
                                'Operating System :: OS Independent',
                               ]
          )