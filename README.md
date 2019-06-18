# JSON2HTML
JSON to HTML converter - It will follow the same spec as http://json2html.com/

## Available Versions
I wrote two versions:
 * a `PHP` version **(working)**
 * a `Python` version **(fix needed)**

## PHP version
Just include the file `json2html.php` into your code.

```php
require_once 'json2html.php';

# your code
```

And use it that way:

```php
require_once 'json2html.php';

/*
 *
 * Test payload
 *
 */

/* with data into markup */
// $payload = '{"<>":"div","class":"card", "id":"' . uniqid() . '","html":[{"<>":"img", "src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '","alt":"this is our logo"},{"<>":"p","text":"Hi {{name}}! Welcome to json2html!"}]}';

/* with some data into external object using {{x}} as marker + data in markup also */
// $payload = '{"<>":"div","class":"{{class}}", "id":"' . uniqid() . '","html":[{"<>":"img", "src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '","alt":"this is our logo"},{"<>":"p","text":"Hi {{name}}! Welcome to json2html!"}]}';

/* with some data into external object using ${x} as marker + data in markup also */
// $payload = '{"<>":"div","class":"${class}", "id":"' . uniqid() . '","html":[{"<>":"img", "src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '","alt":"this is our logo"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"}]}';

/* with all data into external object using ${x} as marker */
$payload = '{"<>":"div","class":"${class}", "id":"${id}","html":[{"<>":"img", "src":"${src}","alt":"${alt}"},{"<>":"p","text":"Hi ${name}! Welcome to json2html!"}]}';

/* won't work */
// $payload = ['x', 'y'];

/* won't work */
// $payload = new stdClass;

/*
 *
 * Test data
 *
 */

/* data sample 1 */
// $data = '[{"name":"Jo"}]';

/* data sample 2 */
// $data = '[{"class":"card"}, {"name":"Jo"}]';

/* data sample 3 */
$data = '[{"class":"card"}, {"id":"' . uniqid() . '"}, {"src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '"}, {"alt":"this is our logo"}, {"name":"Jo"}]';
// $data = '[{"id":"' . uniqid() . '"}, {"class":"card"}, {"src":"https://picsum.photos/id/' . mt_rand(0, 999) . '/400?random=' . uniqid() . '"}, {"alt":"this is our logo"}, {"name":"Jo"}]';

/* Apply transform to get HTML output */
json2html::transform($payload, $data, false); // Payload, Data, Debug (true | false)
```

### Supported `tag` identifiers
It can handle both `{"<>":"div"}` or `{"tag":"div"}`.

### Support most common `HTML` attributes
Example:
 * `{"<>":"div","class":"css_class","id":"html_id"}` gives `<div class="css_class" id="html_id"></div>`
 * `{"<>":"img","alt":"alternative text","src":"image_src"}` gives `<img alt="alternative text" src="image_src">`
 * `{"<>":"a","href":"https://example.com","target":"_blank"}` gives `<a href="https://example.com" target="_blank"></a>`

### Support `text` and `HTML` encoding
 * `{"<>":"p","text":"my new paragraph."}` *(will be text encoded and HTML tags stripped and HTML entities decoded)*
 * `{"<>":"p","html":"<code>will be converted into HTML entitites</code>"}` *(will be HTML encoded and HTML tags conserved)*

Will give:
 * `<p>my new paragraph.</p>`
 * `<p>&lt;code&gt;will be converted into HTML entities&lt;/code&gt;</p>`

### Support for `child` elements included
 * `{"<>":"a","href":"https://example.com","target":"_blank","html":[{"<>":"img","alt":"alternative text","src":"image_src"}]}`

Will give:
 * `<a href="https://example.com" target="_blank"><img alt="alternative text" src="image_src"></a>`

## Python version
More details once patched and finished.

## Contribute
Feel free to contribute by openning issues and writing pull requests :grin:
