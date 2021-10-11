from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = "Cost model to compute flights' delay cost"
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="CostModels",
    version=VERSION,
    author="Andrea Gasparin, Fulvio Vascotto",
    author_email="<andrea.gasparin.phd@units.it>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='git@github.com:andygaspar/CostModels.git',
    packages=find_packages(),
    license='MIT',
    install_requires=['numpy', 'pandas'],
    keywords=['flights', 'costs', 'cost model', 'delay'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
    ],
    include_package_data=True
)
