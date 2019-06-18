<?php
class json2html
{
	const SELF_CLOSING_TAGS = ['meta', 'img', 'br', 'hr'];
	const DEFAULT_MARKER = '${}';
	const MARKERS = ['{{}}', '${}'];
	const DEBUG = false;
	const DATA = null;

	private static $iterations = 0;
	private static $buffer = [];
	private static $cli = false;
	private static $html = '';
	private static $props = [];

	private static function _check_extensions()
	{
		if (!extension_loaded('mbstring')) {
			echo 'Extension mbstring not loaded.';
			return false;
		}
		if (!extension_loaded('json')) {
			echo 'Extension json not loaded.';
			return false;
		}
	}

	private static function _check_sapi()
	{
		if (substr(PHP_SAPI, 0, 3) !== 'cgi') {
			self::$cli = true;
		}
	}
	
	private static function _convert($decoded_tags, $debug)
	{
		// Init internal counter
		self::$iterations++;
		if ($debug === true) {
			echo 'Iteration: ' . self::$iterations . PHP_EOL;
		}

		// Parse given tags
		foreach ($decoded_tags as $key => $value) {
			switch ($key) {
				case 'tag':
				case '<>':
					if ($debug === true) {
						echo 'Converted [' . $value . '] to: <' . $value . '>' . PHP_EOL;
						echo 'is self closing tags: ' . (in_array($value, self::SELF_CLOSING_TAGS) ? 'true' : 'false') . PHP_EOL;
					}

					self::$buffer[] = ['iteration' => self::$iterations, 'tag' => $value];
					break;

				case 'alt':
				case 'class':
				case 'id':
				case 'src':
				case 'href':
				case 'target':
				case 'name':
				case 'action':
				case 'method':
				case 'style':
					if ($debug === true) {
						echo 'Converted to: ' . $key . '="' . $value . '"' . PHP_EOL;
					}

					self::$props[] = ['iteration' => self::$iterations, 'attribute' => $key . '="' . $value . '"'];
					break;

				case 'child':
				case 'children':
				case 'html':
					if (is_array($value)) {
						foreach ($value as $html_tags) {
							self::_convert($html_tags, $debug);
						}
					}
					else {
						if ($debug === true) {
							echo 'Converted to: innerHTML="' . htmlentities(strip_tags($value)) . '"' . PHP_EOL;
						}

						self::$props[] = ['iteration' => self::$iterations, 'content' => htmlentities(strip_tags($value))];
					}
					break;

				case 'text':
					if ($debug === true) {
						echo 'Converted to: innerText="' . html_entity_decode(strip_tags($value)) . '"' . PHP_EOL;
					}

					self::$props[] = ['iteration' => self::$iterations, 'content' => html_entity_decode(strip_tags($value))];
					break;
				
				default:
					echo 'Unsupported tag given. Got: "' . $key . '"' . PHP_EOL;
					return false;
					break;
			}
		}
	}

	private static function _merge()
	{
		// Loop on tags
		for ($i = 0; $i <= count(self::$buffer)-1; $i++) {
			// Open tag
			self::$html .= '<' . self::$buffer[$i]['tag'];

			// Adding attributes
			for ($j = 0; $j <= count(self::$props)-1; $j++) {
				if (self::$props[$j]['iteration'] === self::$buffer[$i]['iteration']) {
					self::$html .= (array_key_exists('attribute', self::$props[$j]) !== false ? ' ' . self::$props[$j]['attribute'] : '');
				}
			}

			// Closing open tag
			self::$html .= '>';

			// Adding content
			for ($j = 0; $j <= count(self::$props)-1; $j++) {
				if (self::$props[$j]['iteration'] === self::$buffer[$i]['iteration']) {
					self::$html .= (array_key_exists('content', self::$props[$j]) !== false ? self::$props[$j]['content'] : '');
				}
			}
		}

		// Close tag
		for ($i = count(self::$buffer)-1; $i >= 0; $i--) {
			if (!in_array(self::$buffer[$i]['tag'], self::SELF_CLOSING_TAGS)) {
				self::$html .= '</' . self::$buffer[$i]['tag'] . '>';
			}
		}
	}

