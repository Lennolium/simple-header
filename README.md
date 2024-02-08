<!--- Logo -->

<div align="center">  
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Lennolium/simple-header/main/img/banner_dark.png" width="700vw">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Lennolium/simple-header/main/img/banner_light.png" width="700vw">
  <img alt="Application Banner" src="https://raw.githubusercontent.com/Lennolium/simple-header/main/img/banner_light.png" width="700vw">
</picture>
</div>
<br>

<!--- Badges -->

<div align="center"> 
  <a href="https://github.com/Lennolium/simple-header/branches" > 
    <img src="https://img.shields.io/github/last-commit/Lennolium/simple-header?label=Last%20Updated&color=orange" alt="last updated" >
  <a></a>  
   <a href="https://app.codacy.com/gh/Lennolium/simple-header/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade" > 
    <img src="https://app.codacy.com/project/badge/Grade/747e8fea69394b10a1f4627babddcf4f" alt="code quality" >
    <a></a>
   <a href="https://github.com/Lennolium/simple-header/commits/main" > 
    <img src="https://img.shields.io/github/commit-activity/m/Lennolium/simple-header?label=Commit%20Activity&color=yellow" 
alt="commit activity" >
     <a></a>
  <a href="https://github.com/Lennolium/simple-header/releases" > 
    <img src="https://img.shields.io/badge/Version-0.1.0-brightgreen" 
alt="stable version" >
     <br>
  <a href="https://github.com/Lennolium/simple-header/issues" > 
    <img src="https://img.shields.io/github/issues-raw/Lennolium/simple-header?label=Open%20Issues&color=critical" alt="open issues" >
  <a href="https://github.com/Lennolium/simple-header/issues?q=is%3Aissue+is%3Aclosed" > 
    <img src="https://img.shields.io/github/issues-closed-raw/Lennolium/simple-header?label=Closed%20Issues&color=inactive" alt="closed issues" > 
     <a href="https://pepy.tech/project/simple-header" > 
    <img src="https://static.pepy.tech/badge/simple-header" alt="pypi downloads" >
  <a href="https://github.com/Lennolium/simple-header/blob/main/LICENSE" > 
    <img src="https://img.shields.io/github/license/Lennolium/simple-header?label=License&color=blueviolet" alt="License" > 
  <a></a> </a> </a> </a> </a> </a> </a> </a> </a>
</div>

<!--- Title Line -->

<div align="center">
  <h1></h1> 
</div>

<!--- Description -->

<div align="center">
Generate ready-to-use headers for a web request with the least chance of
being blocked by anti-scraping techniques applied by websites. The
headers are based on the most common headers sent by browsers and operating
systems, and are ordered in the right way (servers check for that, even if the web standards say it
should not be considered). <br><br>

