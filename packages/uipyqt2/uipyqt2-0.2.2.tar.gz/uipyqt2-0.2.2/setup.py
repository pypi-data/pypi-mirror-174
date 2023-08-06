from io import open
from setuptools import setup


version = "0.2.2"
long_description = "My first module on python. He need for create UI on python"

setup(
    name = "uipyqt2",
    version = version,
    author = "brauser_vekato",
    author_email = "vovbon6767@gmail.com",
    descriptions = (
        u"My first module on python. He need for create UI on python"

    ),
    long_description = long_description,
    license = "Apache License, Version 2.0, see LICENSE file",
    packages = ["uipyqt2"],
    install_requires=["pyqt6"],

    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
        
    ]


)