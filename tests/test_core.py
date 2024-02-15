#!/usr/bin/env python3

"""
test_core.py: Test core functionality of the simple-header package.

This file contains the test cases for the core functionality of the
simple-header package. It tests the Header and Headers classes
and their methods. It also tests the private methods of the Header
class. The tests are written using the unittest module. We try to cover
as many edge cases as possible to ensure the stability of the package.

The tests can be run with the following command:
    $ python -m unittest tests.test_core
"""
from __future__ import annotations

# Header.
__author__ = "Lennart Haack"
__email__ = "simple-header@lennolium.dev"
__license__ = "GNU GPLv3"
__version__ = "0.1.1"
__date__ = "2024-02-14"
__status__ = "Development"
__github__ = "https://github.com/Lennolium/simple-header"

# Imports.
import importlib
import io
import json
import logging
import unittest
from pathlib import Path
from unittest.mock import patch

import simple_header


class TestHeader(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.example.com"
        self.language = "en-US"
        self.mobile = False
        self.seed = 1
        self.intra_site_nav = True  # For always same referer.
        self.user_agent_string = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/110.0.0.0 Safari/537.36")
        self.user_agent = simple_header.sua.parse(self.user_agent_string)

        self.header = simple_header.Header(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                seed=self.seed,
                intra_site_nav=self.intra_site_nav
                )

        # Resulting header fields.
        self.host = 'www.example.com'
        self.connection = 'keep-alive'
        self.cache_control = 'max-age=0'
        self.sec_ch_ua = ('"Not A(Brand";v="99", "Chromium";v="110", "Google '
                          'Chrome";v="110"')
        self.sec_ch_ua_mobile = "?0"
        self.sec_ch_ua_platform = "macOS"
        self.upgrade_insecure_requests = "1"
        self.accept = (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,"
                "application/signed-exchange;v=b3;q=0.7")
        self.sec_fetch_site = "none"
        self.sec_fetch_mode = "navigate"
        self.sec_fetch_user = "?1"
        self.sec_fetch_dest = "document"
        self.accept_encoding = "gzip, deflate"
        self.accept_language = "en-US,en;q=0.5"

    def test_init(self):
        self.assertEqual(self.header.url, self.url)
        self.assertEqual(self.header.language, self.language)
        self.assertEqual(self.header.user_agent.string,
                         self.user_agent.string
                         )
        self.assertEqual(self.header.mobile, self.mobile)
        self.assertEqual(self.header.seed, self.seed)
        self.assertEqual(self.header.intra_site_nav, self.intra_site_nav)

    @patch('simple_header.core.Header._Header__validations')
    def test_init_calls_validations(self, mock_validations):
        mock_validations.return_value = (
                self.url, self.language, self.user_agent, self.mobile)
        header = simple_header.Header(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                seed=self.seed,
                intra_site_nav=self.intra_site_nav
                )
        mock_validations.assert_called_once_with(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile
                )

    @patch('simple_header.core.LOGGER')
    def test_validations_invalid_url(self, mock_logger):
        # Create a Header instance
        header = simple_header.Header(
                url="https://www.example.com",
                language="en-US",
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/110.0.0.0 Safari/537.36",
                mobile=False,
                seed=1,
                intra_site_nav=True
                )

        # Test with invalid URL
        invalid_url = "NotaValidUrl com"
        with self.assertRaises(simple_header.exceptions.InvalidURLError):
            header._Header__validations(
                    url=invalid_url,
                    language="en-US",
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X "
                               "10_15_7) AppleWebKit/537.36 (KHTML, "
                               "like Gecko) Chrome/110.0.0.0 Safari/537.36",
                    mobile=False,
                    )

        # Check if the logger error has been called
        mock_logger.error.assert_called_once()

    def test_dict(self):
        header = simple_header.Header(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                seed=self.seed,
                intra_site_nav=self.intra_site_nav,
                )

        header_dict = self.header.__dict__()
        self.assertIsInstance(header_dict, dict)
        self.assertEqual(header_dict['Host'], self.host)
        self.assertEqual(header_dict['Connection'], self.connection)
        self.assertEqual(header_dict['Cache-Control'], self.cache_control)
        self.assertEqual(header_dict['Sec-Ch-Ua'], self.sec_ch_ua)
        self.assertEqual(header_dict['Sec-Ch-Ua-Mobile'],
                         self.sec_ch_ua_mobile
                         )
        self.assertEqual(header_dict['Sec-Ch-Ua-Platform'],
                         self.sec_ch_ua_platform
                         )
        self.assertEqual(header_dict['Upgrade-Insecure-Requests'],
                         self.upgrade_insecure_requests
                         )
        self.assertEqual(header_dict['User-Agent'], self.user_agent_string)
        self.assertEqual(header_dict['Accept'], self.accept)
        self.assertEqual(header_dict['Sec-Fetch-Site'], self.sec_fetch_site)
        self.assertEqual(header_dict['Sec-Fetch-Mode'], self.sec_fetch_mode)
        self.assertEqual(header_dict['Sec-Fetch-User'], self.sec_fetch_user)
        self.assertEqual(header_dict['Sec-Fetch-Dest'], self.sec_fetch_dest)
        self.assertEqual(header_dict['Accept-Encoding'],
                         self.accept_encoding
                         )
        self.assertEqual(header_dict['Accept-Language'],
                         self.accept_language
                         )

    def test_str(self):
        header_str = str(self.header)
        self.assertIsInstance(header_str, str)

    def test_repr(self):
        header_repr = repr(self.header)
        self.assertIsInstance(header_repr, str)
        expected_repr = (f"Header(url={self.url!r}, language="
                         f"{self.language!r}, user_agent="
                         f"{self.user_agent.string!r}, "
                         f"mobile={self.mobile!r}, seed={self.seed}, "
                         f"intra_site_nav={self.intra_site_nav!r})")
        self.assertEqual(header_repr, expected_repr)

    def test_eq(self):
        # Create a second Header instance with the same attributes
        header_same = simple_header.Header(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                seed=self.seed,
                intra_site_nav=self.intra_site_nav
                )

        # Assert that the two Header instances are equal
        self.assertTrue(self.header == header_same)

        # Create a third Header instance with different attributes
        header_diff = simple_header.Header(
                url="https://www.different.com",
                language="fr-FR",
                user_agent=simple_header.sua.parse(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/58.0.3029.110 Safari/537.3"
                        ),
                mobile=True,
                seed=2,
                intra_site_nav=True
                )
        # Assert that the two Header instances are not equal
        self.assertFalse(self.header == header_diff)
        # Assert if wrong type is passed
        self.assertRaises(TypeError, header_same.__eq__, "mock object")

    def test_getitem(self):
        # Test getting an existing attribute
        self.assertEqual(self.header['url'], self.url)
        self.assertEqual(self.header['language'], self.language)
        self.assertEqual(self.header['user_agent'], self.user_agent)
        self.assertEqual(self.header['mobile'], self.mobile)
        self.assertEqual(self.header['seed'], self.seed)
        self.assertEqual(self.header['intra_site_nav'], self.intra_site_nav)

        self.assertEqual(self.header['Sec-ch-UA'], self.sec_ch_ua)

        with self.assertRaises(AttributeError):
            self.header['non_existing_attribute']

        # Test getting an attribute with wrong case
        self.assertEqual(self.header['URL'], self.url)

        # Test getting an attribute with special characters
        with self.assertRaises(AttributeError):
            self.header['uRl#*']

    @patch('simple_header.core.Header._Header__load_json')
    def test_load_json(self, mock_load_json):
        # Test loading an existing JSON file
        mock_load_json.return_value = {"key": "value"}
        result = self.header._Header__load_json("existing_file.json")
        self.assertEqual(result, {"key": "value"})

        # Test loading a non-existing JSON file
        mock_load_json.side_effect = FileNotFoundError()
        with self.assertRaises(FileNotFoundError):
            self.header._Header__load_json("non_existing_file.json")

        # Test loading a file with invalid JSON
        mock_load_json.side_effect = json.JSONDecodeError('Invalid JSON',
                                                          doc='', pos=0
                                                          )
        with self.assertRaises(json.JSONDecodeError):
            self.header._Header__load_json("invalid_json_file.json")

        # Test loading a JSON file that does not exist in the templates
        mock_load_json.side_effect = (
                simple_header.exceptions.TemplateNotFoundError())
        with self.assertRaises(simple_header.exceptions.TemplateNotFoundError):
            self.header._Header__load_json("non_existing_template.json")

    @patch('simple_header.core.LOGGER')
    def test_load_json_exception(self, mock_logger):
        with self.assertRaises(simple_header.exceptions.TemplateNotFoundError):
            # Load a non-existent JSON file.
            self.header._Header__load_json('non_existent_file.json')

        mock_logger.error.assert_called_once()

    @patch('simple_header.core.Header._Header__load_json')
    def test_detect_language(self, mock_load_json):
        # Mock the __load_json method to return a specific referer json
        mock_load_json.return_value = {"com": ["en-US"], "de": ["de-DE"]}

        # Test detecting language from a URL with a .com TLD
        result = self.header._Header__detect_language(
                "https://www.example.com"
                )
        self.assertEqual(result, "en-US")

        # Test detecting language from a URL with a .de TLD
        result = self.header._Header__detect_language(
                "https://www.example.de"
                )
        self.assertEqual(result, "de-DE")

        # Test detecting language from a URL with a TLD that is not in the
        # referer json
        result = self.header._Header__detect_language(
                "https://www.example.fr"
                )
        self.assertEqual(result, "en-US")  # Should fallback to 'en-US'

    def test_check_language(self):
        # Test language code without country code
        result = self.header._Header__check_language("http://example.com",
                                                     "en"
                                                     )
        self.assertEqual(result, "en-US")

        # Test no dash in language code
        result = self.header._Header__check_language("http://example.com",
                                                     "enUS"
                                                     )
        self.assertEqual(result, "en-US")

    @patch('simple_header.core.LOGGER')
    def test_check_language_warning(self, mock_logger):
        # Test language code not recognized or supported
        result = self.header._Header__check_language("http://example.com",
                                                     "abc"
                                                     )
        self.assertEqual(result, "en-US")
        mock_logger.warning.assert_called_once_with(
                "Language code 'abc' is not recognized or "
                "unsupported! Falling back to default language "
                "'en-US'."
                )

    @patch('simple_header.core.Header._Header__load_json')
    def test_check_language2(self, mock_load_json):
        # Mock the __load_json method to return a specific referer json
        mock_load_json.return_value = {"com": ["en-US"], "de": ["de-DE"]}

        # Test checking a supported language
        result = self.header._Header__check_language(self.url, "en-US")
        self.assertEqual(result, "en-US")

        # Test checking a language that is not supported
        result = self.header._Header__check_language(self.url, "fr-FR")
        self.assertEqual(result, "en-US")  # Should fall back to 'en-US'

        # Test checking a language that is not in the referer json
        result = self.header._Header__check_language(self.url, "es-ES")
        self.assertEqual(result, "en-US")  # Should fall back to 'en-US'

        # Test auto-detecting the language from the TLD of the url
        result = self.header._Header__check_language(
                "https://www.example.de"
                )
        self.assertEqual(result, "de-DE")

    def test_check_user_agent(self):
        # Test checking a supported user agent
        result = self.header._Header__check_user_agent(
                simple_header.sua.UserAgent(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 ("
                        "KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                        )
                )
        self.assertIsInstance(result, simple_header.sua.UserAgent)

        # Test checking a user agent that is not supported
        with self.assertLogs('simple_header.core', level='WARNING') as cm:
            result = self.header._Header__check_user_agent(12345)
            self.assertIsInstance(result, simple_header.sua.UserAgent)

        # Test checking a user agent that is not in the referer json
        result = self.header._Header__check_user_agent(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 ("
                "KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                )
        self.assertIsInstance(result, simple_header.sua.UserAgent)

        # Test auto-detecting the user agent from the TLD of the url
        result = self.header._Header__check_user_agent(None)
        self.assertIsInstance(result, simple_header.sua.UserAgent)

    def test_host(self):
        # Test extracting host from a URL with http protocol
        result = self.header._Header__host("http://www.example.com")
        self.assertEqual(result, "www.example.com")

        # Test extracting host from a URL with https protocol
        result = self.header._Header__host("https://www.example.com")
        self.assertEqual(result, "www.example.com")

        # Test extracting host from a URL without www
        result = self.header._Header__host("https://example.com")
        self.assertEqual(result, "example.com")

        # Test extracting host from a URL with path
        result = self.header._Header__host("https://www.example.com/path")
        self.assertEqual(result, "www.example.com")

        # Test extracting host from a URL with query parameters
        result = self.header._Header__host(
                "https://www.example.com/path?param=value"
                )
        self.assertEqual(result, "www.example.com")

        # Test extracting host from a URL with fragment
        result = self.header._Header__host(
                "https://www.example.com/path#fragment"
                )
        self.assertEqual(result, "www.example.com")

    @patch('simple_header.core.Header._Header__load_json')
    def test_referer(self, mock_load_json):
        # Mock the __load_json method to return the contents of the
        # referer_templates.json file
        mock_load_json.return_value = {
                "com": ["en-US", "https://google.com/",
                        "https://www.facebook.com/"],
                "com.au": ["en-AU", "https://google.com.au/",
                           "https://www.facebook.com.au/"],
                "de": ["de-DE", "https://google.de/",
                       "https://www.facebook.de/"]
                }

        # Test generating referer from a URL with a .com TLD
        result = self.header._Header__referer("https://www.example.com",
                                              "en-US"
                                              )
        self.assertIn("https://www.example.com/", result)
        self.assertIn("https://google.com/", result)
        self.assertIn("https://www.facebook.com/", result)

        # Test generating referer from a URL with a .com.au TLD
        result = self.header._Header__referer("https://www.example.com.au",
                                              "en-AU"
                                              )
        self.assertIn("https://www.example.com.au/", result)
        self.assertIn("https://google.com.au/", result)
        self.assertIn("https://www.facebook.com.au/", result)

        # Test generating referer from a URL with a .de TLD
        result = self.header._Header__referer("https://www.example.de",
                                              "de-DE"
                                              )
        self.assertIn("https://www.example.de/", result)
        self.assertIn("https://google.de/", result)
        self.assertIn("https://www.facebook.de/", result)

        # Test generating referer from a URL with a TLD that is not in the
        # referer json
        result = self.header._Header__referer("https://www.example.fr",
                                              "fr-FR"
                                              )
        self.assertIn("https://www.example.fr/", result)
        self.assertNotIn("https://google.fr/", result)
        self.assertNotIn("https://www.facebook.fr/", result)

    def test_upgrade_insecure_requests(self):
        # Test upgrading insecure requests from a URL with http protocol
        result = self.header._Header__upgrade_insecure_requests(
                "http://www.example.com"
                )
        self.assertEqual(result, "0")

        # Test upgrading insecure requests from a URL with https protocol
        result = self.header._Header__upgrade_insecure_requests(
                "https://www.example.com"
                )
        self.assertEqual(result, "1")

    def test_sec_ch_ua_chromium(self):
        # Test extracting Chromium version from a user agent with Chromium
        result = self.header._Header__sec_ch_ua_chromium(
                simple_header.sua.UserAgent(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 ("
                        "KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                        )
                )
        self.assertEqual(result, "58")

        # Test extracting Chromium version from a user agent without Chromium
        result = self.header._Header__sec_ch_ua_chromium(
                simple_header.sua.UserAgent(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 ("
                        "KHTML, like Gecko) Safari/537.3"
                        )
                )
        self.assertEqual(result, "")

        # Test extracting Chromium version from a user agent with a
        # different Chromium version
        result = self.header._Header__sec_ch_ua_chromium(
                simple_header.sua.UserAgent(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 ("
                        "KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.3"
                        )
                )
        self.assertEqual(result, "60")

    def test_sec_ch_ua(self):
        # Test generating Sec-Ch-Ua headers for a Chrome user agent
        result = self.header._Header__sec_ch_ua(simple_header.sua.UserAgent(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 ("
                "KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                )
                )
        self.assertEqual(result[0],
                         (
                                 '"Not A(Brand";v="99", "Chromium";v="58", '
                                 '"Google Chrome";v="58"')
                         )
        self.assertEqual(result[1], "?0")
        self.assertEqual(result[2], "Windows")

        # Test Sec-Ch-Ua headers for Firefox user agent (no Sec-Ch-Ua
        # headers)
        result = self.header._Header__sec_ch_ua(simple_header.sua.UserAgent(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) "
                "Gecko/20100101 Firefox/60.0"
                )
                )
        self.assertIsNone(result[0])
        self.assertEqual(result[1], None)
        self.assertEqual(result[2], None)

        # Test generating Sec-Ch-Ua headers for a Safari user agent
        result = self.header._Header__sec_ch_ua(simple_header.sua.UserAgent(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 "
                "Safari/605.1.15"
                )
                )
        self.assertIsNone(result[0])
        self.assertEqual(result[1], None)
        self.assertEqual(result[2], None)

        # Test Edge browser.
        edge_ua = simple_header.sua.parse(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 "
                "Safari/537.3 Edge/16.16299"
                )
        result = self.header._Header__sec_ch_ua(edge_ua)
        self.assertEqual(result[0],
                         '"Not A(Brand";v="99", "Microsoft '
                         'Edge";v="16", "Chromium";v="58"'
                         )

        # Test Whale browser.
        whale_ua = simple_header.sua.parse(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
                "Whale/3.24.223.21 Safari/537.36"
                )
        result = self.header._Header__sec_ch_ua(whale_ua)
        self.assertEqual(result[0],
                         '"Whale";v="3", "Not-A.Brand";v="8", '
                         '"Chromium";v="120"'
                         )

        # Test Opera browser.
        opera_ua = simple_header.sua.parse(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
                "Safari/537.36 OPR/106.0.0.0"
                )
        result = self.header._Header__sec_ch_ua(opera_ua)
        self.assertEqual(result[0],
                         '"Not_A Brand";v="8", "Chromium";v="120", '
                         '"Opera";v="106"'
                         )

        # Test QQ browser.
        qq_ua = simple_header.sua.parse(
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ("
                "KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 "
                "Core/1.94.192.400 QQBrowser/11.5.5250.400"
                )
        result = self.header._Header__sec_ch_ua(qq_ua)
        self.assertEqual(result[0],
                         '"Not A;Brand";v="11", "Chromium";v="94", '
                         '"QQ Browser";v="11"'
                         )

    def test_generate(self):
        # Setup.
        header = simple_header.Header(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                seed=self.seed,
                intra_site_nav=self.intra_site_nav,
                )

        # Test with all parameters provided
        header.generate(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                seed=self.seed,
                intra_site_nav=self.intra_site_nav,
                _internal=False
                )

        self.assertIsInstance(header.dict, dict)
        self.assertEqual(header.dict['Host'], self.host)
        self.assertEqual(header.dict['Connection'], self.connection)
        self.assertEqual(header.dict['Cache-Control'], self.cache_control)
        self.assertEqual(header.dict['Sec-Ch-Ua'], self.sec_ch_ua)
        self.assertEqual(header.dict['Sec-Ch-Ua-Mobile'],
                         self.sec_ch_ua_mobile
                         )
        self.assertEqual(header.dict['Sec-Ch-Ua-Platform'],
                         self.sec_ch_ua_platform
                         )
        self.assertEqual(header.dict['Upgrade-Insecure-Requests'],
                         self.upgrade_insecure_requests
                         )
        self.assertEqual(header.dict['User-Agent'],
                         self.user_agent_string
                         )
        self.assertEqual(header.dict['Accept'], self.accept)
        self.assertEqual(header.dict['Sec-Fetch-Site'],
                         self.sec_fetch_site
                         )
        self.assertEqual(header.dict['Sec-Fetch-Mode'],
                         self.sec_fetch_mode
                         )
        self.assertEqual(header.dict['Sec-Fetch-User'],
                         self.sec_fetch_user
                         )
        self.assertEqual(header.dict['Sec-Fetch-Dest'],
                         self.sec_fetch_dest
                         )
        self.assertEqual(header.dict['Accept-Encoding'],
                         self.accept_encoding
                         )
        self.assertEqual(header.dict['Accept-Language'],
                         self.accept_language
                         )

        # Test with no user_agent provided
        header.generate(
                url="https://www.example.com",
                language="en-US",
                user_agent=None,
                mobile=False,
                seed=1,
                intra_site_nav=True,
                _internal=False
                )
        self.assertIsInstance(header.dict, dict)
        self.assertIsNotNone(header.dict['User-Agent'])

        # Test with no language provided (test auto-detect).
        header.generate(
                url="https://www.example.com.au",
                language=None,
                user_agent=self.user_agent_string,
                mobile=False,
                seed=1,
                intra_site_nav=True,
                _internal=False
                )
        self.assertIsInstance(header.dict, dict)
        self.assertIsNotNone(header.dict['Accept-Language'])
        self.assertIn("en-AU", header.dict['Accept-Language'])

        # Test with mobile set to True, for testing sec_ch_ua we need
        # a Chrome browser.

        while True:
            mobile_ua = simple_header.sua.get(num=10,
                                              mobile=True,
                                              shuffle=True
                                              )[0]
            self.header_mobile = simple_header.Header(
                    url="https://www.example.com",
                    user_agent=mobile_ua,
                    seed=1,
                    )

            result_dict = self.header_mobile.generate(
                    url="https://www.example.com",
                    language="en-US",
                    user_agent=mobile_ua,
                    mobile=True,
                    seed=1,
                    intra_site_nav=True,
                    _internal=False
                    )

            if (self.header_mobile.user_agent.mobile and
                    self.header_mobile.user_agent.browser == "Chrome"
                    and self.header_mobile.user_agent.os != "iOS"):
                break

        self.assertIsInstance(result_dict, dict)
        self.assertEqual(self.header_mobile['Sec-Ch-Ua-Mobile'], "?1")
        self.assertEqual(result_dict['Sec-Ch-Ua-Mobile'], "?1")

        # Test with intra_site_nav set to False
        header.generate(
                url="https://www.example.com",
                language="en-US",
                user_agent=self.user_agent_string,
                mobile=False,
                seed=1,
                intra_site_nav=False,
                _internal=False
                )
        self.assertIsInstance(header.dict, dict)
        self.assertNotEqual(header.dict['Referer'],
                            "https://www.example.com/"
                            )

        # Test with intra_site_nav set to True, referer should be
        # the same as the url.
        header.generate(
                url="https://www.example.com",
                language="en-US",
                user_agent=self.user_agent_string,
                mobile=False,
                seed=1,
                intra_site_nav=True,
                _internal=False
                )
        self.assertIsInstance(header.dict, dict)
        self.assertEqual(header.dict['Referer'],
                         "https://www.example.com/"
                         )

    def test_generate_first_element(self):
        # Generate headers with seed=None to select the first element
        self.header.generate(
                url="http://example.com",
                language="en-US",
                user_agent="Mozilla/5.0",
                mobile=False,
                seed=None,
                intra_site_nav=False,
                _internal=False
                )
        # Check if the first element is selected for headers with multiple
        # options
        self.assertEqual(self.header.accept_encoding,
                         ['gzip, deflate', 'gzip, deflate, br']
                         )
        self.assertEqual(self.header.accept_language,
                         ['en-US,en;q=0.5', 'en-US,en;q=0.9']
                         )


class TestHeaders(unittest.TestCase):
    def setUp(self):
        self.headers = simple_header.Headers()
        self.url = "https://www.example.com"
        self.language = "en-US"
        self.mobile = False
        self.seed = 1
        self.intra_site_nav = True
        self.user_agent_string = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/110.0.0.0 Safari/537.36"
        )
        self.user_agent = simple_header.sua.parse(self.user_agent_string)

    def test_get_dict(self):
        # Test with all parameters provided
        result_dict = self.headers.get_dict(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                seed=self.seed,
                intra_site_nav=self.intra_site_nav
                )
        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict['Host'], 'www.example.com')
        self.assertEqual(result_dict['User-Agent'], self.user_agent_string)

        # Test with no user_agent provided
        result_dict = self.headers.get_dict(
                url="https://www.example.com",
                language="en-US",
                user_agent=None,
                mobile=False,
                seed=1,
                intra_site_nav=True
                )
        self.assertIsInstance(result_dict, dict)
        self.assertIsNotNone(result_dict['User-Agent'])

        # Test with no language provided (test auto-detect).
        result_dict = self.headers.get_dict(
                url="https://www.example.com.au",
                language=None,
                user_agent=self.user_agent_string,
                mobile=False,
                seed=1,
                intra_site_nav=True
                )
        self.assertIsInstance(result_dict, dict)
        self.assertIsNotNone(result_dict['Accept-Language'])
        self.assertIn("en-AU", result_dict['Accept-Language'])

        # Test with mobile set to True
        while True:
            mobile_ua = simple_header.sua.get(num=10,
                                              mobile=True,
                                              shuffle=True
                                              )[0]
            result_dict = self.headers.get_dict(
                    url="https://www.example.com",
                    language="en-US",
                    user_agent=mobile_ua,
                    mobile=True,
                    seed=1,
                    intra_site_nav=True
                    )
            if (mobile_ua.mobile and
                    mobile_ua.browser == "Chrome" and
                    mobile_ua.os != "iOS"):
                break
        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict['Sec-Ch-Ua-Mobile'], "?1")

        # Test with intra_site_nav set to False
        result_dict = self.headers.get_dict(
                url="https://www.example.com",
                language="en-US",
                user_agent=self.user_agent_string,
                mobile=False,
                seed=1,
                intra_site_nav=False
                )
        self.assertIsInstance(result_dict, dict)
        self.assertNotEqual(result_dict['Referer'], "https://www.example.com/")

        # Test with intra_site_nav set to True, referer should be the same
        # as the url.
        result_dict = self.headers.get_dict(
                url="https://www.example.com",
                language="en-US",
                user_agent=self.user_agent_string,
                mobile=False,
                seed=1,
                intra_site_nav=True
                )
        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict['Referer'], "https://www.example.com/")

    def test_get_list(self):
        # Test with all parameters provided
        result_list = self.headers.get_list(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                num=7,
                intra_site_nav=self.intra_site_nav
                )
        self.assertIsInstance(result_list, list)
        self.assertEqual(len(result_list), 7)
        self.assertIsInstance(result_list[0], simple_header.Header)
        self.assertEqual(result_list[0]['Host'], 'www.example.com')
        self.assertEqual(result_list[0]['User-Agent'],
                         self.user_agent
                         )
        self.assertEqual(result_list[0]['User-Agent'].string,
                         self.user_agent_string
                         )

        # Test with no user_agent provided
        result_list = self.headers.get_list(
                url="https://www.example.com",
                language="en-US",
                user_agent=None,
                mobile=False,
                num=1,
                intra_site_nav=True
                )
        self.assertIsInstance(result_list, list)
        self.assertEqual(len(result_list), 1)
        self.assertIsInstance(result_list[0], simple_header.Header)
        self.assertIsNotNone(result_list[0]['User-Agent'])

        # Test with no language provided (test auto-detect).
        result_list = self.headers.get_list(
                url="https://www.example.com.au",
                language=None,
                user_agent=self.user_agent_string,
                mobile=False,
                num=23,
                intra_site_nav=True
                )
        self.assertIsInstance(result_list, list)
        self.assertEqual(len(result_list), 23)
        self.assertIsInstance(result_list[0], simple_header.Header)
        self.assertIsNotNone(result_list[0]['Accept-Language'])
        self.assertIn("en-AU", result_list[0]['Accept-Language'][0])

        # Test with mobile set to True
        while True:
            mobile_ua = simple_header.sua.get(num=10,
                                              mobile=True,
                                              shuffle=True
                                              )[0]
            result_list = self.headers.get_list(
                    url="https://www.example.com",
                    language="en-US",
                    user_agent=mobile_ua,
                    mobile=True,
                    num=4,
                    intra_site_nav=True
                    )
            if (mobile_ua.mobile and
                    mobile_ua.browser == "Chrome" and
                    mobile_ua.os != "iOS"):
                break
        self.assertIsInstance(result_list, list)
        self.assertEqual(len(result_list), 4)
        self.assertIsInstance(result_list[0], simple_header.Header)
        self.assertEqual(result_list[0]['Sec-Ch-Ua-Mobile'], "?1")
        self.assertEqual(result_list[0].user_agent.mobile, True)
        self.assertEqual(result_list[0].user_agent.browser, "Chrome")
        self.assertNotEqual(result_list[0].user_agent.os, "iOS")

        # Test with intra_site_nav set to False
        result_list = self.headers.get_list(
                url="https://www.example.com",
                language="en-US",
                user_agent=self.user_agent_string,
                mobile=False,
                num=9,
                intra_site_nav=False
                )
        self.assertIsInstance(result_list, list)
        self.assertEqual(len(result_list), 9)
        self.assertIsInstance(result_list[0], simple_header.Header)
        self.assertNotEqual(result_list[0]['Referer'],
                            "https://www.example.com/"
                            )

        # Test with intra_site_nav set to True, referer should be the same
        # as the url. With maximal number of header combinations.
        result_list = self.headers.get_list(
                url="https://www.example.com",
                language="en-US",
                user_agent=self.user_agent_string,
                mobile=False,
                num=720,
                intra_site_nav=True
                )
        self.assertIsInstance(result_list, list)
        self.assertEqual(len(result_list), 720)
        self.assertIsInstance(result_list[0], simple_header.Header)
        self.assertEqual(result_list[0]['Referer'][0],
                         "https://www.example.com/"
                         )

    def test_get(self):
        # Test with all parameters provided
        result_header = self.headers.get(
                url=self.url,
                language=self.language,
                user_agent=self.user_agent,
                mobile=self.mobile,
                seed=self.seed,
                intra_site_nav=self.intra_site_nav
                )
        self.assertIsInstance(result_header, simple_header.Header)
        self.assertEqual(result_header.host, 'www.example.com')
        self.assertEqual(result_header.user_agent, self.user_agent)
        self.assertEqual(result_header.user_agent.string,
                         self.user_agent_string
                         )

        # Test with no user_agent provided
        result_header = self.headers.get(
                url="https://www.example.com",
                language="en-US",
                user_agent=None,
                mobile=False,
                seed=1,
                intra_site_nav=True
                )
        self.assertIsInstance(result_header, simple_header.Header)
        self.assertIsNotNone(result_header.user_agent)

        # Test with no language provided (test auto-detect).
        result_header = self.headers.get(
                url="https://www.example.com.au",
                language=None,
                user_agent=self.user_agent_string,
                mobile=False,
                seed=1,
                intra_site_nav=True
                )
        self.assertIsInstance(result_header, simple_header.Header)
        self.assertIsNotNone(result_header.accept_language)
        self.assertIn("en-AU", result_header.accept_language[0])

        # Test with mobile set to True
        while True:
            mobile_ua = simple_header.sua.get(num=10,
                                              mobile=True,
                                              shuffle=True
                                              )[0]
            result_header = self.headers.get(
                    url="https://www.example.com",
                    language="en-US",
                    user_agent=mobile_ua,
                    mobile=True,
                    seed=1,
                    intra_site_nav=True
                    )
            if (mobile_ua.mobile and
                    mobile_ua.browser == "Chrome" and
                    mobile_ua.os != "iOS"):
                break
        self.assertIsInstance(result_header, simple_header.Header)
        self.assertEqual(result_header.sec_ch_ua_mobile, "?1")

        # Test with intra_site_nav set to False
        result_header = self.headers.get(
                url="https://www.example.com",
                language="en-US",
                user_agent=self.user_agent_string,
                mobile=False,
                seed=1,
                intra_site_nav=False
                )
        self.assertIsInstance(result_header, simple_header.Header)
        self.assertNotEqual(result_header.referer, "https://www.example.com/")

        # Test with intra_site_nav set to True, referer should be the same
        # as the url.
        result_header = self.headers.get(
                url="https://www.example.com",
                language="en-US",
                user_agent=self.user_agent_string,
                mobile=False,
                seed=1,
                intra_site_nav=True
                )
        self.assertIsInstance(result_header, simple_header.Header)
        self.assertEqual(result_header.referer[0], "https://www.example.com/")


class LogListHandler(logging.Handler):
    """
    This class is used to capture log messages during the import of the
    package.
    """

    def __init__(self, *args, **kwargs):
        super(LogListHandler, self).__init__(*args, **kwargs)
        self.log = []

    def emit(self, record):
        self.log.append(self.format(record))


class TestPrintLogLeftover(unittest.TestCase):
    """
    This class tests if we forgot any print statements in the package or
    if there are any log messages during the import of the package.
    Works fully automatically, no need to modify the test when the
    package is modified or this code is reused in another package.

    The test is based on the following assumptions:
    - The package name is the same as the name of the folder in the 'src'
      folder.
    - The package is located in the 'src' folder.


    The test is based on the following exemplary directory structure:
    .
    ├── src
    │   └── simple_header
    │       ├── core.py
    │       └── ...
    └── tests
        └── test_core.py
    """

    @staticmethod
    def get_package_name():
        """
        Get the package name dynamically for importing.

        :return: The package name, e.g. 'simple_header.core'.
        :rtype: str
        """

        # Get the module name.
        module_name = __name__.split("_", maxsplit=1)[-1]

        # Get the package name.
        current_fp = Path(__file__).resolve()
        root_fp = current_fp.parent.parent
        src_subs = [f.name for f in (root_fp / "src").iterdir() if
                    f.is_dir()]

        return f"{src_subs[0]}.{module_name}"

    def import_package(self):
        """
        Import the package and reload it to ensure that the import of the
        package is successful.

        :return: None
        """

        # Re-Import the module dynamically
        imported_package = importlib.import_module(self.get_package_name())
        importlib.reload(imported_package)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_leftover(self, mock_stdout):
        """
        Test if there are any print statements left in the package.

        :param mock_stdout: Mocked or redirected standard output.
        :type mock_stdout: MagicMock
        :return: None
        """

        # Re-Import the package
        self.import_package()

        self.assertEqual(mock_stdout.getvalue(), "")

    def test_log_during_import(self):
        """
        Test if there are any log messages during the import of package.

        :return: None
        """

        # Create a logger.
        logger = logging.getLogger(self.get_package_name())
        logger.setLevel(logging.INFO)

        # Create our handler and add it to the logger.
        handler = LogListHandler()
        logger.addHandler(handler)

        # Re-Import the package.
        self.import_package()

        # Check if any logs were triggered.
        self.assertEqual(handler.log, [])
