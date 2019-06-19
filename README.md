# JSON2HTML
JSON to HTML converter - It will follow the same spec as http://json2html.com/examples/

## Available Versions
I wrote two versions:
 * a `PHP` version **(working)**
 * a `Python` version **(working)**

## PHP version
Just include the file `json2html.php` into your code.

```php
require_once 'json2html.php';

# your code
```

And use it that way:

```php
require_once 'json2html.php';

$payload = '{"<>":"div","class":"${class}", "id":"${id}","html":[{"<>":"img", "src":"${src}","alt":"${alt}"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"}]}';

$data = '[{"class":"card"}, {"id":"' . uniqid() . '"}, {"src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '"}, {"alt":"this is our logo"}, {"name":"Jo"}]';

/* Apply transform to get HTML output */
echo json2html::transform($payload, $data); // Payload, Data, Debug (true | false)
```

### Tests
There is a test file you can use to play with the class.

> Modify the file `json2html.test.php` and run it from CLI.

```bash
php -f json2html.test.php

Received:
string(152) "{"<>":"div","class":"${class}", "id":"${id}","html":[{"<>":"img", "src":"${src}","alt":"${alt}"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"}]}"
string(150) "[{"class":"card"}, {"id":"5d0839d3c5824"}, {"src":"https://picsum.photos/id/767/400?random=5d0839d3c5864"}, {"alt":"this is our logo"}, {"name":"Jo"}]"

Converted:
string(166) "<div class="card" id="5d0839d3c5824"><img src="https://picsum.photos/id/767/400?random=5d0839d3c5864" alt="this is our logo"><p>Hi Jo! Welcome to json2html!</p></div>"
```

> Arguments are not supported yet.

## Python version
Just include the file `json2html.py` into your code.

```python
import json2html

# your code
```

And use it that way:

```python
import json2html

payload = '{"<>":"div","class":"${class}", "id":"${id}","html":[{"<>":"img", "src":"${src}","alt":"${alt}"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"}]}'

data = '[{"class":"card"},{"id":"element_id"},{"src":"https://picsum.photos/id/82/400?random=54654654654"},{"alt":"this is our logo"},{"name":"Jo"}]'

# Apply transform to get HTML output
print(json2html.transform(payload, data)) # Payload, Data, Debug (True | False)
```

### Tests
There is a test file you can use to play with the class.

> Modify the file `json2html.test.py` and run it from CLI.

```bash
python3 json2html.test.py

************
* CLI Mode *
************

Received:
 {"<>":"div","class":"${class}", "id":"${id}","html":[{"<>":"img", "src":"${src}","alt":"${alt}"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"}]}
[{'class': 'card'}, {'id': 'element_id'}, {'src': 'https://picsum.photos/id/82/400?random=54654654654'}, {'alt': 'this is our logo'}, {'name': 'Jo'}]

Converted:
 <div class="card" id="element_id"><img src="https://picsum.photos/id/82/400?random=54654654654" alt="this is our logo"><p>Hi Jo! Welcome to json2html!</p></div>
```

## Supported markup
Each versions support the spec bellow:

### Supported `tag` identifiers
It can handle both `{"<>":"div"}` or `{"tag":"div"}`.

### Support most common `HTML` attributes
Example 1:
```json
{"<>":"div","class":"css_class","id":"html_id"}
```
Gives:
```html
<div class="css_class" id="html_id"></div>
```
Example 2:
```json
{"<>":"img","alt":"alternative text","src":"image_src"}
```
Gives:
```html
<img alt="alternative text" src="image_src">
```
Example 3:
```json
{"<>":"a","href":"https://example.com","target":"_blank"}
```
Gives:
```html
<a href="https://example.com" target="_blank"></a>
```

### Support `text` and `HTML` encoding
Sample text:
```json
{"<>":"p","text":"my new paragraph."}
```
Gives:
> will be text encoded and HTML tags stripped and HTML entities decoded
```html
<p>my new paragraph.</p>
```

Sample HTML:
```json
{"<>":"p","html":"<code>will be converted into HTML entitites</code>"}
```
Gives:
> will be HTML encoded and HTML tags conserved
```html
<p>&lt;code&gt;will be converted into HTML entities&lt;/code&gt;</p>
```

### Support for `child` elements included
You can use `child`, `children` or `html` to define child elements.

With an image as child:
```json
{"<>":"a","href":"https://example.com","target":"_blank","html":[{"<>":"img","alt":"alternative text","src":"image_src"}]}
```
Gives:
```html
<a href="https://example.com" target="_blank"><img alt="alternative text" src="image_src"></a>
```

## Contribute
Feel free to contribute by openning issues and writing pull requests :grin:
