"""
MIT License

Copyright (c) 2019 Jonathan Barda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import re
import array
import pprint
import os
import psutil

class json2html:
	SELF_CLOSING_TAGS = ('meta', 'img', 'br', 'hr')
	DEFAULT_MARKER = '${}'
	MARKERS = ('{{}}', '${}')
	DEBUG = False
	DATA = None
	DISPLAY_PROPERTIES = False

	iterations = 0
	childs = 0
	buffer = []
	cli = False
	html = ''
	props = []

	@staticmethod
	def in_array(needle, haystack):
		if (needle in haystack):
			return True
		return False
	
	@staticmethod
	def is_array(needle):
		return isinstance(needle, (list, tuple))

	@staticmethod
	def is_string(needle):
		return isinstance(needle, str)

	@staticmethod
	def contains(needle, string):
		if (string.find(needle) == -1):
			return False
		return True

	@staticmethod
	def display_banner():
		os.system('clear')
		print("""
************
* CLI Mode *
************
""")

	@classmethod
	def invoked_from_bash_cmdline(cls):
		# print('Parent:', psutil.Process(os.getpid()).parent().name())
		if (psutil.Process(os.getpid()).parent().name() == "bash"):
			cls.cli = True
			return True
		return False
	
	@classmethod
	def invoked_as_run_in_terminal(cls):
		# print('Parent:', psutil.Process(os.getpid()).parent().name())
		if (cls.contains('terminal', psutil.Process(os.getpid()).parent().name()) == True):
			cls.cli = True
			return True
		return False
	
	@classmethod
	def _convert(cls, decoded_tags, debug):
		# Init internal counter
		cls.iterations += 1
		if (debug == True):
			print('\n* Iteration:', cls.iterations)
		
		# Parse given tags
		for (key, value) in decoded_tags.items():
			if (key == 'tag' or key == '<>'):
				cls.buffer.append({'iteration': cls.iterations, 'tag': value})
				if (debug == True):
					print('Converted [' + value + '] to: <' + value + '>')
					print('is self closing tag:', 'true' if value in cls.SELF_CLOSING_TAGS else 'false')

			elif (key == 'alt' or key == 'class' or key == 'id' or key == 'src' or key == 'href' or key == 'target' or key == 'name' or key == 'action' or key == 'method' or key == 'style'):
				cls.props.append({'iteration': cls.iterations, 'attribute': key + '="' + value + '"'})
				if (debug == True):
					print('Converted to: ' + key + ' = "' + value + '"')
			
			elif (key == 'child' or key == 'children' or key == 'html'):
				if (cls.is_array(value)):
					for html_tags in value:
						cls._convert(html_tags, debug)
				else:
					cls.props.append({'iteration': cls.iterations, 'content': value})
					if (debug == True):
						print('Converted to: innerHTML="' + value + '"')
			
			elif (key == 'text'):
				cls.props.append({'iteration': cls.iterations, 'content': value})
				if (debug == True):
					print('Converted to: innerText="' + value + '"')
				
			else:
				print('Unsupported tag given. Got: "' + key + '"\n')
				return False
	
	@classmethod
	def _merge(cls, debug):
		# Loop on tags
		i = 0
		while i <= len(cls.buffer)-1:
			# Debug pass
			if (debug == True):
				print('Pass:', i)

			# Open tag
			cls.html += '<' + cls.buffer[i]['tag']

			# Reading props
			if (debug == True):
				print('Props:', cls.props)

			# Adding attributes
			for j in range(0, len(cls.props)):
				if (cls.props[j]['iteration'] == cls.props[i]['iteration']):
					# print('J:A:', cls.props[j]['iteration'], '==', 'I:A:', cls.props[i]['iteration'])
					cls.html += ' ' + cls.props[j]['attribute'] if 'attribute' in cls.props[j] else ''
					
			# Closing open tag
			cls.html += '>'

			# Adding content
			for k in range(0, len(cls.props)):
				if (cls.props[k]['iteration'] == cls.props[i]['iteration']):
					# print('K:C:', cls.props[k]['iteration'], '==', 'I:C:', cls.props[i]['iteration'])
					cls.html += cls.props[k]['content'] if 'content' in cls.props[k] else ''
			
			# Remove consumed props[i] (passed around 3 hours on that crap!!)
			del cls.props[i]

			# Increment tag open counter
			i += 1

		# Close tag
		i = len(cls.buffer)-1
		while i >= 0:
		# for i in range(0, len(cls.buffer)):
			if (cls.in_array(cls.buffer[i]['tag'], cls.SELF_CLOSING_TAGS) == False):
				cls.html += '</' + cls.buffer[i]['tag'] + '>'
			
			# Deincrement tag close counter
			i -= 1

	@classmethod
	def _replace(cls, html, data, marker, debug):
		# Additional debug infos
		if (debug == True):
			print('Data:', data)
			print('Used marker:', marker)

		# Validate given marker
		if (cls.in_array(marker, cls.MARKERS)):
			if (marker == '{{}}'):
				regex = r"({{)(\w*)(}})(\w*)"
			elif (marker == '${}'):
				regex = r"(\${)(\w*)(})(\w*)"
		else:
			print('Unsupported marker given.\n')
			return False

		# Apply changes
		matches = re.finditer(regex, html, re.MULTILINE)
		if (debug == True):
			print('Used regex:', regex)
			print('Search in:', html)
			print('Results:', matches)

		if (matches):
			## Loop on matches
			index = 0
			for matchNum, match in enumerate(matches, start=1):
				if (debug == True):
					print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
				cls.html = cls.html.replace(match.group(), data[index][match.group(2)])

				## Increment data counter
				index += 1
			
				""" for groupNum in range(0, len(match.groups())):
					groupNum = groupNum + 1
					print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum))) """
		else:
			print('Failed to process data.\n')
			return False
	
	@classmethod
	def transform(cls, tags, data = None, debug = None, marker = None):
		# Run some internal methods
		cls.invoked_from_bash_cmdline()
		cls.invoked_as_run_in_terminal()

		# Display banner when on CLI mode
		if (cls.cli == True):
			cls.display_banner()

		# Save state
		encoded_tags = tags
		encoded_data = data

		# Assign default props
		if (data == None):
			data = cls.DATA
		
		if (debug == None):
			debug = cls.DEBUG
		
		if (marker == None):
			marker = cls.DEFAULT_MARKER

		# Display some internal debugging info
		if (cls.cli == True):
			if (debug == True):
				if (cls.DISPLAY_PROPERTIES == True):
					print('* Received:\n', encoded_tags, '\n\n ==> Properties:\n', dir(encoded_tags))
				else:
					print('* Received:\n', encoded_tags)
			else:
				print('Received:\n', encoded_tags)

		# Check if you we got tags to process
		if (encoded_tags != ''):
			# Check given tags type
			if (cls.is_string(encoded_tags)):
				# Decode tags
				decoded_tags = json.loads(encoded_tags)

				# Decode data
				if (encoded_data != None):
					decoded_data = json.loads(encoded_data)
				else:
					decoded_data = encoded_data
				
				# Check decoding result
				if (decoded_tags):
					if (debug == True):
						if (cls.DISPLAY_PROPERTIES == True):
							print('\n* Decoded tags:\n', decoded_tags, '\n\n ==> Properties:\n', dir(decoded_tags))
							print('\n* Decoded data:\n', decoded_data, '\n\n ==> Properties:\n', dir(decoded_data))
						else:
							print('\n* Decoded tags:\n', decoded_tags)
							print('\n* Decoded data:\n', decoded_data)
						print('\nConverting...')
					
					# Convert tags
					cls._convert(decoded_tags, debug)

					# Display memory info
					if (debug == True):
						print('\n* Buffer:', len(cls.buffer), '\n')
						pprint.pprint(cls.buffer)
						print('\n* Props:', len(cls.props), '\n')
						pprint.pprint(cls.props)
						print('\nMerging...\n')
					
					# Merge buffer and props
					cls._merge(debug)

					# Parse given data
					if (decoded_data != None):
						if (cls.cli == True):
							print(decoded_data)
						if (debug == True):
							print('\nAdding data...\n')
						cls._replace(cls.html, decoded_data, marker, debug)
					
					# Output result
					if (cls.cli == True):
						print('\nConverted:\n', cls.html, '\n')
					return cls.html
				
				# Return debug info on error
				else:
					print('Failed to parse tags/data.')
					if (debug == True):
						print(dir(decoded_tags))
						print(dir(data))
					return False
			else:
				print('Tags must be a string. ' + type(tags).__name__.capitalize() + ' given.')
				return False
		else:
			print('Empty tags given.')
			return False

# Required execution code
def main():
	# Test payload / data
	# fail result
	# payload = ['x', 'y']
	
	# pass result
	# payload = '{"<>":"div","class":"card", "id":"8465416541651365132","html":[{"<>":"img", "src":"https://picsum.photos/id/82/400?random=54654654654","alt":"this is our logo"},{"<>":"p","text":"Hi {{name}}! Welcome to json2html!"}]}'
	# payload = '{"<>":"div","class":"{{class}}", "id":"8465416541651365132","html":[{"<>":"img", "src":"https://picsum.photos/id/82/400?random=54654654654","alt":"this is our logo"},{"<>":"p","text":"Hi {{name}}! Welcome to json2html!"}]}'
	# payload = '{"<>":"div","class":"${class}", "id":"8465416541651365132","html":[{"<>":"img", "src":"https://picsum.photos/id/82/400?random=54654654654","alt":"this is our logo"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"}]}'
	payload = '{"<>":"div","class":"${class}", "id":"${id}","html":[{"<>":"img", "src":"${src}","alt":"${alt}"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"},{"<>":"p","text":"Awesome it works!"}]}'

	# Test data
	# fail result
	# data = ''
	# data = '[]'

	# pass result
	# data = None
	# data = '[{"name":"Jo"}]'
	# data = '[{"id":"element_id"},{"name":"Jo"}]'
	# data = '[{"class":"card"},{"name":"Jo"}]'
	data = '[{"class":"card"},{"id":"element_id"},{"src":"https://picsum.photos/id/82/400?random=54654654654"},{"alt":"this is our logo"},{"name":"Jo"}]'

	global json2html
	# json2html.transform(payload, data, True)
	json2html.transform(payload, data)

try:
	main()
except KeyboardInterrupt:
	print('\nKeyboardInterrupt has been caught.')
	exit(1)