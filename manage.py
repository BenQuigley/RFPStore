import csv
import os

from slugify import slugify

CSV_SOURCE = 'Source.csv'
HTML_TEMPLATE = os.path.join('templates', 'template.html')
HTML_OUTFILE = os.path.join('output', 'index.html')

def read_csv_data(fn):
	"""
	Read data from the CSV source file.
	Ignore headers.
	:return: an iterable of rows of strings.
	"""
	with open(fn, 'r', encoding="UTF-8") as infile:
		reader = csv.reader(infile)
		headers = next(reader)
		for line in reader:
			yield line


def get_html_template(fn):
	"""
	Read HTML data from the template source file.
	:return: a string.
	"""
	with open(fn, 'r') as infile:
		return ''.join((line for line in infile))

def post_process(string):
	"""
	Remove double and trailing spaces.
	Replace codes with words.
	"""
	string = string.strip()
	string = string.replace('  ', ' ')
	codes = {"Y": "Existing functionality",
				"F": "On the roadmap",
				"C": "Available by customization",
				"V": "Available via a vendor",
				"T": "Available via a third party",
			}
	if len(string) == 1 and string in codes.keys():
		string = "{} - {}".format(string, codes[string])
	return string

class Store:
	"""
	Repository of RFP response information consisting of
	sections with questions and answers.

	write_html is used to create an html outfile in the target directory.
	"""
	def __init__(self, filename):
		data = read_csv_data(filename)
		self.sections = {}
		i = 0
		for line in data:
			i += 1
			if line[0]:
				header = line[0]
				self.sections[header] = []
			self.sections[header].append(line[1:3])
		print("RFP Store data created successfully from {}.".format(filename))
		print(i, "responses recorded.")

	def _barf_html(self):
		indentation = '                '
		output = ""
		for section, contents in self.sections.items():
			# Section header:
			output += '{}<h1 id="{}">{}</h1>\n'.format(indentation, slugify(section), section)
			# Table of questions & answers:
			output += '{}<table>'.format(indentation)
			for question, answer in contents:
				question = post_process(question)
				question_html ="<p>{}</p>\n".format(question)
				answer_html = ""
				list_mode = False
				for answer_line in answer.split("\n"):
					answer_line = post_process(answer_line)
					if answer_line[:2] == "* ":
						if list_mode == False:
							list_mode = True
							answer_html += "{}<ul>\n".format(indentation)
						answer_html += "{}    <li>{}</li>\n".format(indentation, answer_line[2:])
					else:
						if list_mode == True:
							list_mode = False
							answer_html += "{}</ul>\n".format(indentation)
						answer_html += "<p>{}</p>\n".format(post_process(answer_line))
				output += "{}<tr><td>{}</td><td>{}</td></tr>".format(indentation, question_html, answer_html)
			output += "{}</table>".format(indentation)
		return output

	def _barf_html_sections(self):
		indentation = '					'
		output = ""
		list_template = '{ind}<li>\n'\
			'{ind}    <a href="#{}">{}</a>\n'\
			'{ind}</li>\n'
		for section in self.sections:
			html_section = list_template.format(slugify(section), section, ind=indentation)
			output += html_section
		return output

	def write_html(self, source_file=None, outfile=None):
		# TODO Honor indentation
		html = get_html_template(HTML_TEMPLATE)
		html = html.replace("{ HEADERS }", self._barf_html_sections())
		html = html.replace("{ CONTENT }", self._barf_html())
		with open(HTML_OUTFILE, 'w') as outfile:
			outfile.write(html)

def main():
	s = Store(CSV_SOURCE)
	s.write_html()

if __name__ == "__main__":
	main()
