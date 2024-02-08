#!/usr/bin/env python3

"""
Generate ready-to-use headers for a web request with the least chance of
being blocked by anti-scraping techniques applied by websites. The
headers are based on the most common headers of browsers and operating
systems, and are ordered in the right way (servers check for that).
The inspect_headers.py file contains a Flask app to validate which
headers your browser or scraper sends.

# Import the package.
import simple_header as sh

# Get a Header instance with a random mobile user agent to scrape URL.
header = sh.get(url="https://www.example.com", mobile=True)

# Access the ready-to-use header dict and single header values:
header.dict
>> {'User-Agent': 'Mozilla/5.0 ...', 'Host': 'www.example.org',
'Connection': 'keep-alive', ...}

header.connection >> 'keep-alive'
header.user_agent.string >> 'Mozilla/5.0 ...'
header.user_agent.os >> 'Windows'

# Get a list of 10 Header instances sorted by plausibility with
# different seeds/header combinations, but the same given user agent:
sh.get_list(url="https...", num=10, user_agent="Mozilla/5...")
>> [Header(...), Header(...), ...]

# Get a ready-to-use header dict with overwritten language detection
# from TLD (.com = 'en-US' -> 'de-DE'). The seed of 3 will give the
# third most plausible header combination to avoid detection:
sh.get_dict(url="https...com", language="de-DE", seed=3)
>> {'User-Agent': 'Mozilla/5.0 ...', 'Host': 'www.example.com', ...}

# Fetch the two most common mobile user agent instances (see the README
# of simple-useragent for full documentation):
sh.sua.get(num=2, shuffle=False, mobile=True)
>> [UserAgent('Mozilla/5.0 (iPhone ...'), UserAgent('Mozilla/5.0  ...')]

sh.sua.get_ua()[0].string >> 'Mozilla/5.0 (Windows NT ...'
sh.sua.get_ua()[0].os >> 'Windows'
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "simple-header@lennolium.dev"
__license__ = "GNU GPLv3"
__version__ = "0.1.0"
__date__ = "2024-02-07"
__status__ = "Development"
__github__ = "https://github.com/Lennolium/simple-header"

# Imports.
from .core import Header, get, get_dict, get_list, sua
