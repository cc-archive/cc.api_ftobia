"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *

def js_wrap(html_output):
    lines = [l.strip() for l in html_output.split('\n')]
    wrapped_lines = ["document.write('" + l + "');" for l in lines
                             if l != '' ]
    return '\n'.join(wrapped_lines)
