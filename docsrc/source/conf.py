# Path setup
import os
import sys
sys.path.insert(0, os.path.abspath('./../../discrevpy'))

# Project information
project = 'discrevpy'
copyright = '2021, snkas'
author = 'snkas'
release = '0.2.6'
language = 'en'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]
exclude_patterns = []

# Options for HTML output
html_theme = 'furo'
html_sidebars = {
    '**': [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html",
    ]
}
html_extra_path = ['_extra']
html_favicon = 'favicon_discrevpy.png'
