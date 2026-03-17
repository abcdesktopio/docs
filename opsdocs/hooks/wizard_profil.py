"""
wizard_profil.py — MkDocs hook
Injects <meta> tags into wizard pages so wizard.js can read
page.meta values without needing a separate API call:

  - <meta name="wiz-profile" content="admin">   on step pages
  - <meta name="wiz-overview" content="true">   on the overview page
"""

import re


def on_page_content(html, page, config, **kwargs):
    meta = page.meta or {}

    tags = []

    # Step pages: inject profile
    if meta.get('profile'):
        tags.append(f'<meta name="wiz-profile" content="{meta["profile"]}">')

    # Overview page: detect by absence of step + presence of tabbed profile tabs
    # We mark it via a custom meta key in frontmatter: wizard_overview: true
    if meta.get('wizard_overview'):
        tags.append('<meta name="wiz-overview" content="true">')

    if tags:
        html = '\n'.join(tags) + '\n' + html

    return html
