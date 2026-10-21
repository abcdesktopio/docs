#!/usr/bin/env python3
"""Check www.abcdesktop.io for HTTP, rendering and content errors and write a Markdown report.

Usage:
    python3 scripts/check_site.py [--site URL] [--output report.md] [--external] [--skip-links]

Standard library only. Exit code is 1 when at least one check fails.
"""

import argparse
import datetime
import html
import json
import os
import re
import ssl
import struct
import sys
import time
import urllib.error
import urllib.parse as up
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36 abcdesktop-site-check'
PASS, WARN, FAIL = 'PASS', 'WARN', 'FAIL'
ICON = {PASS: '✅', WARN: '⚠️', FAIL: '❌'}


def ssl_context():
    # Python.org builds on macOS ship without a CA store; fall back to the system bundle.
    ctx = ssl.create_default_context()
    if not ctx.get_ca_certs() and os.path.exists('/etc/ssl/cert.pem'):
        ctx = ssl.create_default_context(cafile='/etc/ssl/cert.pem')
    return ctx


CTX = ssl_context()
_cache = {}


def fetch(url, method='GET', timeout=30):
    """Return (status, final_url, body_bytes, headers). Status 0 means a network error."""
    key = (url, method)
    if key in _cache:
        return _cache[key]
    req = urllib.request.Request(url, method=method, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            res = (r.status, r.geturl(), r.read() if method == 'GET' else b'', {k.lower(): v for k, v in r.headers.items()})
    except urllib.error.HTTPError as e:
        res = (e.code, url, b'', {})
    except Exception as e:  # network errors are reported, not raised
        res = (0, url, str(e).encode(), {})
    _cache[key] = res
    return res


def status_of(url, timeout=30):
    code = fetch(url, 'HEAD', timeout)[0]
    if not 200 <= code < 300:
        code = fetch(url, 'GET', timeout)[0]
    return code


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.imgs, self.heads = set(), [], [], []
        self.headings, self.text, self.mermaid = [], [], []
        self.title, self.meta = '', {}
        self._skip, self._in_title, self._in_article, self._h, self._mermaid = 0, False, False, None, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'a':
            if 'name' in a:
                self.ids.add(a['name'])
            if a.get('href') is not None:
                self.links.append(a['href'])
        if tag in ('img', 'script', 'iframe', 'source') and a.get('src'):
            self.links.append(a['src'])
        if tag == 'link':
            self.heads.append(a)
            if a.get('href') and a.get('rel') not in ('preconnect', 'dns-prefetch', 'alternate'):
                self.links.append(a['href'])
        if tag == 'meta':
            if a.get('name'):
                self.meta[a['name']] = a.get('content', '')
        if tag == 'img':
            self.imgs.append(a)
        if tag in ('pre', 'div') and 'mermaid' in (a.get('class') or '').split():
            self._mermaid = []
        if tag in ('script', 'style', 'code', 'pre'):
            self._skip += 1
        if tag == 'title':
            self._in_title = True
        if tag == 'article':
            self._in_article = True
        if re.fullmatch(r'h[1-6]', tag) and self._in_article:
            self._h = [int(tag[1]), '']

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'code', 'pre'):
            self._skip = max(0, self._skip - 1)
        if tag in ('pre', 'div') and self._mermaid is not None and self._skip == 0:
            self.mermaid.append(''.join(self._mermaid))
            self._mermaid = None
        if tag == 'title':
            self._in_title = False
        if tag == 'article':
            self._in_article = False
        if re.fullmatch(r'h[1-6]', tag) and self._h:
            self.headings.append((self._h[0], self._h[1].strip()))
            self._h = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._h is not None:
            self._h[1] += data
        if self._mermaid is not None:
            self._mermaid.append(data)
        if not self._skip and self._in_article:
            self.text.append(data)


def ico_sizes(data):
    if len(data) < 6 or data[:4] != b'\x00\x00\x01\x00':
        return None
    count = struct.unpack('<H', data[4:6])[0]
    sizes = []
    for i in range(count):
        w, h = data[6 + 16 * i], data[7 + 16 * i]
        sizes.append((w or 256, h or 256))
    return sorted(set(sizes))


