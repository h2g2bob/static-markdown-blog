#!/usr/bin/env python3
import markdown
from jinja2 import Template
from pathlib import Path
import datetime

BASE_URL = 'https://dbatley.com/blog/'
PUBLIC_DIR = Path('./public')

def all_md_files():
    return [
        _meta_for_filename(pth.as_posix())
        for pth in sorted(PUBLIC_DIR.glob('**/*.md'), reverse=True)]

def _get_markdown(filename):
    md = markdown.Markdown(extensions=['meta', 'fenced_code'])
    with open(filename, 'r', encoding='utf8') as fd:
        html = md.convert(fd.read())
    meta = {key: value for key, [value] in md.Meta.items()}
    return (meta, html)

def write_rss_file(mdfiles):
    with open((PUBLIC_DIR / 'index.rss').as_posix(), 'w', encoding='utf8') as f:
        f.write(_render_template('index.rss', mdfiles))

def write_index_file(mdfiles):
    with open((PUBLIC_DIR / 'index.html').as_posix(), 'w', encoding='utf8') as f:
        f.write(_render_template('index.html', mdfiles))

def _render_template(template_name, mdfiles):
    with open('templates/' + template_name, 'r') as f:
        template = Template(f.read())

    context = {'items': mdfiles}
    return template.render(context)

def write_blog_entry(mdfile):
    with open('templates/entry.html', 'r') as f:
        template = Template(f.read())

    context = {'item': mdfile}
    with open(mdfile['htmlfile'], 'w', encoding='utf8') as f:
        f.write(template.render(context))

def _meta_for_filename(filename):
    data = {}
    meta, html = _get_markdown(filename)

    data['mdfile'] = filename
    data['htmlfile'] = filename.replace(".md", ".html")

    md_link = Path(filename).relative_to(PUBLIC_DIR).as_posix()
    html_link = md_link.replace(".md", ".html")
    data['relurl'] = html_link
    data['fullurl'] = BASE_URL + html_link

    datestr = meta['date']
    pubdate = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
    data['date'] = datestr
    data['rfc822'] = pubdate.strftime('%a, %02d %b %Y 00:00:00 GMT')

    data['title'] = meta['title']
    data['description'] = meta['description']
    data['image'] = meta['image']
    data['html'] = html

    return data

def main():
    mdfiles = all_md_files()
    write_rss_file(mdfiles)
    write_index_file(mdfiles)
    for mdfile in mdfiles:
        write_blog_entry(mdfile)

if __name__ == '__main__':
    main()
