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

- __Authentic:__ All header values, combinations and their order are verified to work with most web servers.
- __Powerful:__ Pass your own user agent in or use the convenience functions to get common, real-world user agents. 
- __Wide Support:__ Almost all user agents supported: Windows, macOS, Linux, Android and iOS: Google Chrome, Firefox, Safari, Edge, Opera, Whale and QQ.
- __Lightweight:__ Designed to consume minimal system resources and optimized for performance.
- __Simple:__ Easy to use and understand with a clean and simple API.
- __Compatible:__ Supports `Python 3.8 and above`. Runs on Windows, macOS and Linux.
- __Ready-to-use:__ It generates headers for direct use in web requests, and you can focus on your project.
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

Just import the package and use the convenience functions. For more advanced usage, you can initialize the class to set custom settings.

   ```python
    import simple_header as sh

    sh.get(num=2, mobile=True)  # List of the 2 most common mobile user agents (attributes explained below).
    # [UserAgent('Mozilla/5.0 (Android ...'), UserAgent('Mozilla/5.0 (iPhone; ...')]
    
    sh.get_list(shuffle=True, force_cached=True)  # Random list of available desktop user agents strings.
    # ['Mozilla/5.0 ...', 'Mozilla/5.0 (iPhone ...', 'Mozilla/5.0 (iPhone ...', ...]
    
    sh.get_dict()  # Dictionary with all desktop and mobile user agents.
    # {'desktop': ['Mozilla/5.0 ...', ...] 'mobile': ['Mozilla/5.0 (iPhone ...', ...]}
   ```
&nbsp;

#### Advanced Usage

Import the package and initialize the UserAgents class to set custom settings (optional, see [Settings and Parameters](#settings-and-parameters) for details).
   ```python
    import simple_header as sh

    simple_ua = sua.UserAgents(max_retries=3, timeout=5, cache_duration=86400, cache_location='example/path/to/folder')
   ```
&nbsp;

Fetching User Agents.
   ```python
    # Fetch a specified number of random mobile user agent instances (with settings from the class above).
    simple_ua.get(num=2, shuffle=True, mobile=True)
    # [UserAgent('Mozilla/5.0 (iPhone ...'), UserAgent('Mozilla/5.0 (iPhone; ...')]
   ```  
&nbsp;

You can also use the convenience functions to get user agents without initializing the class.
   ```python
    sua.get(num=2, mobile=True)  # List of the 2 most common mobile user agent (attributes explained below).
    # [UserAgent('Mozilla/5.0 (Android ...'), UserAgent('Mozilla/5.0 (iPhone; ...')]
    
    sua.get_list(force_cached=True)  # List of all available desktop user agents as strings.
    # ['Mozilla/5.0 ...', 'Mozilla/5.0 (iPhone ...', 'Mozilla/5.0 (iPhone ...', ...]
    
    sua.get_dict()  # Dictionary with all desktop and mobile user agents.
    # {'desktop': ['Mozilla/5.0 ...', ...] 'mobile': ['Mozilla/5.0 (iPhone ...', ...]}
   ```
&nbsp;

The instance offers attributes for the user agent properties.
   ```python
    # Parse a custom string directly to the UserAgent class and access its attributes.
    obj = sua.parse('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    obj.string  # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit ...'
    obj.browser  # 'Chrome', 'Firefox', 'Safari', 'Edge', 'IE', 'Opera', 'Whale', 'QQ Browser', 'Samsung Browser', 'Other'
    obj.browser_version  # '110', '109', '537', ...
    obj.browser_version_minor  # '0', '1', '36', ...

    # You can also access the attributes with square brackets.
    obj = sua.get(num=1, shuffle=True)[0]
    obj['os']  # 'Windows', 'macOS', 'Linux', 'Android', 'iOS', 'Other'
    obj['os_version']  # '10', '7', '11', '14', ...
    obj['os_version_minor']  # '0', '1', '2', ...
    obj['mobile']  # True / False
   ```
&nbsp;

#### Settings and Parameters

The functions can take the following parameters:

- __num:__ The number of user agents to fetch (default: _None_ = gets you all user agents available).
- __mobile:__ Fetch mobile or desktop user agents (default: _False_ = desktop).
- __shuffle:__ Whether to shuffle/randomize the order of user agents (default: _False_ = ordered by usage).
- __force_cached:__ Force the use of memory or file cached user agents (default: _None_ = fetches new user agents if cache is outdated, _False_ = always call the API, _True_ = always use the cache).

&nbsp;

You can set custom preferences when initializing the class with `UserAgents(...)`.

- __max_retries:__ The maximum number of retries to reach the API, before falling back to local cache (default: _3_).
- __timeout:__ The timeout in seconds for the API request (default: _5_).
- __cache_duration:__ The duration in seconds for the user agents to be cached (default: _86400_ = 1 day).
- __cache_location:__ The folder in which the user agents are cached, specific to the OS. You can see the default location with `UserAgents._cache_location`.

&nbsp;

> __Notes:__
> 
> - The user agents are cached locally to avoid unnecessary API calls, and are refreshed automatically every 24 hours.
> - During runtime the user agents are stored in memory and written to a cache file for persistence and performance.
> - Every time you invoke a simple-header function, it is automatically checked for outdated user agents.

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

