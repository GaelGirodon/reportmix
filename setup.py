from io import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='reportmix',
    version='0.1.0',
    description='Merge reports from multiple tools into a single file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    url='https://github.com/GaelGirodon/reportmix',
    author='Gael Girodon',
    author_email='contact@gaelgirodon.fr',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='report mix merge security dependency-check npm audit sonarqube owasp',
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'reportmix=reportmix:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/GaelGirodon/reportmix/issues',
        'Source': 'https://github.com/GaelGirodon/reportmix',
    },
)
