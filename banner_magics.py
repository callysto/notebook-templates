#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Jupyter notebook magics (Python 3) to insert the Callysto banners

Use `%top_banner` and `%bottom_banner`, without backticks, in separate code cells
"""

from IPython.core.magic import register_line_magic
from IPython.display import SVG
from requests import get

raw_github_url = 'https://raw.githubusercontent.com/callysto/notebook-templates/master/'
top_banner_filename = 'callysto-notebook-top-banner-interactive.svg'
bottom_banner_filename = 'callysto-notebook-bottom-banner-interactive.svg'

@register_line_magic
def top_banner(line):
    r = get(raw_github_url + top_banner_filename)
    display(SVG(r.text))
    
@register_line_magic
def bottom_banner(line):
    r = get(raw_github_url + bottom_banner_filename)
    display(SVG(r.text))
