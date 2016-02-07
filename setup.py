import sys

from setuptools import setup, find_packages

version = '0.1.1'

long_description = """
Extending Python's Future (Promise) object with missing chaining API like `.then()` and others.

Adapting the most useful chaining mechanisms from JavaScript Promises.
"""

project_home = 'https://github.com/dvdotsenko/python-future-then'

requirements = []

if sys.version_info[0] < 3:
    requirements.append('futures') # adds concurrent.futures backport for pre-v3 python


if __name__ == "__main__":
    setup(
        name='futures_then',
        description='Python Futures made then-able',
        long_description=long_description,
        version=version,
        author='Daniel Dotsenko',
        author_email='dotsa@hotmail.com',
        url=project_home,
        download_url=project_home+'/tarball/master',
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7"
        ],
        keywords = ['Promise', 'Future', 'Promises', 'Futures', 'thenable', 'chain'],
        license='MIT',
        packages=['futures_then'],
        include_package_data=True,
        install_requires=requirements
    )

# Next:
# python setup.py register
# python setup.py sdist upload
