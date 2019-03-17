#!/usr/bin/env python3

import markdown
from lxml import etree
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
    root = etree.Element('rss', attrib={'version': '2.0'})
    channel = etree.SubElement(root, 'channel')

    etree.SubElement(channel, 'title').text = 'h2g2bob\'s blog'

    for filename in filenames:
        item = etree.SubElement(channel, 'item')
        _populate_rss_item(item, filename)

    return etree.tostring(root, xml_declaration=True, encoding='UTF-8')

def _populate_rss_item(item, filename):
    meta, _html = get_markdown(filename)

    etree.SubElement(item, 'title').text = meta['title']
    etree.SubElement(item, 'description').text = meta['description']
    etree.SubElement(item, 'pubDate').text = meta['date']
    etree.SubElement(item, 'link').text = BASE_URL + Path(filename).relative_to(PUBLIC_DIR).as_posix()

def write_rss_file():
    with open((PUBLIC_DIR / 'index.rss').as_posix(), 'wb') as f:
        f.write(make_rss(list_md_files()))

if __name__ == '__main__':
    write_rss_file()
