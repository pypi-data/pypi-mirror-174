from setuptools import setup, find_packages
import os


VERSION = '0.0.2'
DESCRIPTION = 'Suraj Bherwani\'s helper function'


# Setting up
setup(
    name="fleettwo",
    version=VERSION,
    author="Suraj Bherwani",
    author_email="<avengenation7@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['tensorflow', 'bokeh', 'numpy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)