def png_size(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return struct.unpack('>II', data[16:24])


class Report:
    def __init__(self):
        self.sections = []  # (title, [(status, name, details)])

    def section(self, title):
        self.sections.append((title, []))

    def add(self, status, name, details=''):
        self.sections[-1][1].append((status, name, details))
        print(f'[{status}] {name}' + (f' — {details.splitlines()[0][:120]}' if details else ''), flush=True)

    def counts(self):
        c = defaultdict(int)
        for _, items in self.sections:
            for s, _, _ in items:
                c[s] += 1
        return c

    def markdown(self, site, started, duration):
        c = self.counts()
        out = [f'# Site check report — {site}', '',
               f'- Date: {started:%Y-%m-%d %H:%M:%S}',
               f'- Duration: {duration:.0f} s',
               f'- Result: {ICON[PASS]} {c[PASS]} passed · {ICON[WARN]} {c[WARN]} warnings · {ICON[FAIL]} {c[FAIL]} failed', '']
        out += ['## Summary', '', '| Section | ✅ | ⚠️ | ❌ |', '|---|---|---|---|']
        for title, items in self.sections:
            sc = defaultdict(int)
            for s, _, _ in items:
                sc[s] += 1
            out.append(f'| [{title}](#{slug(title)}) | {sc[PASS]} | {sc[WARN]} | {sc[FAIL]} |')
        for title, items in self.sections:
            out += ['', f'## {title}', '', '| Status | Check | Details |', '|---|---|---|']
            for s, name, details in items:
                first = details.splitlines()[0] if details else ''
                out.append(f'| {ICON[s]} {s} | {md(name)} | {md(first)} |')
            long = [(name, d) for s, name, d in items if d and '\n' in d]
            for name, d in long:
                out += ['', f'<details><summary>{html.escape(name)}</summary>', '', '```text', d, '```', '', '</details>']
        return '\n'.join(out) + '\n'


def slug(t):
    return re.sub(r'[^a-z0-9 -]', '', t.lower()).strip().replace(' ', '-')


def md(s):
    return str(s).replace('|', '\\|').replace('<', '&lt;').replace('>', '&gt;').replace('\n', ' ')


def short(url, site):
    return url.replace(site, '') or '/'


def listing(items, limit=50):
    items = sorted(set(items))
    extra = f'\n… and {len(items) - limit} more' if len(items) > limit else ''
    return f'{len(items)} issue(s)\n' + '\n'.join(items[:limit]) + extra


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--site', default='https://www.abcdesktop.io')
    ap.add_argument('--output', default='site-check-report.md')
    ap.add_argument('--external', action='store_true', help='also check external links (slow, rate-limited by some hosts)')
    ap.add_argument('--skip-links', action='store_true', help='skip internal link status checks')
    args = ap.parse_args()
    site = args.site.rstrip('/')
    host = up.urlparse(site).netloc
    started, t0 = datetime.datetime.now(), time.time()
    rep = Report()

    # ── Pages ────────────────────────────────────────────────────────────────
    rep.section('Pages and sitemap')
    code, _, body, _ = fetch(site + '/sitemap.xml')
    pages = sorted(set(re.findall(r'<loc>([^<]+)</loc>', body.decode('utf-8', 'replace'))))
    rep.add(PASS if code == 200 and pages else FAIL, 'sitemap.xml', f'HTTP {code}, {len(pages)} pages')
    parsed, raw = {}, {}
    bad = []
    for u in pages:
        c, _, b, _ = fetch(u)
        if c != 200:
            bad.append(f'{c} {short(u, site)}')
        raw[u] = b.decode('utf-8', 'replace')
        p = Page()
        p.feed(raw[u])
        parsed[u] = p
    rep.add(FAIL if bad else PASS, 'All sitemap pages return 200', listing(bad) if bad else f'{len(pages)} pages')

    def page(path):
        return parsed.get(site + path), raw.get(site + path, '')

    # ── Root files ───────────────────────────────────────────────────────────
    rep.section('Root files and icons')
    c, _, b, _ = fetch(site + '/robots.txt')
    txt = b.decode('utf-8', 'replace')
    rep.add(PASS if c == 200 and 'Sitemap:' in txt else FAIL, '/robots.txt', f'HTTP {c}' + (', declares Sitemap' if 'Sitemap:' in txt else ''))
    c, _, b, _ = fetch(site + '/favicon.ico')
    sizes = ico_sizes(b) if c == 200 else None
    if c != 200 or not sizes:
        rep.add(FAIL, '/favicon.ico', f'HTTP {c}' + ('' if c != 200 else ', not a valid ICO'))
    else:
        missing = [s for s in (16, 32, 48) if (s, s) not in sizes]
        rep.add(WARN if missing else PASS, '/favicon.ico', f'sizes {sizes}' + (f', missing {missing}' if missing else ''))
    for path, want in (('/apple-touch-icon.png', (180, 180)), ('/android-chrome-192x192.png', (192, 192)), ('/android-chrome-512x512.png', (512, 512))):
        c, _, b, _ = fetch(site + path)
        size = png_size(b) if c == 200 else None
        rep.add(PASS if size == want else FAIL, path, f'HTTP {c}' + (f', {size[0]}x{size[1]}' if size else ''))
    c, _, b, _ = fetch(site + '/site.webmanifest')
    try:
        man = json.loads(b) if c == 200 else None
    except ValueError:
        man = None
    if not man:
        rep.add(FAIL, '/site.webmanifest', f'HTTP {c}' + (', invalid JSON' if c == 200 else ''))
    else:
        problems = []
        for icon in man.get('icons', []):
            ic, _, ib, _ = fetch(up.urljoin(site + '/site.webmanifest', icon['src']))
            sz = png_size(ib) if ic == 200 else None
            if not sz or f'{sz[0]}x{sz[1]}' != icon.get('sizes'):
                problems.append(f"{icon['src']} declared {icon.get('sizes')}, got HTTP {ic} {sz}")
        rep.add(FAIL if problems or not man.get('icons') else PASS, '/site.webmanifest icons resolve',
                '\n'.join(problems) or f"{len(man['icons'])} icon entries, theme_color {man.get('theme_color')}")

    # ── Head tags ────────────────────────────────────────────────────────────
    rep.section('Head tags on every page')
    alt, no_apple, no_manifest, no_theme, icon_hrefs = [], [], [], [], defaultdict(list)
    for u, p in parsed.items():
        rels = [(h.get('rel'), h.get('href')) for h in p.heads]
        if any(h.get('rel') == 'alternate' and h.get('hreflang') for h in p.heads):
            alt.append(short(u, site))
        if not any(r == 'apple-touch-icon' for r, _ in rels):
            no_apple.append(short(u, site))
        if not any(r == 'manifest' for r, _ in rels):
            no_manifest.append(short(u, site))
        if 'theme-color' not in p.meta:
            no_theme.append(short(u, site))
        for r, h in rels:
            if r == 'icon':
                icon_hrefs[up.urljoin(u, h)].append(short(u, site))
    rep.add(FAIL if alt else PASS, 'No hreflang rel="alternate" links (they trigger <page>/sitemap.xml 404s)', listing(alt) if alt else 'none found')
    rep.add(FAIL if no_apple else PASS, 'rel="apple-touch-icon" present', listing(no_apple) if no_apple else 'all pages')
    rep.add(FAIL if no_manifest else PASS, 'rel="manifest" present', listing(no_manifest) if no_manifest else 'all pages')
    rep.add(FAIL if no_theme else PASS, 'meta theme-color present', listing(no_theme) if no_theme else 'all pages')
    for href in icon_hrefs:
        c, _, b, _ = fetch(href)
        sizes = ico_sizes(b) if c == 200 else None
        if c != 200:
            rep.add(FAIL, f'Declared favicon {short(href, site)}', f'HTTP {c}')
        elif sizes and not {(16, 16), (32, 32)} <= set(sizes):
            rep.add(WARN, f'Declared favicon {short(href, site)}', f'sizes {sizes}: no 16/32 px image, consider favicon.ico')
        else:
            rep.add(PASS, f'Declared favicon {short(href, site)}', f'sizes {sizes or "n/a"}')

    # ── Session fixes ────────────────────────────────────────────────────────
    rep.section('Fixes applied during review')
    p, h = page('/install/4.4/applicationoverview/')
    ok = p and any(t == 'Application Catalog' for _, t in p.headings) and any('appList' in l for l in p.links)
    rep.add(PASS if ok else FAIL, 'Application overview has an "Application Catalog" section linking to the catalog')
    p, h = page('/contribute/4.4/services/pyos/')
    blocks = p.mermaid if p else []
    joined = '\n'.join(blocks)
    ok = bool(blocks) and 'node_kubernetesKubernetes' not in joined and 'node_kubernetes{{"Kubernetes Cluster"}}' in joined
    rep.add(PASS if ok else FAIL, 'pyos Mermaid diagram keeps the hexagon node (macros {% raw %})', f'{len(blocks)} mermaid block(s)')
    p, h = page('/ebook/ebook-abcdesktop-en/')
    jinja = bool(re.search(r'Macro (Syntax )?Error', h))
    rep.add(FAIL if jinja or not p else PASS, 'Ebook page renders without a macros/Jinja error')
    if p:
        toc = {up.urlparse(l).fragment for l in p.links if l.startswith('#') and len(l) > 1}
        missing = sorted(t for t in toc if t not in p.ids)
        rep.add(FAIL if missing else PASS, 'Ebook table-of-contents anchors resolve', ', '.join(missing) or f'{len(toc)} anchors')
    p, h = page('/advanced/4.4/applications/simplestapplicationxedit/')
    text = ' '.join(p.text) if p else ''
    rep.add(PASS if p and '```' not in text else FAIL, 'xedit page has no unrendered code fence')
    n = text.count('To generate the base64-encoded value')
    rep.add(PASS if n == 1 else WARN, 'xedit base64 instructions appear once', f'{n} occurrence(s)')
    p, h = page('/advanced/4.4/applications/templateapplication/')
    links = p.links if p else []
    old = [l for l in links if 'packages.ubuntu.com' in l and 'bionic' in l]
    new = [l for l in links if 'launchpad.net/ubuntu/' in l and '2048-qt' in l]
    rep.add(FAIL if old or not new else PASS, '2048 package link points to a maintained Ubuntu release', (new or old or ['no link'])[0])
    for l in new:
        c = status_of(l, 25)
        rep.add(PASS if 200 <= c < 300 else WARN, 'Launchpad 2048-qt page reachable', f'HTTP {c}')
    p, _ = page('/usecases/4.4/overview/')
    rep.add(FAIL if p and any('pyos/discussions' in l for l in p.links) else PASS, 'No link to disabled pyos GitHub Discussions')
    p, _ = page('/advanced/4.4/storage/overview/')
    q, _ = page('/advanced/4.4/authentication/overview/')
    rep.add(FAIL if p and q and p.title.strip() == q.title.strip() else PASS, 'Storage and authentication overviews have distinct titles')

    # ── Generic content checks ───────────────────────────────────────────────
    rep.section('Content and rendering (all pages)')
    issues = defaultdict(list)
    titles, links = defaultdict(list), defaultdict(set)
    for u, p in parsed.items():
        s, text = short(u, site), ' '.join(p.text)
        if re.search(r'Macro (Syntax )?Error|jinja2\.exceptions|UndefinedError', raw[u]):
            issues['Macros/Jinja error'].append(s)
        for m in set(re.findall(r'\{\{[^}]{0,80}\}\}|\{%[^%]{0,80}%\}', text)):
            issues['Unrendered macro in text'].append(f'{s}: {m}')
        for m in set(re.findall(r'!!!\s+\w+|\]\([^)\s]{1,120}\)|^#{1,6}\s\S|```', text, re.M)):
            issues['Unrendered Markdown'].append(f'{s}: {m.strip()[:60]}')
        prev = 1
        for lvl, t in p.headings:
            if lvl > prev + 1:
                issues['Heading level jump'].append(f'{s}: h{prev}->h{lvl} "{t[:50]}"')
            prev = lvl
        if p.headings and sum(1 for l, _ in p.headings if l == 1) != 1:
            issues['Page without exactly one H1'].append(s)
        if not p.meta.get('description'):
            issues['Missing meta description'].append(s)
        titles[p.title.strip()].append(s)
        for m in set(re.findall(r'''<(?:img|script|link|iframe|source)[^>]+(?:src|href)=["'](http://[^"']+)''', raw[u])):
            issues['Mixed content (http://)'].append(f'{s}: {m}')
        for img in p.imgs:
            if not img.get('alt'):
                issues['Image without alt'].append(f"{s}: {(img.get('src') or '')[:80]}")
        for l in p.links:
            l = l.strip()
            if not l or l.startswith(('mailto:', 'javascript:', 'data:', 'tel:')):
                continue
            a = up.urlparse(up.urljoin(u, l))
            if a.scheme not in ('http', 'https'):
                continue
            if a.hostname in ('localhost', '127.0.0.1'):
                issues['Link to localhost'].append(f'{s}: {l}')
                continue
            if a.netloc == host:
                if a.path.endswith('.md'):
                    issues['Unconverted .md link'].append(f'{s}: {l}')
                if a.fragment:
                    target = a._replace(fragment='').geturl()
                    tp = parsed.get(target) or parsed.get(target + '/')
                    if tp is not None and up.unquote(a.fragment) not in tp.ids:
                        issues['Broken anchor'].append(f'{s} -> {short(a.geturl(), site)}')
            links[a._replace(fragment='').geturl()].add(s)
    for t, us in titles.items():
        if len(us) > 1:
            issues['Duplicate <title>'].append(f'"{t[:60]}": ' + ', '.join(us))
    for name in ('Macros/Jinja error', 'Unrendered macro in text', 'Unrendered Markdown', 'Broken anchor', 'Unconverted .md link',
                 'Link to localhost', 'Mixed content (http://)', 'Duplicate <title>', 'Heading level jump', 'Page without exactly one H1',
                 'Missing meta description', 'Image without alt'):
        v = issues.get(name, [])
        severe = name in ('Macros/Jinja error', 'Unrendered Markdown', 'Broken anchor', 'Unconverted .md link', 'Link to localhost', 'Mixed content (http://)')
        rep.add(PASS if not v else (FAIL if severe else WARN), name, listing(v) if v else 'none')

    # ── Links ────────────────────────────────────────────────────────────────
    rep.section('Links')
    internal = {k: v for k, v in links.items() if up.urlparse(k).netloc == host}
    external = {k: v for k, v in links.items() if up.urlparse(k).netloc != host}
    if args.skip_links:
        rep.add(WARN, 'Internal links', 'skipped (--skip-links)')
    else:
        bad = []
        for k, refs in sorted(internal.items()):
            if k in parsed:
                continue
            c = status_of(k)
            if not 200 <= c < 300:
                bad.append(f'{c} {short(k, site)}  (on {", ".join(sorted(refs)[:3])})')
        rep.add(FAIL if bad else PASS, 'Internal links and resources', listing(bad) if bad else f'{len(internal)} URLs')
    if not args.external:
        rep.add(WARN, 'External links', f'{len(external)} URLs not checked (use --external)')
    else:
        bad, blocked = [], []
        for k, refs in sorted(external.items()):
            hostname = up.urlparse(k).hostname or ''
            if hostname in ('fonts.googleapis.com', 'fonts.gstatic.com') or '/edit/' in k:
                continue
            c = status_of(k, 20)
            if c == 429:
                time.sleep(5)
                _cache.pop((k, 'HEAD'), None)
                _cache.pop((k, 'GET'), None)
                c = status_of(k, 20)
            if hostname == 'github.com':
                time.sleep(1)
            line = f'{c} {k}  (on {", ".join(sorted(refs)[:3])})'
            if c in (401, 403, 429) or (c == 400 and 'facebook' in hostname):
                blocked.append(line)
            elif not 200 <= c < 300:
                bad.append(line)
        rep.add(FAIL if bad else PASS, 'External links', listing(bad) if bad else f'{len(external)} URLs')
        rep.add(WARN if blocked else PASS, 'External links blocked for bots / rate-limited (verify manually)', listing(blocked) if blocked else 'none')

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(rep.markdown(site, started, time.time() - t0))
    c = rep.counts()
    print(f'\nReport written to {args.output}: {c[PASS]} passed, {c[WARN]} warnings, {c[FAIL]} failed')
    return 1 if c[FAIL] else 0


if __name__ == '__main__':
    sys.exit(main())
