# hooks/toc_tab_filter.py
#
# Annote les headings situés dans des onglets (tabbed-set / pymdownx.tabbed)
# avec un attribut data-tab-path="Onglet|Sous-onglet".
#
# Le JS (wizard.js) lit cet attribut pour filtrer la TOC dynamiquement.
# Aucune dépendance externe : uniquement html.parser (stdlib Python).

from html.parser import HTMLParser
import html as html_mod


class _TabAnnotator(HTMLParser):
    """
    Parcourt le HTML une seule fois (O(n)).
    Maintient une pile des tabbed-set/tabbed-block rencontrés
    pour construire le chemin d'onglets de chaque heading.
    """

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.result = []          # fragments HTML reconstruits
        self._stack = []          # pile : éléments ouverts avec leur tag
        self._tab_stack = []      # pile : (label_text, block_index_actuel)
        self._set_stack = []      # pile par tabbed-set : {labels, block_idx}

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _current_tab_path(self):
        return "|".join(label for label, _ in self._tab_stack)

    def _attrs_str(self, attrs):
        parts = []
        for name, value in attrs:
            if value is None:
                parts.append(name)
            else:
                parts.append(f'{name}="{html_mod.escape(value, quote=True)}"')
        return (" " + " ".join(parts)) if parts else ""

    def _get_attr(self, attrs, name):
        for k, v in attrs:
            if k == name:
                return v
        return None

    def _has_class(self, attrs, cls):
        classes = (self._get_attr(attrs, "class") or "").split()
        return cls in classes

    # ------------------------------------------------------------------ #
    #  HTMLParser callbacks                                                #
    # ------------------------------------------------------------------ #

    def handle_starttag(self, tag, attrs):
        # ---- tabbed-set : on empile un contexte ----
        if tag == "div" and self._has_class(attrs, "tabbed-set"):
            self._set_stack.append({"labels": [], "block_idx": -1})
            self._stack.append(("tabbed-set", tag))
            self.result.append(f"<{tag}{self._attrs_str(attrs)}>")
            return

        # ---- label à l'intérieur d'un tabbed-set direct ----
        if tag == "label" and self._set_stack:
            # On mémorise le label ; son texte sera capturé dans handle_data
            self._set_stack[-1]["labels"].append("")
            self._stack.append(("label", tag))
            self.result.append(f"<{tag}{self._attrs_str(attrs)}>")
            return

        # ---- tabbed-content : contient les blocs ----
        if tag == "div" and self._has_class(attrs, "tabbed-content"):
            self._stack.append(("tabbed-content", tag))
            self.result.append(f"<{tag}{self._attrs_str(attrs)}>")
            return

        # ---- tabbed-block : on entre dans le contenu d'un onglet ----
        if tag == "div" and self._has_class(attrs, "tabbed-block"):
            if self._set_stack:
                ctx = self._set_stack[-1]
                ctx["block_idx"] += 1
                idx = ctx["block_idx"]
                labels = ctx["labels"]
                label = labels[idx] if idx < len(labels) else f"tab{idx}"
                self._tab_stack.append((label, idx))
            self._stack.append(("tabbed-block", tag))
            self.result.append(f"<{tag}{self._attrs_str(attrs)}>")
            return

        # ---- heading : injecter data-tab-path si dans un onglet ----
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            tab_path = self._current_tab_path()
            if tab_path:
                # Ajouter l'attribut seulement s'il n'est pas déjà là
                names = [k for k, _ in attrs]
                if "data-tab-path" not in names:
                    attrs = list(attrs) + [("data-tab-path", tab_path)]
            self._stack.append(("heading", tag))
            self.result.append(f"<{tag}{self._attrs_str(attrs)}>")
            return

        # ---- cas général ----
        self._stack.append(("other", tag))
        self.result.append(f"<{tag}{self._attrs_str(attrs)}>")

    def handle_endtag(self, tag):
        self.result.append(f"</{tag}>")
        if not self._stack:
            return
        kind, _ = self._stack[-1]
        self._stack.pop()

        if kind == "tabbed-set":
            self._set_stack.pop()
        elif kind == "tabbed-block":
            if self._tab_stack:
                self._tab_stack.pop()

    def handle_startendtag(self, tag, attrs):
        self.result.append(f"<{tag}{self._attrs_str(attrs)}/>")

    def handle_data(self, data):
        # Capture le texte des labels pour nommer les onglets
        if self._stack and self._stack[-1][0] == "label" and self._set_stack:
            self._set_stack[-1]["labels"][-1] += data
        self.result.append(data)

    def handle_entityref(self, name):
        self.result.append(f"&{name};")

    def handle_charref(self, name):
        self.result.append(f"&#{name};")

    def handle_comment(self, data):
        self.result.append(f"<!--{data}-->")

    def get_output(self):
        return "".join(self.result)


def on_page_content(html, page, config, **kwargs):
    annotator = _TabAnnotator()
    annotator.feed(html)
    return annotator.get_output()