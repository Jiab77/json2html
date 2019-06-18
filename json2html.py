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

class json2html:
	SELF_CLOSING_TAGS = ('meta', 'img', 'br', 'hr')
	DEFAULT_MARKER = '${}'
	MARKERS = ('{{}}', '${}')
	DEBUG = False
	DATA = None

	iterations = 0
	buffer = []
	cli = False
	html = ''
	props = []

	is_array = lambda var: isinstance(var, (list, tuple))

	@staticmethod
	def _convert(decoded_tags, debug):
		nonlocal iterations
		nonlocal buffer
		nonlocal html
		nonlocal props
		nonlocal SELF_CLOSING_TAGS
		
		# Init internal counter
		iterations += 1
		if (debug == True):
			print('Iteration:', iterations + '\n')
		
		# Parse given tags
		for (key, value) in decoded_tags.items():
			if (key == 'tag' or key == '<>'):
				if (debug == True):
					print('Converted [{}] to: <{}>\n', value, value)
					print('is self closing tag:', 'true' if value in SELF_CLOSING_TAGS else 'false')

				buffer.append({'iteration': iterations, 'tag': value})

			elif (key == 'alt' or key == 'class' or key == 'id' or key == 'src' or key == 'href' or key == 'target' or key == 'name' or key == 'action' or key == 'method' or key == 'style'):
				if (debug == True):
					print('Converted to: {} = {}\n', key, value)
				
				props.append({'iteration': iterations, 'attribute': key + '="' + value + '"'})
			
			elif (key == 'child' or key == 'children' or key == 'html'):
				if (is_array(value)):
					for html_tags in value.values():
						json2html._convert(html_tags, debug)
				else:
					if (debug == True):
						print('Converted to: innerHTML="{}"\n', value)
					
					props.append({'iteration': iterations, 'content': value})
			
			elif (key == 'text'):
				if (debug == True):
					print('Converted to: innerText="{}"\n', value)
				
				props.append({'iteration': iterations, 'content': value})
			
			else:
				print('Unsupported tag given. Got: "{}"\n', key)
				return False
	
	@staticmethod
	def _merge():
		nonlocal buffer
		nonlocal props
		nonlocal html

		# Loop on tags
		i = 0
		while i <= len(buffer)-1:
			# Open tag
			html += '<' + buffer[i]['tag']

			# Adding attributes
			j = 0
			while j <= len(props)-1:
				if (props[j]['iteration'] == props[i]['iteration']):
					html += ' ' + props[j]['attribute'] if 'attribute' in props[j] else ''
				
				# Increment counter
				j += 1
			
			# Closing open tag
			html += '>'

			# Adding content
			j = 0
			while j <= len(props)-1:
				if (props[j]['iteration'] == props[i]['iteration']):
					html += props[j]['content'] if 'content' in props[j] else ''
				
				# Increment counter
				j += 1
			
			# Increment counter
			i += 1

		# Close tag
		i = len(buffer)-1
		while i >= 0:
			if (in_array(buffer[i]['tag'], SELF_CLOSING_TAGS) == False):
				html += '</' + buffer[i]['tag'] + '>'
			
			# Deincrement counter
			i -= 1

	@staticmethod
	def _replace(html, data, marker, debug):
		nonlocal MARKERS

		# Validate given marker
		if (in_array(marker, MARKERS)):
			if (marker == '{{}}'):
				regex = r'/({{)(\w*)(}})(\w*)/m'
			elif (marker == '${}'):
				regex = r'/(\${)(\w*)(})(\w*)/m'
		else:
			print('Unsupported marker given.\n')
			return False

		# Apply changes
		matches = re.finditer(regex, html, 0)
		if (len(matches) > 0):
			count = len(matches)

			if (debug == True):
				print(matches)
			
			if (count == len(data)):
				index = 0
				for match in matches:
					if (match[2] != '' and isinstance(match[2], str)):
						html = html.replace(match[0], data[index][match[2]])
						index += 1
		else:
			print('Failed to process data.\n')
			return False
	
	@staticmethod
	def transform(tags, data = DATA, debug = DEBUG, marker = DEFAULT_MARKER):
		if (tags != ''):
			if (isinstance(tags, str)):
				nonlocal buffer
				nonlocal props
				nonlocal html

				# Decode stuff
				tags = tags.decode().encode('UTF-8')
				decoded_tags = json.loads(tags)
				if (data != None):
					data = data.decode().encode('UTF-8')
					decoded_data = json.loads(data)
				else:
					decoded_data = data
				
				# Check decoding result
				if (decoded_tags):
					# Convert tags
					if (debug == True):
						print('\nDecoded:\n')
						print(dir(decoded_tags))
						print(dir(decoded_data))
						print('\nConverting...\n')
					
					json2html._convert(decoded_tags, debug)

					# Merge buffer and props
					if (debug == True):
						print('\nBuffer:\n')
						pprint.pprint(buffer)
						print('\nProps:\n')
						pprint.pprint(props)
						print('\nMergin...\n')
					
					json2html._merge()

					# Parse given data
					if (decoded_data != None):
						if (debug == True):
							print('Adding data...\n')
						
						json2html._replace(html, decoded_data, marker, debug)
					
					# Output result
					return html
				else:
					print(dir(decoded_tags))
					print(dir(data))
					return False
			else:
				print('Tags must be a string. {} given.', type(tags).__name__.capitalize())
				return False
		else:
			print('Empty tags given.')
			return False
