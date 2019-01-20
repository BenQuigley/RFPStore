import csv
import os
import sys
import argparse
import webbrowser
from typing import Iterator

try:
    from slugify import slugify
except ImportError:
    print('(Slugify import failed; using naive slug function instead.)')

    def slugify(string):
        return string.lower().replace(' ', '-')

VERBOSE = False
HTML_TEMPLATE = os.path.join('rfp-store', 'template.html')
HTML_OUTFILE = os.path.join('rfp-store', 'index.html')


def printv(*args, **kwargs):
    '''
    Print only if in verbose mode.
    '''
    if VERBOSE:
        print(*args)


def read_csv_data(fn: str) -> Iterator:
    """
    Read data from the CSV source file.
    :return: an iterable of rows of strings.
    """
    with open(fn, 'r', encoding="UTF-8") as infile:
        reader = csv.reader(infile)
        next(reader)  # Ignore headers.
        for line in reader:
            yield line


def get_file_contents(fn: str) -> str:
    """
    Read the contents of file.
    :return: a string.
    """
    with open(fn, 'r') as infile:
        return ''.join((line for line in infile))


def post_process(string: str) -> str:
    """
    Remove forbidden characters.
    Replace codes with words.
    """
    string = string.strip()
    forbidden_strings = {"’": "'", '”': '"', '“': '"',
                         '  ': ' ', '–': '-', "…": "...",
                         }
    for forbidden, allowed in forbidden_strings.items():
        string = string.replace(forbidden, allowed)
    codes = {"Y": "Existing functionality",
             "F": "On the roadmap",
             "C": "Available by customization",
             "V": "Available via a vendor",
             "T": "Available via a third party",
             "N": "Not available",
             }
    output = ""
    for line in string.split('\n'):
        if len(string) == 1 and string in codes.keys():
            line = "{} - {}".format(string, codes[string])
        output += line + "\n"
    return output


def htmlify(text: str, indentation: str):
    """
    Convert a text to basic HTML.
    """
    result_html = ""
    list_mode = False
    for line in text.split("\n"):
        if line[:2] == "* ":
            if not list_mode:
                list_mode = True
                result_html += f"{indentation}<ul>\n"
            line = line[2:]
            result_html += f"{indentation}    <li>{line}</li>\n"
        else:
            if list_mode:
                list_mode = False
                result_html += f"{indentation}</ul>\n"
            result_html += f"{indentation}<p>{line}</p>\n"
    if list_mode:
        list_mode = False
        result_html += f"{indentation}</ul>\n"
    return result_html


class Store:
    """
    Repository of RFP response information consisting of
    sections with questions and answers.

    write_html is used to create an html outfile in the target directory.
    """
    sections: dict
    questions_count: int

    def __init__(self, filename) -> None:
        data = read_csv_data(filename)
        self.sections = {}
        self.questions_count = 0
        header = ""
        for line in data:
            self.questions_count += 1
            if line[0] and line[0] != header:
                header = line[0]
                self.sections[header] = []
            self.sections[header].append(line[1:3])
            # Check rest of line for data and throw an error:
            if len(line) > 3:
                for val in line[3:]:
                    if val:
                        exception = ('The source data contains more than three'
                                     f' columns in row {self.questions_count}.'
                                     'Exception row:' + line)
                        raise Exception

    def _barf_html(self) -> str:
        """
        Render HTML content for the questions and answers of each section.
        """
        indentation = '                '  # Todo: indent dynamically
        output = ""
        for section, contents in self.sections.items():
            # Section header:
            section_slug = slugify(section)
            output += f'{indentation}<h1 id="{section_slug}">{section}</h1>\n'
            # Table of questions & answers:
            output += f'{indentation}<table>'
            for question, answer in contents:
                question_html = htmlify(post_process(question), indentation)
                answer_html = htmlify(post_process(answer), indentation)
                output += f"{indentation}<tr><td>{question_html}</td><td>"\
                           f"{answer_html}</td></tr>"
            output += f"{indentation}</table>"
        return output

    def _barf_html_sections(self) -> str:
        indentation = '                    '
        output = ""
        list_template = '{ind}<li>\n'\
            '{ind}    <a href="#{}">{}</a>\n'\
            '{ind}</li>\n'
        for section in self.sections:
            printv(section)
            html_section = list_template.format(slugify(section), section,
                                                ind=indentation)
            output += html_section
        return output

    def write_html(self, target_location):
        # TODO Honor indentation
        html = get_file_contents(HTML_TEMPLATE)
        html = html.replace("{ HEADERS }", self._barf_html_sections())
        html = html.replace("{ CONTENT }", self._barf_html())
        with open(target_location, 'w') as outfile:
            outfile.write(html)
