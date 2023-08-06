from setuptools import find_packages, setup
# import sys

# if sys.version_info < (3, 9):
#     raise RuntimeError('This package require ZoneInfo')

with open('README_PUB.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ciberc-lg",
    packages=find_packages(),
    version="0.4.0",
    description="Lighting Gale client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://<site>.readthedocs.io/",
    license="GPLv3",
    author="CiberC Dev",
    install_requires=[
        'requests>=2.28',
        'pydantic>=1.9',
    ],
    python_requires='>=3.9',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
