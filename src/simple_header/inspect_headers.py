#!/usr/bin/env python3

"""
inspect_headers.py: Script to inspect the headers of incoming requests.

This script is a simple web server that prints the headers of incoming
requests. It is useful for inspecting the headers of a request sent by a
web scraper or a web browser, to check if your scraper is looking like a
legitimate web browser. The server is accessible from every device in
your local network, depending on your firewall settings. I recommend you
run this script in your terminal, and not in an IDE. You have to install
flask to run this script (pip install flask). Then just uncomment the
code below and run the script. Then open your web browser and enter the
URL of the server, which is printed in the terminal (127.0.0.1:5000).
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
# from flask import Flask, request
#
# app = Flask(__name__)
#
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     # Remove Origin, Content-Length and Type header.
#     headers_conv = dict(request.headers)
#     headers_conv.pop("Content-Length", None)
#     headers_conv.pop("Content-Type", None)
#     headers_conv.pop("Origin", None)
#
#     for key, value in headers_conv.items():
#         print(f"{key}:", value)
#
#     return "<br>".join(
#             list(map(lambda i: f"{i[0]}: {i[1]}", headers_conv.items()))
#             ) + """
#     <p><form method="POST"><input type="submit" name="submit"
#     value="Submit"></form></p>"""
#
#
# # I recommend you run this script in your terminal, and not in an IDE.
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)
