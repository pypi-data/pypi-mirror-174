from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Extracting the content from the webpage'
LONG_DESCRIPTION = 'A package that allows to extract content from the webpage accessed via URL or the html file.'

# Setting up
setup(
    name="contentfetch",
    version=VERSION,
    author="aidotio",
    author_email="neneranadheer@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['beautifulsoup4','requests','news-please','newspaper3k','pandas','selenium','chromedriver_binary','unidecode','fake_useragent',
    ],
    keywords=['webpage','scrape','crawl'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)