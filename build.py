#!/usr/bin/env python3

import markdown
from jinja2 import Template
from pathlib import Path

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

def make_rss(filenames):
    return _render_template('index.rss', filenames)

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
    meta['link'] = BASE_URL + Path(filename).relative_to(PUBLIC_DIR).as_posix()
    return meta

def write_rss_file():
    with open((PUBLIC_DIR / 'index.rss').as_posix(), 'w', encoding='utf8') as f:
        f.write(make_rss(list_md_files()))

if __name__ == '__main__':
    write_rss_file()
