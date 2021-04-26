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
html_theme = 'nature'
html_sidebars = {
    '**': ['globaltoc.html', 'searchbox.html'],
}
html_extra_path = ['_extra']
