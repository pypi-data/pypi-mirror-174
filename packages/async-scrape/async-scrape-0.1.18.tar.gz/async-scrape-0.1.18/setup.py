# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_scrape', 'async_scrape.libs', 'async_scrape.utils']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'PyPAC>=0.16.0,<0.17.0',
 'aiohttp>=3.8.3,<4.0.0',
 'nest-asyncio>=1.5.6,<2.0.0',
 'requests-html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'async-scrape',
    'version': '0.1.18',
    'description': 'A package designed to scrape webpages using aiohttp and asyncio. Has some error handling to overcome common issues such as sites blocking you after n requests over a short period.',
    'long_description': '# Async-scrape\n## _Perform webscrape asyncronously_\n\n[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)\n\nAsync-scrape is a package which uses asyncio and aiohttp to scrape websites and has useful features built in.\n\n## Features\n\n- Breaks - pause scraping when a website blocks your requests consistently\n- Rate limit - slow down scraping to prevent being blocked\n\n\n## Installation\n\nAsync-scrape requires [C++ Build tools](https://go.microsoft.com/fwlink/?LinkId=691126) v15+ to run.\n\n\n```\npip install async-scrape\n```\n\n## How to use it\nKey inpur parameters:\n- `post_process_func` - the callable used to process the returned response\n- `post_process_kwargs` - and kwargs to be passed to the callable\n- `use_proxy` - should a proxy be used (if this is true then either provide a `proxy` or `pac_url` variable)\n- `attempt_limit` - how manay attempts should each request be given before it is marked as failed\n- `rest_wait` - how long should the programme pause between loops\n- `call_rate_limit` - limits the rate of requests (useful to stop getting blocked from websites)\n- `randomise_headers` - if set to `True` a new set of headers will be generated between each request\n\n### Get requests\n```\n# Create an instance\nfrom async_scrape import AsyncScrape\n\ndef post_process(html, resp, **kwargs):\n    """Function to process the gathered response from the request"""\n    if resp.status == 200:\n        return "Request worked"\n    else:\n        return "Request failed"\n\nasync_Scrape = AsyncScrape(\n    post_process_func=post_process,\n    post_process_kwargs={},\n    fetch_error_handler=None,\n    use_proxy=False,\n    proxy=None,\n    pac_url=None,\n    acceptable_error_limit=100,\n    attempt_limit=5,\n    rest_between_attempts=True,\n    rest_wait=60,\n    call_rate_limit=None,\n    randomise_headers=True\n)\n\nurls = [\n    "https://www.google.com",\n    "https://www.bing.com",\n]\n\nresps = async_Scrape.scrape_all(urls)\n```\n\n### Post requests\n```\n# Create an instance\nfrom async_scrape import AsyncScrape\n\ndef post_process(html, resp, **kwargs):\n    """Function to process the gathered response from the request"""\n    if resp.status == 200:\n        return "Request worked"\n    else:\n        return "Request failed"\n\nasync_Scrape = AsyncScrape(\n    post_process_func=post_process,\n    post_process_kwargs={},\n    fetch_error_handler=None,\n    use_proxy=False,\n    proxy=None,\n    pac_url=None,\n    acceptable_error_limit=100,\n    attempt_limit=5,\n    rest_between_attempts=True,\n    rest_wait=60,\n    call_rate_limit=None,\n    randomise_headers=True\n)\n\nurls = [\n    "https://eos1jv6curljagq.m.pipedream.net",\n    "https://eos1jv6curljagq.m.pipedream.net",\n]\npayloads = [\n    {"value": 0},\n    {"value": 1}\n]\n\nresps = async_Scrape.scrape_all(urls, payloads=payloads)\n```\n\n### Response\nResponse object is a list of dicts in the format:\n```\n{\n    "url":url, # url of request\n    "req":req, # combination of url and params\n    "func_resp":func_resp, # response from post processing function\n    "status":resp.status, # http status\n    "error":None # any error encountered\n}\n```\n\n\n## License\n\nMIT\n\n**Free Software, Hell Yeah!**\n\n[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn\'t be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)\n\n   [dill]: <https://github.com/joemccann/dillinger>\n   [git-repo-url]: <https://github.com/joemccann/dillinger.git>\n   [john gruber]: <http://daringfireball.net>\n   [df1]: <http://daringfireball.net/projects/markdown/>\n   [markdown-it]: <https://github.com/markdown-it/markdown-it>\n   [Ace Editor]: <http://ace.ajax.org>\n   [node.js]: <http://nodejs.org>\n   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>\n   [jQuery]: <http://jquery.com>\n   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>\n   [express]: <http://expressjs.com>\n   [AngularJS]: <http://angularjs.org>\n   [Gulp]: <http://gulpjs.com>\n\n   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>\n   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>\n   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>\n   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>\n   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>\n   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>\n',
    'author': 'Robert Franklin',
    'author_email': 'cia05rf@gmail.com',
    'maintainer': 'Robert Franklin',
    'maintainer_email': 'cia05rf@gmail.com',
    'url': 'https://github.com/cia05rf/async-scrape/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
