#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom markdown rendering with syntax highlighting support
"""

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension


def custom_markdownify(text):
    """
    Convert markdown to HTML with syntax highlighting and additional features.

    Args:
        text (str): Markdown text to convert

    Returns:
        str: HTML rendered text with syntax highlighting
    """
    md = markdown.Markdown(
        extensions=[
            FencedCodeExtension(),
            CodeHiliteExtension(
                css_class="highlight",
                linenums=False,
                guess_lang=True,
            ),
            TableExtension(),
            "markdown.extensions.extra",
        ]
    )
    return md.convert(text)
