import csv
import os
import sys
import argparse
import webbrowser

try:
    from slugify import slugify
except ImportError:
    print('(Slugify import failed; using naive slug function instead.)')
    def slugify(string):
        return string.lower().replace(' ', '-')

DEFAULT_SOURCE = 'Source.csv'
EXAMPLE_SOURCE = 'Sample.csv'
HTML_TEMPLATE = os.path.join('templates', 'template.html')
HTML_OUTFILE = os.path.join('output', 'index.html')

def choose_source():
    """
    Choose the CSV file from which to read sections, questions and answer
    content.
    If the user supplies an argument, look for a file at that filename (and
    complain if one doesn't exist).
    Otherwise use "Source.csv".
    # todo Use a proper argument parser in order to supply a help function.
    :return: a filename (string).
    """
    if len(sys.argv) > 1:
        source = sys.argv[1]
    else:
        source = DEFAULT_SOURCE
    print(f'Looking for source data in "{source}".')
    if os.path.isfile(source):
        return source
    else:
        raise Exception(f'File ("{source}") not found.')
        sys.exit()


def read_csv_data(fn):
    """
    Read data from the CSV source file.
    :return: an iterable of rows of strings.
    """
    with open(fn, 'r', encoding="UTF-8") as infile:
        reader = csv.reader(infile)
        next(reader)  # Ignore headers.
        for line in reader:
            yield line

def get_file_contents(fn):
    """
    Read the contents of file.
    :return: a string.
    """
    with open(fn, 'r') as infile:
        return ''.join((line for line in infile))

def post_process(string):
    """
    Remove forbidden characters.
    Replace codes with words.
    """
    string = string.strip()
    forbidden = {"’": "'", '”': '"', '“': '"',
                 '  ': ' ', '–': '-', "…": "...",
                }
    for forbidden, allowed in forbidden.items():
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

def htmlify(text, indentation):
    """
    Convert a text to basic HTML.
    """
    result_html = ""
    for line in text.split("\n"):
        result_html += f"{indentation}<p>{line}</p>\n"
    return result_html

def user_yes_no(prompt, default="n"):
    """
    Grab a simple yes or no from the user.
    :return: True or False.
    """
    valid_responses = {'y': True, 'n': False}
    prompt += " (y/n)\n".replace(default, default.upper())
    response = input(prompt)
    if not response:
        result = default
    elif response[0].lower()in valid_responses:
        result = response
    else:
        result = default
    return valid_responses[result]

class Store:
    """
    Repository of RFP response information consisting of
    sections with questions and answers.

    write_html is used to create an html outfile in the target directory.
    """
    def __init__(self, filename):
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
                        print(f"The source data contains more than three columns in row {self.questions_count}.")
                        print("Exception row:")
                        print(line)
                        raise Exception

    def _barf_html(self):
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

    def _barf_html_sections(self):
        indentation = '                    '
        output = ""
        list_template = '{ind}<li>\n'\
            '{ind}    <a href="#{}">{}</a>\n'\
            '{ind}</li>\n'
        for section in self.sections:
            html_section = list_template.format(slugify(section), section, ind=indentation)
            output += html_section
        return output

    def write_html(self):
        # TODO Honor indentation
        html = get_file_contents(HTML_TEMPLATE)
        html = html.replace("{ HEADERS }", self._barf_html_sections())
        html = html.replace("{ CONTENT }", self._barf_html())
        with open(HTML_OUTFILE, 'w') as outfile:
            outfile.write(html)

def main():
    csv_source = choose_source()
    s = Store(csv_source)
    print(f"RFP Store data created successfully from {csv_source}.")
    count = "{:,}".format(s.questions_count)
    print(count, "responses recorded.")
    if user_yes_no(f"Write HTML to {HTML_OUTFILE}?", default='y'):
        s.write_html()
        print(f"{HTML_OUTFILE} written.")
        open_file = user_yes_no("Open it now in the web browser?", default='y')
        if open_file:
            webbrowser.open(HTML_OUTFILE)

if __name__ == "__main__":
    main()
