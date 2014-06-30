from setuptools import find_packages, setup
import os.path

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

setup(
    name="txnrpe",
    version="1.0a",
    packages=find_packages(),
    install_requires=["Twisted >= 14.0.0"],
    author="Petri Savolainen",
    author_email="petri.savolainen@koodaamo.fi",
    classifiers=classifiers,
    description="A NRPE client/server implementation for Twisted",
    license="GPL2",
    url="http://github.com/koodaamo/txnrpe",
    long_description=file('README.md').read()
)