	private static function _replace($html, $data, $marker, $debug)
	{
		// Validate given marker
		if (in_array($marker, self::MARKERS)) {
			switch ($marker) {
				case '{{}}':
					$re = '/({{)(\w*)(}})(\w*)/m';
					break;
				case '${}':
					$re = '/(\${)(\w*)(})(\w*)/m';
					break;
			}
		}
		else {
			echo 'Unsupported marker given.' . PHP_EOL;
			return false;
		}
		
		// Apply changes
		if (preg_match_all($re, $html, $matches, PREG_SET_ORDER, 0) !== false) {
			$count = count($matches);
				
			if ($debug === true) {
				// Print the entire match result
				var_dump($matches);
			}
	
			if ($count === count($data)) {
				$index = 0;
				foreach ($matches as $match) {
					if (!empty($match[2]) && is_string($match[2])) {
						self::$html = str_replace($match[0], $data[$index]->{$match[2]}, self::$html);
						$index++;
					}
				}
			}
		}
		else {
			echo 'Failed to process data.' . PHP_EOL;
			return false;
		}
	}

	public static function transform($tags, $data = self::DATA, $debug = self::DEBUG, $marker = self::DEFAULT_MARKER)
	{
		if (!empty($tags)) {
			if (is_string($tags)) {
				// Check internals
				self::_check_extensions();
				self::_check_sapi();

				// Output internal debug on CLI
				if (self::$cli === true) {
					echo 'Received:' . PHP_EOL;
					var_dump($tags, $data);
				}

				// Decode stuff
				$tags = mb_convert_encoding($tags, 'UTF-8');
				$decoded_tags = json_decode($tags);
				if (!is_null($data)) {
					$data = mb_convert_encoding($data, 'UTF-8');
					$decoded_data = json_decode($data);
				}
				else {
					$decoded_data = $data;
				}

				// Check decoding result
				if ($decoded_tags) {
					// Convert tags
					if ($debug === true) {
						echo PHP_EOL . 'Decoded:' . PHP_EOL;
						var_dump($decoded_tags, $decoded_data);
						echo PHP_EOL . 'Converting...' . PHP_EOL;
					}
					self::_convert($decoded_tags, $debug);

					// Merge buffer and props
					if ($debug === true) {
						echo PHP_EOL . 'Buffer:' . PHP_EOL;
						print_r(self::$buffer);
						echo PHP_EOL . 'Props:' . PHP_EOL;
						print_r(self::$props);
						echo PHP_EOL . 'Merging...' . PHP_EOL;
					}
					self::_merge();

					// Parse given data
					if (!is_null($decoded_data)) {
						if ($debug === true) {
							echo 'Adding data...' . PHP_EOL;
						}
						self::_replace(self::$html, $decoded_data, $marker, $debug);
					}

					// Output internal debug on CLI
					if (self::$cli === true) {
						echo PHP_EOL . 'Converted:' . PHP_EOL;
						var_dump(self::$html);
					}

					// Output result
					return self::$html;
				}
				else {
					var_dump($decoded_tags, json_last_error(), json_last_error_msg(), $data);
					return false;
				}
			}
			else {
				echo 'Tags must be a string. ' . ucfirst(gettype($tags)) . ' given.' . PHP_EOL;
				return false;
			}
		}
		else {
			echo 'Empty tags given.' . PHP_EOL;
			return false;
		}
	}
}

// Test payload / data
// $payload = '{"<>":"div","class":"card", "id":"' . uniqid() . '","html":[{"<>":"img", "src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '","alt":"this is our logo"},{"<>":"p","text":"Hi {{name}}! Welcome to json2html!"}]}';
// $payload = '{"<>":"div","class":"{{class}}", "id":"' . uniqid() . '","html":[{"<>":"img", "src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '","alt":"this is our logo"},{"<>":"p","text":"Hi {{name}}! Welcome to json2html!"}]}';
// $payload = '{"<>":"div","class":"${class}", "id":"' . uniqid() . '","html":[{"<>":"img", "src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '","alt":"this is our logo"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"}]}';
$payload = '{"<>":"div","class":"${class}", "id":"${id}","html":[{"<>":"img", "src":"${src}","alt":"${alt}"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"}]}';
// $payload = ['x', 'y'];
// $payload = new stdClass;

// $data = '[{"name":"Jo"}]';
// $data = '[{"class":"card"}, {"name":"Jo"}]';
$data = '[{"class":"card"}, {"id":"' . uniqid() . '"}, {"src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '"}, {"alt":"this is our logo"}, {"name":"Jo"}]';
// $data = '[{"id":"' . uniqid() . '"}, {"class":"card"}, {"src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '"}, {"alt":"this is our logo"}, {"name":"Jo"}]';

json2html::transform($payload, $data, false);
