# docs/macros/snippets_first.py
import re
from pathlib import Path


def resolve_snippets(markdown, docs_dir):
    def replace_snippet(match):
        indent = match.group(1)          # espaces avant --8<--
        relative_path = match.group(2).strip().strip('"').strip("'")
        path = docs_dir / relative_path
        if path.exists():
            content = path.read_text(encoding="utf-8")
            # ré-indente chaque ligne du fragment
            indented = "\n".join(
                (indent + line) if line.strip() else line
                for line in content.splitlines()
            )
            return resolve_snippets(indented, docs_dir)
        return match.group(0)

    return re.sub(
        r'^([ \t]*)--8<--\s+["\']([^"\']+)["\']',
        replace_snippet,
        markdown,
        flags=re.MULTILINE,
    )


def define_env(env):
    pass


def on_pre_page_macros(env):
    docs_dir = Path(env.conf["docs_dir"])
    env.markdown = resolve_snippets(env.markdown, docs_dir)