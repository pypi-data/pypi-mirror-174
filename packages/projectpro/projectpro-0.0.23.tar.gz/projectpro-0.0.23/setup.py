from setuptools import setup, find_packages

VERSION = '0.0.23'
DESCRIPTION = 'Code execution logging'
LONG_DESCRIPTION = 'A package that allows to checkpoint/log the state of code execution'

setup(
    name="projectpro",
    version=VERSION,
    author="ProjectPro",
    author_email="mohammed@projectpro.io",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'geocoder'],
    keywords=['python', 'logging', 'checkpoint', 'log', 'script', 'ipynb'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)


