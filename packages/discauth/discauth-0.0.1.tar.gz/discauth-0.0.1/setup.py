from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))



VERSION = '0.0.1'
DESCRIPTION = 'package(api wrapper) to help using the discord oauth2 api endpoints with less programming '

# Setting up
setup(
    name="discauth",
    version=VERSION,
    author="ui",
    author_email="bitcoin@sexism.cc",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="View the github repo [here](https://github.com/uiisback/discauth) for more info!",
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'discord', 'oauth', 'discauth', 'oauth2'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)