JAWS -- Just Another Web Scraper
================================
# Introduction
JAWS is a system for quickly designing web scrapers. It contains a framework for designing custom resources, parsers and outputs for entirely custom scrapers as well as a few implemenations for common use cases.

# Dependenices
JAWS is written in Python, for Python2. The dependencies for the latest version are:
* mechanize==0.2.5
* requests==2.2.1

JAWS can also be installed with easy_install or pip.

# Components
The core components of the JAWS framework can be found in core.py.

## Scraper
The Scraper class is a collection of all the core components into one object which can be easily instantiated and used to scrape all data into your specified output.

## Resource
The JAWSResource class is the abstract class describing the interface by which pages are provided to the parser for scraping. A resource could be as simple as a file reader or as complex as a full Web crawler.

## Parser
The JAWSParser class is the abstract class describing the way your scraper will turn input from the resource into a python dictionary of keys and values to be fed to the output.

## Output
The JAWSOutput class is the abstract class describing what to actually do with that data you have scraped. It could describe a file output format (a csv is probably simplest), a database interface, or whatever else you can think of.

# Future Work
* Automatic Schema Detection
* JSON parser
* Examples for README
* Better documentation in code
* Python3 compatibility

# License
All code and content distributed with JAWS is released under the [GNU GPLv3](http://www.gnu.org/licenses/gpl-3.0.html) unless otherwise specified or prohibited.
