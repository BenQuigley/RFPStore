import csv
import os

from slugify import slugify

def read_data(fn):
	with open(fn, 'r', encoding="UTF-8") as infile:
		reader = csv.reader(infile)
		headers = next(reader)
		for line in reader:
			yield line

def clean(string):
	"""
	Removes double and trailing spaces.
	"""
	return string.strip().replace('  ', ' ')
	
class Store:
	def __init__(self, filename):
		data = read_data(filename)
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
	
	def barf_html(self):
		indentation = '                '
		output = ""
		for section, contents in self.sections.items():
			output += '{}<h1 id="{}">{}</h1>\n'.format(indentation, slugify(section), section)
			for question, answer in contents:
				output += "{}<h3>{}</h2>\n".format(indentation, question)
				for answer_line in answer.split("\n"):
					output += "{}<p>{}</p>\n".format(indentation, clean(answer_line))
		return output
		
	def barf_html_sections(self):
		indentation = '					'
		output = ""
		list_template = '{ind}<li>\n'\
			'{ind}    <a href="#{}">{}</a>\n'\
			'{ind}</li>\n'
		for section in self.sections:
			html_section = list_template.format(slugify(section), section, ind=indentation)
			output += html_section
		return output
	
	def get_html_template(self, fn):
		with open(fn, 'r') as infile:
			return "".join((line for line in infile))
	
	def write_html(self, source_file=None, outfile=None):
		# TODO Honor indentation
		if source_file is None:
			source_file = os.path.join("startbootstrap-simple-sidebar", "index.html")
		if outfile is None:
			outfile = os.path.join('startbootstrap-simple-sidebar', 'outfile.html')
		html = self.get_html_template(source_file)
		html = html.replace("{ HEADERS }", self.barf_html_sections())
		html = html.replace("{ CONTENT }", self.barf_html())
		with open(outfile, 'w') as outfile:
			outfile.write(html)

		
def main():
	s = Store("Source.csv")
	s.write_html()
	
if __name__ == "__main__":
	main()