# JSON2HTML
JSON to HTML converter - It will follow the same spec as http://json2html.com/

## Available Versions
I wrote two versions:
 * a `PHP` version **working**
 * a `Python` version **fix needed**

### PHP version
Just include the file `json2html.php` into your code.

```php
require_once 'json2html.php'

# your code
```

And use it that way:

```php
require_once 'json2html.php'

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

### Python version
More details once patched and finished.

## Contribute
Feel free to contribute by openning issues and writing pull requests :grin:
