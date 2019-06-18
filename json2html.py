import json
import re
import array
import pprint

class json2html:
	SELF_CLOSING_TAGS = ['meta', 'img', 'br', 'hr']
	DEFAULT_MARKER = '${}'
	MARKERS = ['{{}}', '${}']
	DEBUG = false
	DATA = null

	iterations = 0
	buffer = {}
	cli = False
	html = ''
	props = {}

	is_array = lambda var: isinstance(var, (list, tuple))

	@staticmethod
	def _convert(decoded_tags, debug):
		# Init internal counter
		self.iterations += 1
		if (debug == True):
			print('Iteration:', self.iterations + '\n')
		
		# Parse given tags
		for (key, value) in decoded_tags.items():
			if (key == 'tag' or key == '<>'):
				if (debug == True):
					print('Converted [{}] to: <{}>\n', value, value)
					print('is self closing tag:', 'true' if value in SELF_CLOSING_TAGS else 'false')

				self.buffer[] = ['iteration' = self.iterations, 'tag' = value]

			elif (key == 'alt' or key == 'class' or key == 'id' or key == 'src'):
				if (debug == True):
					print('Converted to: {} = {}\n', key, value)
				
				self.props[] = ['iteration' = self.iterations, 'attribute' = key + '="' + value + '"']
			
			elif (key == 'child' or key == 'children' or key == 'html'):
				if (is_array(value)):
					for html_tags in value.values():
						self._convert(html_tags, debug)
				else:
					if (debug == True):
						print('Converted to: innerHTML="{}"\n', value)
					
					self.props[] = ['iteration' = self.iterations, 'content' = value]
			
			elif (key == 'text'):
				if (debug == True):
					print('Converted to: innerText="{}"\n', value)
				
				self.props[] = ['iteration' = self.iterations, 'content' = value]
			
			else:
				print('Unsupported tag given. Got: "{}"\n', key)
				return False
	
	@staticmethod
	def _merge():
		# Loop on tags
		i = 0
		while i <= len(self.buffer)-1:
			# Open tag
			self.html += '<' + self.buffer[i]['tag']

			# Adding attributes
			j = 0
			while j <= len(self.props)-1:
				if (self.props[j]['iteration'] == self.props[i]['iteration']):
					self.html += ' ' + self.props[j]['attribute'] if 'attribute' in self.props[j] else ''
				
				# Increment counter
				j += 1
			
			# Closing open tag
			self.html += '>'

			# Adding content
			j = 0
			while j <= len(self.props)-1:
				if (self.props[j]['iteration'] == self.props[i]['iteration']):
					self.html += self.props[j]['content'] if 'content' in self.props[j] else ''
				
				# Increment counter
				j += 1
			
			# Increment counter
			i += 1

		# Close tag
		i = len(self.buffer)-1
		while i >= 0:
			if (in_array(self.buffer[i]['tag'], SELF_CLOSING_TAGS) == False):
				self.html += '</' + self.buffer[i]['tag'] + '>'
			
			# Deincrement counter
			i -= 1

	@staticmethod
	def _replace(html, data, marker, debug):
		# Validate given marker
		if (in_array(marker, MARKERS)):
			if (marker == '{{}}'):
				re = r'/({{)(\w*)(}})(\w*)/m'
			elif (marker == '${}'):
				re = r'/(\${)(\w*)(})(\w*)/m'
		else:
			print('Unsupported marker given.\n')
			return False

		# Apply changes
		if (matches = re.finditer(re, html, 0)):
			count = len(matches)

			if (debug == True):
				print(matches)
			
			if (count == len(data)):
				index = 0
				for match in matches:
					if (match[2] != '' and isinstance(match[2], str)):
						self.html = self.html.replace(match[0], data[index]->{match[2]})
						index += 1
		else:
			print('Failed to process data.\n')
			return False
	
	@staticmethod
	def transform(tags, data = DATA, debug = DEBUG, marker = DEFAULT_MARKER):
		if (tags != ''):
			if (isinstance(tags, str)):
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
						print dir(decoded_tags)
						print dir(decoded_data)
						print('\nConverting...\n')
					
					self._convert(decoded_tags, debug)

					# Merge buffer and props
					if (debug == True):
						print('\nBuffer:\n')
						pprint.pprint(self.buffer)
						print('\nProps:\n')
						pprint.pprint(self.props)
						print('\nMergin...\n')
					
					self._merge()

					# Parse given data
					if (decoded_data != None):
						if (debug == True):
							print('Adding data...\n')
						
						self._replace(self.html, decoded_data, marker, debug)
					
					# Output result
					return self.html
				else:
					print dir(decoded_tags)
					print dir(data)
					return False
			else:
				print('Tags must be a string. {} given.', type(tags).__name__.capitalize())
				return False
		else:
			print('Empty tags given.')
			return False