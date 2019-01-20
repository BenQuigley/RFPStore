RFP Factory
===========

This Python script creates static web pages for the purpose of
displaying question and answer text in a sectioned format.

Development To-Do
-----------------

1. Write tests.

2. Make the RFP store product a one-page web site.

3. Add flashing of messages to the HTML.

Requirements
------------

::

   $ pip install -r requirements.txt

Usage
-----

To generate an RFP store in ``output/index.html``:

::

   $ python run.py your-data.csv

An example source file is supplied in ``Sample.csv``. An example output
file can be viewed at ``output/sample.html``, or you can generate one
with:

::

   $ python run.py Sample.csv

Acknowledgements
----------------

Thank you to datademofun for the template at
https://github.com/datademofun/heroku-basic-flask/

Thank you to Heroku for the tutorials and hosting the site.

Thank you to `Start Bootstrap <https://startbootstrap.com>`__ for the
`simple-sidebar
<https://github.com/BlackrockDigital/startbootstrap-simple-sidebar>`__ template
which was adapted for this tool's output.
