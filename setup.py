"""
ReportMix setup file.
"""

import re
from io import open
from os import path

from setuptools import setup, find_packages

DIR = path.abspath(path.dirname(__file__))


def get_long_description() -> str:
    """
    Get the long description from the README.md file.
    :return: Long description
    """
    with open(path.join(DIR, 'README.md'), encoding='utf-8') as file:
        return file.read()


def get_version() -> str:
    """
    Get the version number from reportmix/main.py.
    :return: Version number
    """
    main_file = path.join(DIR, 'reportmix', 'main.py')
    version_re = re.compile(r'__version__\s+=\s+"(?P<version>.*)"')
    with open(main_file, 'r', encoding='utf-8') as file:
        match = version_re.search(file.read())
        return match.group('version') if match is not None else 'unknown'


setup(
    name='reportmix',
    version=get_version(),
    description='Merge reports from multiple tools into a single file',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/GaelGirodon/reportmix',
    author='Gael Girodon',
    author_email='contact@gaelgirodon.fr',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security',
        'Topic :: Software Development :: Quality Assurance',
    ],
    keywords='report mix merge security dependency-check npm audit sonarqube owasp',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.24.0',
        'jinja2>=2.11.2'
    ],
    entry_points={
        'console_scripts': [
            'reportmix=reportmix.main:main'
        ]
    },
    project_urls={
        'Bug Reports': 'https://github.com/GaelGirodon/reportmix/issues',
        'Source': 'https://github.com/GaelGirodon/reportmix',
    },
)
