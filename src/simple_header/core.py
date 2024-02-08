#!/usr/bin/env python3

"""
core.py: Responsible for the core functionality of the package.

This module contains the main classes and functions for the package,
which are responsible for parsing at least a URL and returning the
headers for a request to scrape the website with the least chance of
being blocked by anti-scraping techniques. You can also pass a user
agent string or, for more granular browser- and os-specific headers, an
object (simple-useragent:  https://pypi.org/project/simple-useragent/).
If you do not pass a user agent, a random one from the simple-useragent
package is used, based on most common user agents. If you need a mobile
user agent, you have to set the mobile parameter. For country-specific
headers, we auto-detect the language from the TLD of the url. If you
want to overwrite it, you can pass the ISO language code (e.g. 'en-US',
'en-AU', 'de-DE', ...). The seed is used for getting different header
value combinations with reproducible results. Maximal 720 different
header value combinations are possible. I recommend you start by using
the get_list function with num of 10 to get a list of 10 Header
instances with the same user agent but different seeds/header
combinations, ordered by their plausibility of being accepted as
legitimate browser by the server. Each Header instance has a dictionary
with the headers as key-value pairs in the right ordering (servers check
for that, even if the web standards say it should not be important),
ready to use in a request by using the instances dict attribute or
__dict__ method. The modules get_dict function directly returns a single
ready to use dictionary with the headers for a request. The inspect.py
file contains a Flask app to validate which headers your browser sends.
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
import json
import logging
import os.path
import pathlib
import random
import re

import simple_useragent as sua
import tldextract
import validators

from . import exceptions

# Logging.
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class Header:
    """
    Class to generate headers for a request with right orderings and
    values to avoid anti-scraping techniques applied by websites.
    """

    def __init__(
            self,
            url: str,
            language: str = None,
            user_agent: sua.UserAgent | str = None,
            mobile: bool = False,
            seed: int = None,
            ) -> None:
        """
        Initializes the Header class.

        :param url: The url to scrape.
        :type url: str
        :param language: Language of the website or where the request is
            made from. Automatically detected from the TLD of the url.
            Used for generating referer and accept-language  headers.
            Overwrite it by passing the ISO language code (e.g. 'en-US',
            'en-AU', 'de-DE', ...).
        :type language: str
        :param user_agent: The user agent to use for the request.
            If None, a random user agent is generated.
        :type user_agent: sua.UserAgent | str | None
        :param mobile: If the request should look like it was made from
            a mobile device.
        :type mobile: bool
        :param seed: Seed for random headers values (if multiple values
            are available). If None, the first and most common value is
            used.
        :type seed: int
        """

        # Input and class parameters.
        self.url = None
        self.language = None
        self.mobile = None
        self.seed = None

        # Header values.
        self.host = None
        self.connection = None
        self.cache_control = None
        self.sec_ch_ua = None
        self.sec_ch_ua_mobile = None
        self.sec_ch_ua_platform = None
        self.upgrade_insecure_requests = None
        self.user_agent = None
        self.accept = None
        self.sec_fetch_site = None
        self.sec_fetch_mode = None
        self.sec_fetch_dest = None
        self.sec_fetch_user = None
        self.referer = None
        self.accept_encoding = None
        self.accept_language = None

        # Output dictionary.
        self.dict = None

        # Validate all input parameters.
        (self.url,
         self.language,
         self.user_agent,
         self.mobile) = self.__validations(
                url=url,
                language=language,
                user_agent=user_agent,
                mobile=mobile
                )
        self.seed = seed

        # Generate the header values, save them to the instance
        # attributes and combine them into a dictionary (self.dict).
        # We set __internal=True to not validate the inputs again.
        self.generate(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                seed=self.seed,
                _internal=True
                )

    def __dict__(self) -> dict[str, str]:
        """
        Returns the browser headers in a dictionary, ready to use for a
        request.

        :return: The headers as a dictionary.
        :rtype: dict[str, str]
        """
        return self.dict

    def __str__(self) -> str:
        """
        Returns the Header instance as a readable string seperated with
        commas, whitespaces and line breaks.

        :return: The Header instance as formatted string.
        :rtype: str
        """

        return "\n".join(
                f"{key}: {value}," for key, value in self.dict.items()
                )

    def __repr__(self) -> str:
        """
        Returns the Header instance as a representation for fast
        reconstruction.

        :return: The Header instance as a shortened representation.
        :rtype: str
        """

        return (f"{self.__class__.__name__}(url={self.url!r}, "
                f"language={self.language!r}, "
                f"user_agent={self.user_agent.string!r}, "
                f"mobile={self.mobile!r})")

    def __eq__(self, other) -> bool:
        """
        Returns True if the user agent strings are equal.

        :param other: The other Header instance to compare.
        :type other: Header
        :return: True if Header dicts are equal.
        :rtype: bool
        """

        if not isinstance(other, self.__class__):
            raise TypeError(
                    f"Can not compare {self.__class__.__name__} with other "
                    f"types than {self.__class__.__name__}."
                    )

        return self.dict == other.dict

    def __getitem__(self, item):
        """
        Returns the value of the given item.

        :param item: The item to get the value from.
        :type item: str
        :return: The value of the given item.
        :rtype: str
        """

        if hasattr(self, item.lower().replace("-", "_")):
            return getattr(self, item.lower().replace("-", "_"))
        else:
            raise AttributeError(
                    f"'{self.__class__.__name__}' object has no attribute '"
                    f"{item}'."
                    )

    @staticmethod
    def __load_json(
            file_name: str
            ) -> json:
        """
        Load a json file from the 'data' folder.

        :param file_name: The name of the json file.
        :type file_name: str
        :return: The json file as a dictionary.
        :rtype: json
        """

        fp = pathlib.Path(os.path.dirname(__file__),
                          "data",
                          file_name
                          )

        # Open templates from json file.
        try:
            with open(fp, "r") as fh:
                return json.load(fh)

        except FileNotFoundError as e:
            LOGGER.error(f"Could not find template file, that is shipped"
                         f"with the package! Verify that the file exists "
                         f"and if it does, report the issue please.\n"
                         f"{str(e.__class__.__name__)}: {str(e)}"
                         )
            raise exceptions.TemplateNotFoundError(
                    f"Could not find template file, that is shipped"
                    f"with the package! Verify that the file exists "
                    f"and if it does, report the issue please.\n"
                    f"{str(e.__class__.__name__)}: {str(e)}"
                    )

    def __detect_language(
            self,
            url: str,
            ) -> str:
        """
        Detect the language of the website from the TLD of the passed
        url. If the TLD is not in the referer json, we fall back to
        'com'.

        :param url: The url to scrape.
        :type url: str
        :return: The language code of the website.
        :rtype: str
        """

        tld = tldextract.extract(url).suffix
        referer_json = self.__load_json("referer_templates.json")

        # Sanitize and format TLD input for referer.
        if tld not in referer_json.keys():
            LOGGER.warning(
                    f"Could not auto-detect language for TLD '{tld}'! "
                    f"Falling back to to standard language 'en-US'."
                    )
            tld = "com"

        return referer_json[tld][0]

    def __check_language(
            self,
            url: str,
            language: str = None,
            ) -> str:
        """
        Check if the passed language code is supported and return the
        language code in the right format. If no language code is
        passed, we detect the language from the TLD of the url.

        :param url: The url to scrape.
        :type url: str
        :param language: The language code to check and format.
        :type language: str
        :return: The validated language code in the right format.
        :rtype: str
        """

        referer_json = self.__load_json("referer_templates.json")

        # No language code passed -> we detect language from the TLD.
        if not language:
            return self.__detect_language(url=url)

        # Language code passed -> we check if it is in the referer json.
        for value in referer_json.values():
            # Exact match: 'en-US' -> 'en-US'.
            if language.lower() == value[0].lower():
                return value[0]

            # Language code without country code: 'en' -> 'en-US'.
            elif language.lower() == value[0][:2].lower():
                return value[0]

            # No dash in language code: 'enUS' -> 'en-US'.
            elif language.lower() == value[0].replace("-", "").lower():
                return value[0]

        # Language code not recognized or supported.
        LOGGER.warning(
                f"Language code '{language}' is not recognized or "
                f"unsupported! Falling back to default language "
                f"'en-US'."
                )
        return "en-US"

    @staticmethod
    def __check_user_agent(
            user_agent: sua.UserAgent | str | None,
            mobile: bool = False,
            ) -> sua.UserAgent | None:
        """
        Check if the user agent is a string and parse it to a UserAgent
        object. Passed UserAgent instances get returned without change.
        If no user agent is passed, a random one is generated.

        :param user_agent: The user agent string or object.
        :type user_agent: str | sua.UserAgent | None
        :param mobile: If the request should look like it was made from
            a mobile device. Only used if no user agent is passed.
        :type mobile: bool
        :return: The user agent object.
        :rtype: sua.UserAgent
        """

        # Validate user agent object type.
        if isinstance(user_agent, sua.UserAgent):
            return user_agent

        # If string is passed, we parse it to an UserAgent object.
        elif isinstance(user_agent, str):
            return sua.parse(user_agent)

        elif user_agent is None:
            LOGGER.info("No user agent passed. Generating a random one.")
            return sua.get(num=1, shuffle=True, mobile=mobile)[0]

        # If an invalid user_agent type is passed, we generate a random
        # user agent instance.
        else:
            LOGGER.warning(
                    f"User agent must be of type UserAgent or str. "
                    f"Generating a random user agent for you."
                    )
            return sua.get(num=1, shuffle=True, mobile=mobile)[0]

    def __validations(
            self,
            url: str,
            language: str,
            user_agent: sua.UserAgent | str,
            mobile: bool,
            ) -> tuple[str, str, sua.UserAgent, bool]:
        """
        Validate all input parameters and return them in the right
        format. If a wrong type or invalid value for the url is passed,
        an exception is raised.

        :param url: The url to scrape.
        :type url: str
        :param language: The language code to check and format.
        :type language: str
        :param user_agent: The user agent string or object.
        :type user_agent: str | sua.UserAgent
        :param mobile: If the request should look like it was made from
            a mobile device. Only used if no user agent is passed.
        :return: The validated input parameters.
        :rtype: tuple[str, str, sua.UserAgent, bool]
        """

        # Validate the passed url -> if not valid, return None.
        if not validators.url(url) or not isinstance(url, str):
            msg = (f"URL '{url}' is not a str or invalid! "
                   f"No {self.__class__.__name__} instance created. "
                   f"Valid example: 'https://www.example.com/site.html'.")
            LOGGER.error(msg)
            raise exceptions.InvalidURLError(msg)

        # Validate or convert the passed user agent. If no user agent is
        # passed, a random one is generated.
        user_agent = self.__check_user_agent(
                user_agent=user_agent,
                mobile=mobile
                )

        # Validate passed language code or auto-detect it from the tld,
        # if None is passed.
        language = self.__check_language(
                url=url,
                language=language
                )

        return url, language, user_agent, mobile

    @staticmethod
    def __host(
            url: str,
            ) -> str:
        """
        Extract the host from the url for use as host header.

        :param url: The url to scrape.
        :type url: str
        :return: The host of the url.
        :rtype: str
        """

        # Remove the protocol and path of the url.
        protocol = url.split("://", maxsplit=1)[0] if "://" in url else "https"
        return url.replace(f"{protocol}://", "").split("/")[0]

    def __referer(
            self,
            url: str,
            language: str,
            ) -> list[str]:
        """
        Generate a list of referers for the request. The referers are
        language specific and depend on the TLD of the url. We fetch
        them from a json file with most common referers for each TLD.
        The first referer is always the url without path (simulating
        a same page request from the same domain as the target url).

        :param url: The url to scrape.
        :type url: str
        :param language: The language code.
        :type language: str
        :return: A list of most common referers for the request.
        :rtype: list[str]
        """

        # TODO: Also use sub-paths of the url as referers:
        #   domain.com/category/car.html -> domain.com/category/

        referer_json = self.__load_json("referer_templates.json")

        # Create a list and add the url without path as first referer.
        referers = [f"{url.split("/")[0]}//{url.split("/")[2]}/"]

        # Use language to get the TLD from the referer json. Fallback to
        # 'com' if not found.
        tld = "com"
        for key in referer_json.keys():
            if language.lower() == referer_json[key][0].lower():
                tld = key
                break

        # Add the referers from the json file, but skip the first entry,
        # as it is the language (e.g. 'en-US').
        referers.extend(referer_json.get(tld, [])[1:])

        return referers

    @staticmethod
    def __upgrade_insecure_requests(
            url: str,
            ) -> str:
        """
        Check if the url is a http or https request and return the
        corresponding value for the upgrade-insecure-requests header.

        :param url: The url to scrape.
        :type url: str
        :return: '1' if the url is a https request, '0' if it is http.
        :rtype: str
        """

        return "0" if url.startswith("http://") else "1"

    @staticmethod
    def __sec_ch_ua_chromium(
            user_agent: sua.UserAgent,
            ) -> str:
        """
        Extract the Chromium version from the user agent string.

        :param user_agent: The user agent object.
        :type user_agent: sua.UserAgent
        :return: The Chromium version or the browser version as
            fallback.
        :rtype: str
        """

        version = re.search(r'Chrome/(\d+)\.\d+\.\d+\.\d+', user_agent.string)
        return version.group(1) if version else user_agent.browser_version

    def __sec_ch_ua(
            self,
            ua_obj: sua.UserAgent,
            ) -> (tuple[str, str, str] |
                  tuple[None, None, None]):
        """
        Generate the Sec-Ch-Ua headers for Chrome and Chromium based
        browsers. For other browsers we return None.

        :param ua_obj: Pass the user agent object.
        :type ua_obj: sua.UserAgent
        :return: A tuple with the Sec-Ch-Ua, Sec-Ch-Ua-Mobile and
            Sec-Ch-Ua-Platform or None for unsupported browsers and os.
        :rtype: tuple[list[str], list[str], list[str]] |
            tuple[None, None, None]
        """

        # IE, Firefox and Safari do not send Sec-Ch-Ua headers.
        if ua_obj.browser in ["Safari", "Firefox", "IE"]:
            return None, None, None

        # Always the same for all browsers.
        sec_ch_ua_mobile = f"?{int(ua_obj.mobile)}"
        sec_ch_ua_platform = ua_obj.os

        # For Chrome-based browsers we need to extract Chromium version.
        ua_chromium_version = self.__sec_ch_ua_chromium(ua_obj)

        # Browser specific sec-ch-ua string.
        # Opera.
        if ua_obj.browser == "Opera":
            sec_ch_ua = (
                    f'"Not_A Brand";v="8", '
                    f'"Chromium";v="{ua_chromium_version}", '
                    f'"Opera";v="{ua_obj.browser_version}"')

        # Edge.
        elif ua_obj.browser == "Edge":
            sec_ch_ua = (
                    f'"Not A(Brand";v="99", '
                    f'"Microsoft Edge";v="{ua_obj.browser_version}", '
                    f'"Chromium";v="{ua_chromium_version}"')

        # Whale.
        elif ua_obj.browser == "Whale":
            sec_ch_ua = (
                    f'"Whale";v="{ua_obj.browser_version}", '
                    f'"Not-A.Brand";v="8", '
                    f'"Chromium";v="{ua_chromium_version}"')

        # QQ Browser.
        elif ua_obj.browser == "QQ Browser":
            sec_ch_ua = (
                    f'"Not A;Brand";v="{ua_obj.browser_version}", '
                    f'"Chromium";v="{ua_chromium_version}", '
                    f'"QQ Browser";v="{ua_obj.browser_version}"')

        # Samsung Browser.
        elif ua_obj.browser == "Samsung Browser":
            sec_ch_ua = (
                    f'"Not?A_Brand";v="{ua_obj.browser_version}", '
                    f'"Chromium";v="{ua_chromium_version}", '
                    f'"Samsung Browser";v="{ua_obj.browser_version}"')

        # Chrome, Chromium and fallback for others.
        else:
            sec_ch_ua = (
                    f'"Not A(Brand";v="99", '
                    f'"Chromium";v="{ua_chromium_version}", '
                    f'"Google Chrome";v="{ua_obj.browser_version}"')

        return sec_ch_ua, sec_ch_ua_mobile, sec_ch_ua_platform

    def generate(
            self,
            url: str,
            language: str = None,
            user_agent: sua.UserAgent | str = None,
            mobile: bool = False,
            seed: int = None,
            _internal: bool = False,
            ) -> dict[str, str]:
        """
        Generate headers for a request and save them to the instance
        attributes and combined into a dictionary. If no user agent is
        passed, a random one is generated. If no language is passed, we
        detect it from the TLD of the url.

        :param url: The url to scrape.
        :type url: str
        :param language: Language of the website or where the request is
            made from. If None, automatically detected from the TLD of
            the url. Used for generating referer and accept-language
            headers. Overwrite it by passing the ISO language code
            (e.g.'en-US','en-AU', 'de-DE', ...).
        :type language: str
        :param user_agent: The user agent to use for the request. If None,
            a random user agent is generated. If a string is passed, it
            is parsed to a UserAgent object.
        :type user_agent: sua.UserAgent | str
        :param mobile: If the request should look like it was made from
            a mobile device. Only used if no user agent is passed.
        :type mobile: bool
        :param seed: Seed for random headers values (if multiple values
            are available). If None, the first and most common value is
            used (max=720).
        :type seed: int
        :param _internal: If the function is called from inside the
            class. If True, we do not validate the inputs again.
        :type _internal: bool
        :return: The headers as a dictionary.
        :rtype: dict[str, str]
        """

        # Validate all input parameters. Except for internal func call.
        if not _internal:
            (self.url,
             self.language,
             self.user_agent,
             self.mobile,) = self.__validations(
                    url=url,
                    language=language,
                    user_agent=user_agent,
                    mobile=mobile,
                    )

        # Headers:
        # Domain to scrape without protocol and path.
        self.host = self.__host(url=self.url)
        self.connection = "keep-alive"
        self.cache_control = "max-age=0"
        # Sec-Ch-Ua headers only send by Chrome-based browsers.
        self.sec_ch_ua = self.__sec_ch_ua(ua_obj=user_agent)[0]
        self.sec_ch_ua_mobile = self.__sec_ch_ua(ua_obj=user_agent)[1]
        self.sec_ch_ua_platform = self.__sec_ch_ua(ua_obj=user_agent)[2]
        # SSL connection: '1', no SSL: '0'.
        self.upgrade_insecure_requests = self.__upgrade_insecure_requests(
                url=self.url
                )
        # Direct request: 'none', dynamic data request (XHR): 'none'.
        self.sec_fetch_site = ["none", "same-site"]
        # Direct request: 'navigate', XHR: 'cors' or 'same-origin'.
        self.sec_fetch_mode = ["navigate", "same-origin", "cors"]
        # Direct html request: 'document', XHR: 'empty'.
        self.sec_fetch_dest = ["document", "empty"]
        # Request made by user ('?1') or by script (omitted).
        self.sec_fetch_user = "?1"
        # Host url and language specific referer.
        self.referer = self.__referer(
                url=self.url,
                language=self.language,
                )
        # Sometimes 'br' is used to identify a scraper.
        self.accept_encoding = ["gzip, deflate", "gzip, deflate, br"]
        # Language of website or where the request is made from.
        self.accept_language = [
                f"{self.language},{self.language[:2]};q=0.5",
                f"{self.language},{self.language[:2]};q=0.9"]

        # Import header templates json and get the template for the current os
        # and browser.
        header_templates = self.__load_json("header_templates.json")
        header_template = header_templates[user_agent.os][user_agent.browser]

        # Assign the instance attributes values to the header template.
        for key in header_template:

            # The Accept header is defined in the template, we just need
            # to assign it to the instance attribute.
            if key == "Accept":
                self.accept = header_template[key]
                continue

            # For the user agent header we use the user agent string
            # from the user agent object.
            elif key == "User-Agent":
                header_template[key] = self.user_agent.string
                continue

            # We convert it to the right formatted name of the instance
            # attribute.
            else:
                attr = getattr(self, key.lower().replace("-", "_"))

            # The attribute is a list.
            if isinstance(attr, list):
                # Random element.
                if seed is not None:
                    random.seed(seed)
                    header_template[key] = random.choice(attr)

                else:
                    # First element.
                    header_template[key] = attr[0]

            # The attribute is a string.
            else:
                header_template[key] = attr

        self.dict = header_template

        return header_template


class Headers:
    """
    Class to generate headers for a request with right orderings and
    values to avoid anti-scraping techniques applied by websites.
    """

    def __init__(self) -> None:
        """
        Initializes the Headers class with static methods only.
        Nothing to initialize so far.
        """
        pass

    @staticmethod
    def get_dict(
            url: str,
            language: str = None,
            user_agent: str | sua.UserAgent = None,
            mobile: bool = False,
            seed: int = None,
            ) -> dict[str, str]:
        """
        Generate headers for a request with right orderings and values
        to avoid anti-scraping techniques applied by websites. The
        returned dictionary can be directly used in a request.

        :param url: The url to scrape.
        :type url: str
        :param language: Language of the website or where the request is
            made from. If None, automatically detected from the TLD of
            the url. Used for generating referer and accept-language
            headers. Overwrite it by passing the ISO language code
            (e.g.'en-US','en-AU', 'de-DE', ...).
        :type language: str
        :param user_agent: The user agent to use for the request. If None,
            a random user agent is generated. If a string is passed, it
            is parsed to a UserAgent object. If a UserAgent object is
            passed, it is used as is.
        :type user_agent: str | sua.UserAgent
        :param mobile: If the request should look like it was made from
            a mobile device.
        :type mobile: bool
        :param seed: Seed for random headers values (if multiple values
            are available). If None, the first and most common value is
            used (max=720).
        :type seed: int
        :return: The headers in a dictionary, ready to use in a request.
        :rtype: dict[str, str]
        """

        # Create a Header instance.
        header = Header(
                url=url,
                language=language,
                user_agent=user_agent,
                mobile=mobile,
                seed=seed,
                )

        # Return the headers as a dictionary.
        return header.dict

    @staticmethod
    def get_list(
            url: str,
            language: str = None,
            user_agent: str | sua.UserAgent = None,
            mobile: bool = False,
            num: int = 10,
            ) -> list[Header]:
        """
        Generate headers for a request with right orderings and values
        to avoid anti-scraping techniques applied by websites. In the
        returned list, are Header instances with different seeds for
        all possible header value combinations. The instances are
        ordered by their plausibility of being accepted as legitimate
        browser by the server.

        :param url: The url to scrape.
        :type url: str
        :param language: Language of the website or where the request is
            made from. If None, automatically detected from the TLD of
            the url. Used for generating referer and accept-language
            headers. Overwrite it by passing the ISO language code
            (e.g.'en-US','en-AU', 'de-DE', ...).
        :type language: str
        :param user_agent: The user agent to use for the request. If None,
            a random user agent is generated. If a string is passed, it
            is parsed to a UserAgent object. If a UserAgent object is
            passed, it is used as is.
        :type user_agent: str | sua.UserAgent
        :param mobile: If the request should look like it was made from
            a mobile device.
        :type mobile: bool
        :param num: Number of header instances to generate and append to
            the list (max=720, default=10).
        :type num: int
        :return: The headers in a dictionary, ready to use in a request.
        :rtype: dict[str, str]
        """

        headers = []

        for i in range(min(num, 720)):
            header = Header(
                    url=url,
                    language=language,
                    user_agent=user_agent,
                    mobile=mobile,
                    seed=i,
                    )

            headers.append(header)

        return headers

    @staticmethod
    def get(
            url: str,
            language: str = None,
            user_agent: str | sua.UserAgent = None,
            mobile: bool = False,
            seed: int = None,
            ) -> Header:
        """
        Generate headers for a request with right orderings and values
        to avoid anti-scraping techniques applied by websites. It
        returns a single Header instance with the most plausibility to be
        accepted as legitimate browser by the server. With its
        attributes you can access each header value separately and get
        the ready to use header dictionary by its dict attribute or
        __dict__ method.

        :param url: The url to scrape.
        :type url: str
        :param language: Language of the website or where the request is
            made from. If None, automatically detected from the TLD of
            the url. Used for generating referer and accept-language
            headers. Overwrite it by passing the ISO language code
            (e.g.'en-US','en-AU', 'de-DE', ...).
        :type language: str
        :param user_agent: The user agent to use for the request. If None,
            a random user agent is generated. If a string is passed, it
            is parsed to a UserAgent object. If a UserAgent object is
            passed, it is used as is.
        :type user_agent: str | sua.UserAgent
        :param mobile: If the request should look like it was made from
            a mobile device.
        :type mobile: bool
        :param seed: Seed for random headers values (if multiple values
            are available). If None, the first and most common value is
            used (max=720).
        :type seed: int
        :return: A Header instance.
        :rtype: Header
        """

        header = Header(
                url=url,
                language=language,
                user_agent=user_agent,
                mobile=mobile,
                seed=seed,
                )

        return header


# Convenience functions.
get_dict = Headers.get_dict
get_list = Headers.get_list
get = Headers.get
