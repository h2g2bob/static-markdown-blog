#!/usr/bin/env python3
import markdown
from jinja2 import Template
from pathlib import Path
import datetime

BASE_URL = 'https://dbatley.com/blog/'
PUBLIC_DIR = Path('./public')

def list_md_files():
    return [
        pth.as_posix()
        for pth in sorted(PUBLIC_DIR.glob('**/*.md'), reverse=True)]

def get_markdown(filename):
    md = markdown.Markdown(extensions=['meta', 'fenced_code'])
    with open(filename, 'r', encoding='utf8') as fd:
        html = md.convert(fd.read())
    meta = {key: value for key, [value] in md.Meta.items()}
    return (meta, html)

def write_rss_file():
    filenames = list_md_files()
    with open((PUBLIC_DIR / 'index.rss').as_posix(), 'w', encoding='utf8') as f:
        f.write(_render_template('index.rss', filenames))

def write_index_file():
    filenames = list_md_files()
    with open((PUBLIC_DIR / 'index.html').as_posix(), 'w', encoding='utf8') as f:
        f.write(_render_template('index.html', filenames))

def _render_template(template_name, filenames):
    with open('templates/' + template_name, 'r') as f:
        template = Template(f.read())

    context = {
        'items': [
            _meta_for_filename(filename)
            for filename in filenames]}
    return template.render(context)

def _meta_for_filename(filename):
    meta, _html = get_markdown(filename)

    md_link = Path(filename).relative_to(PUBLIC_DIR).as_posix()
    html_link = md_link.replace(".md", ".html")
    meta['relurl'] = html_link
    meta['fullurl'] = BASE_URL + html_link

    pubdate = datetime.datetime.strptime(meta['date'], '%Y-%m-%d').date()
    meta['rfc822'] = pubdate.strftime('%a, %02d %m %Y 00:00:00 GMT')

    return meta

if __name__ == '__main__':
    write_rss_file()
    write_index_file()