[![Donate](https://img.shields.io/badge/Donate-Paypal-blue?style=flat-square&logo=paypal)](https://www.paypal.me/smogg)
[![BuyMeACoffee](https://img.shields.io/badge/Buy%20me%20a-Coffee-f5d132?style=flat-square&logo=buymeacoffee)](https://buymeacoffee.com/lennolium)
</div>
<div align="center">
  <h3></h3>  
    </div>     
&nbsp;

<!--- Table of contents -->

## Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Quickstart](#quickstart)
  - [Advanced Usage](#advanced-usage)
  - [Settings and Parameters](#settings-and-parameters)
- [Development](#development)
- [Contributors](#contributors)
- [Credits](#credits)
- [License](#license)

&nbsp;

<!--- Features -->

## Features

- __Authentic:__ All header values, combinations and their ordering are `verified to work` with most web servers.
- __Powerful:__ Pass your own user agent in or use the convenience functions to get common, real-world user agents. 
- __Wide Support:__ Almost `all user agents supported`: Windows, macOS, Linux, Android and iOS: Google Chrome, Firefox, Safari, Edge, Opera, Whale and QQ.
- __Lightweight:__ Designed to consume minimal system resources and optimized for performance.
- __Simple:__ Easy to use and understand with a clean and simple API.
- __Compatible:__ Supports `Python 3.8 and above`. Runs on Windows, macOS and Linux.
- __Ready-to-use:__ It generates headers for direct use in web requests, so you can focus on your project.
- __Open Source:__ Provides transparency and allows community contributions for continuous development.

&nbsp;

<!--- Installation -->

## Installation

Just install the package from [PyPi](https://pypi.org/project/simple-header/) using pip:

   ```bash
    pip install simple-header
   ```

&nbsp;

<!--- Usage -->

## Usage

#### Quickstart

Just import the package and use the convenience function.
   ```python
    import simple_header as sh

    sh.get_dict(url="https://www.example.com/cat/pics.html")
    # {'User-Agent': 'Mozilla/5.0 ...', 'Host': 'www.example.com', 'Connection': 'keep-alive', ...}
   ```
&nbsp;

#### Advanced Usage

Import the package and use the full-fledged `get()` function. For detailed explanation of function parameters, please see [Settings and Parameters](#settings-and-parameters).
   ```python
    import simple_header as sh

    # Get a Header instance with a random mobile user agent to scrape the desired url.
    header = sh.get(url="https://www.example.com/cat/pics.html", mobile=True)
    header.dict
    # {'User-Agent': 'Mozilla/5.0 ...', 'Host': 'www.example.org', 'Connection': 'keep-alive', ...}
    
    # Access more attributes of the Header instance (just a few examples).
    header.connection  # 'keep-alive'
    header.referer  # 'https://www.example.com'  <- url without path
    header.user_agent.string  # 'Mozilla/5.0 ...'  <- randomly chosen user agent
    header.user_agent.os  # 'Windows'
    
    # Overwrite auto language detection (.com = 'en-US' -> 'de-DE') and set custom seed.
    header = sh.get(url="https://www.example.com/cat/pics.html", language="de-DE",seed=3)
    header.referer  # 'https://www.web.de/'  <- referer from pool of common german websites
    header.accept_language  # 'de-DE,de;q=0.5'  <- language set to German
    
    sh.get(url="https...com", user_agent="Mozilla/5.0 ...")  # Header instance with given user agent string.
    # Header('Mozilla/5.0 ...', 'https...com', 'keep-alive', ...)
    
    ua = sh.sua.get(num=2, mobile=True)  # List of 2 the two most common mobile user agent as UserAgent instance.
    sh.get(url="https...com", user_agent=ua[0])  # Header instance with the previously fetched UserAgent instance passed.
    # Header('Mozilla/5.0 ...', 'https...com', 'keep-alive', ...)
   ```
&nbsp;

You can also use get more than one Header instance at once with the `get_list()` function. 
The `get_dict()` function returns a dictionary with the headers directly usable in a request.
   ```python
    # Get a list of 10 Header instances, each with the passed user agent string.
    sh.get_list(url="https...com", user_agent="Mozilla/5.0 ...", num=10)
    # [Header(...), Header(...), ...]
    
    sh.get_dict(url="https://www.example.com/cat/pics.html") # Dictionary with just the headers.
    # {'User-Agent': 'Mozilla/5.0 ...', 'Host': 'www.example.com', 'Connection': 'keep-alive', ...} 
   ```
&nbsp;

Fetching User Agents. For full explanation check the [simple-useragent](https://github.com/Lennolium/simple-useragent) package.
   ```python
    # Fetch a specified number of random mobile user agent instances.
    sh.sua.get(num=2, shuffle=True, mobile=True)
    # [UserAgent('Mozilla/5.0 (iPhone ...'), UserAgent('Mozilla/5.0 (iPhone; ...')]

    sh.sua.get_list(force_cached=True)  # List of all available desktop user agents as strings.
    # ['Mozilla/5.0 ...', 'Mozilla/5.0 (iPhone ...', 'Mozilla/5.0 (iPhone ...', ...]
     
    sh.sua.get_dict()  # Dictionary with all desktop and mobile user agents.
    # {'desktop': ['Mozilla/5.0 ...', ...] 'mobile': ['Mozilla/5.0 (iPhone ...', ...]}
   ```  
&nbsp;

The UserAgent instance offers attributes for the user agent properties. You can also access the properties with dictionary syntax.
   ```python
    # Parse a custom string directly to the UserAgent class and access its attributes.
    obj = sh.sua.parse('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    obj.string  # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit ...'
    obj.browser  # 'Chrome', 'Firefox', 'Safari', 'Edge', 'IE', 'Opera', 'Whale', 'QQ Browser', 'Samsung Browser', 'Other'
    obj.browser_version  # '110', '109', '537', ...
    obj.browser_version_minor  # '0', '1', '36', ...
    obj['os']  # 'Windows', 'macOS', 'Linux', 'Android', 'iOS', 'Other'
    obj['os_version']  # '10', '7', '11', '14', ...
    obj['os_version_minor']  # '0', '1', '2', ...
    obj['mobile']  # True / False
   ```
&nbsp;

#### Settings and Parameters

The functions can take the following parameters:

- __url:__ The url of the website you want to scrape.
- __language:__ The language of the website you want to scrape or where the request is made from (default: _None_ = auto-detect).
- __user_agent:__ A custom user agent string or a UserAgent instance to use for header generation (default: _None_ = random user agent).
- __mobile:__ If no `user_agent` is passed: Generate a mobile or desktop user agent (default: _False_ = desktop).
- __seed:__ The random seed for referer selection and header value combinations (default: _None_ = most plausible values chosen, max: _720_).
- __num:__ The number of Header instances to fetch only for `get_list` method (default: _10_, max: _720_).

&nbsp;

> __Notes:__
> 
> - The `src/simple_header/inspect_headers.py` file contains a commented-out Flask app to validate which headers your browser or scraper sends.
> - The language auto-detection is based on the top-level domain of the url. You can overwrite it with the `language` parameter, by giving it a language (e.g. _'de-DE'_) or a country code (e.g. _'de'_). Fallback for unknown or non-country domains (.org, .dev, ...) is _'en-US'_.
> - For each language there is a pool of common websites, which are used to get a plausible referer. Also, we use the url to scrape without the path as referer (e.g. 'https://www.example.com/cat/pics.html' -> 'https://www.example.com'). The referer is used to make the request look more realistic, as it seems like the user is browsing between different pages of the website.
> - The `seed` parameter is used to set the random seed for referer selection and header values (if multiple are available). This is useful if your request got blocked by the server, so you try again with another seed. There are around 720 different combinations/seeds possible.
> - The order of the headers is important, as most servers and bot-detectors check for that, even if the web standards say it should not be considered. I _manually tested_ for every browser and OS which headers are sent and in which order.

&nbsp;

<!--- Development -->

## Development

As an open-source project, I strive for transparency and collaboration in my development process. I greatly 
appreciate any contributions members of our community can provide. Whether you are fixing bugs, proposing features, 
improving documentation, or spreading awareness - your involvement strengthens the project. Please review the 
[code of conduct](https://github.com/Lennolium/simple-header/blob/main/.github/CODE_OF_CONDUCT.md) to understand how we work together 
respectfully.

- __Bug Report:__ If you are experiencing an issue while using the package, please [create an issue](https://github.com/Lennolium/simple-header/issues/new/choose).
- __Feature Request:__ Make this project better by [submitting a feature request](https://github.com/Lennolium/simple-header/discussions/new?category=feature-requests).
- __Documentation:__ Improve our documentation by [adding a wiki page](https://github.com/Lennolium/simple-header/wiki).
- __Community Support:__ Help others on [GitHub Discussions](https://github.com/Lennolium/simple-header/discussions).
- __Security Report:__ Report critical security issues via our [template](https://github.com/Lennolium/simple-header/blob/main/.github/SECURITY.md).

&nbsp;

<!-- Contributors -->

## Contributors

Thank you so much for giving feedback, implementing features and improving the code and project!

<a href = "https://github.com/Lennolium/simple-header/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=Lennolium/simple-header" alt="Contributors"/> 
</a>

&nbsp;

<!--- Credits -->

## Credits

Full credits are in the [ACKNOWLEDGMENTS](https://github.com/Lennolium/simple-header/blob/main/ACKNOWLEDGMENTS) file.

&nbsp;

<!--- License -->

## License

Provided under the terms of the [GNU GPL3 License](https://www.gnu.org/licenses/gpl-3.0.en.html) © Lennart Haack 2024.

See [LICENSE](https://github.com/Lennolium/simple-header/blob/main/LICENSE) file for details.
For the licenses of used third party libraries and software, please refer to the [ACKNOWLEDGMENTS](https://github.com/Lennolium/simple-header/blob/main/ACKNOWLEDGMENTS) file.

