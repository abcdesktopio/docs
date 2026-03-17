"""
wizard_nav.py — MkDocs hook
Removes wizard sub-pages (step > 1) from the left navigation menu.
"""

import re
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page


def on_nav(nav, config, files, **kwargs):
    nav.items = _filter(nav.items)
    return nav


def _read_step(page):
    """Read 'step' from YAML frontmatter without loading the full page."""
    try:
        with open(page.file.abs_src_path, encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            fm = match.group(1)
            step_match = re.search(r'^\s*step\s*:\s*(\d+)', fm, re.MULTILINE)
            if step_match:
                return int(step_match.group(1))
    except Exception:
        pass
    return 1


def _filter(items):
    result = []
    for item in items:
        if isinstance(item, Section):
            item.children = _filter(item.children)
            result.append(item)
        elif isinstance(item, Page):
            if _read_step(item) <= 1:
                result.append(item)
        else:
            result.append(item)
    return result