#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime

AUTHOR = "Helmut Irle"
SITENAME = "Helmut.dev"
SITETITLE = "Helmut.dev"
SITESUBTITLE = "Better code"
SITEURL = "https://www.helmut.dev"
SITELOGO = "/images/me.jpg"

PATH = "content"
THEME = "Flex"

TIMEZONE = "Africa/Johannesburg"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MAIN_MENU = True
MENUITEMS = (
    ("Better Python", "/category/better-python.html"),
    ("Better Django", "/category/better-django.html"),
)

# Blogroll
LINKS = (
    ("Sequel Sermon", "https://sequelsermon.com"),
)

# Social widget
SOCIAL = (
    ("github", "https://www.github.com/psyonara"),
    ("twitter", "https://www.twitter.com/psyonara"),
)

DEFAULT_PAGINATION = 5
SUMMARY_MAX_LENGTH = 100

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["sitemap"]

SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.7,
        "pages": 0.5,
        "indexes": 0.6,
    },
    "changefreqs": {
        "articles": "monthly",
        "pages": "monthly",
        "indexes": "weekly",
    },
}

PYGMENTS_STYLE = "monokai"
COPYRIGHT_NAME = "Helmut.dev"
COPYRIGHT_YEAR = datetime.now().year

GOOGLE_ANALYTICS = "UA-172353205-1"
