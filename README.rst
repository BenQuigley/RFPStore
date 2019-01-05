RFP Store
=========

This Python script creates static web pages for the purpose of 
displaying question and answer text in a sectioned format.

The HTML output uses Bootstrap. It is adapted from the
[simple-sidebar](https://github.com/BlackrockDigital/startbootstrap-simple-sidebar)
template by [Start Bootstrap](https://startbootstrap.com). You can see a sample
[here](https://blackrockdigital.github.io/startbootstrap-simple-sidebar/).

Development To-Do
-----------------

1. Hook up to Heroku
2. Create frontend for users in Bootstrap
3. Implement backend in Flask
4. Get everything out of the output/ folder that's not automatically generated.

Requirements
------------

[slugify](https://github.com/un33k/python-slugify) is used, but isn't strictly
required. To install:

    $ pip install slugify

Usage
-----

To generate an RFP store in `output/index.html`:

    $ python run.py your-data.csv

An example source file is supplied in `Sample.csv`. An example output file can
be viewed at `output/sample.html`, or you can generate one with:

    $ python run.py Sample.csv
	
To use the default source data location of `Source.csv`, you can run the script
with no arguments:

    $ python run.py
