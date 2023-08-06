from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.12'
DESCRIPTION = 'STM32 CLI'
LONG_DESCRIPTION = 'A package that allows comunicate STM32'

# Setting up
setup(
    name="stm32cli",
    version=VERSION,
    author="loye (PHUC LOI)",
    author_email="phucloi97@hotmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pyserial', 'colorama', 'click'],
    keywords=["stm32", "cli", "bootloader"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
      "console_scripts":[
        "stm32cli=stm32cli:main",
        ],
    },

)