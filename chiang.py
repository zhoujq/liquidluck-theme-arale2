#!/usr/bin/env python

import os
import logging
from liquidluck.writers.base import BaseWriter
from liquidluck.readers.base import Post
from liquidluck.options import g
try:
    import json
    _json_decode = json.loads
except ImportError:
    import simplejson
    _json_decode = simplejson.loads


class ChiangPost(Post):
    @property
    def template(self):
        if self.relative_filepath.lower() == 'history.md':
            return 'history.html'
        return 'post.html'

    @property
    def order(self):
        if self.relative_filepath == 'README.md':
            return 0
        return int(self.meta.get('order', 9))

    @property
    def category(self):
        cat = self.meta.get('category', None)
        if cat:
            return cat
        if self.relative_filepath == 'README.md':
            return 'docs'
        if self.folder:
            return self.folder.split(os.path.sep)[0]
        return ''

    @property
    def date(self):
        return self.updated

    @property
    def filename(self):
        name = self.meta.get('filename', None)
        if name:
            return name
        name = super(ChiangPost, self).filename.lower()
        if name == 'readme':
            return 'index'
        return name


class PackageWriter(BaseWriter):
    writer_name = 'package'

    def __init__(self):
        for f in os.listdir(os.path.join(g.source_directory)):
            if f.lower() == 'history.md':
                g.resource['history'] = True
            if f == 'tests':
                g.resource['tests'] = True

        path = os.path.join(g.source_directory, 'package.json')
        if os.path.exists(path):
            f = open(path)
            g.resource['package'] = _json_decode(f.read())
            f.close()
        else:
            g.resource['package'] = {}
            logging.warn('package.json not found.')

    def start(self):
        pass


class JasmineTestWriter(BaseWriter):
    writer_name = 'jasmine'

    def start(self):
        dest = os.path.join(g.output_directory, 'tests', 'runner.html')
        self.render({}, 'runner.html', dest)


class MochaTestWriter(BaseWriter):
    writer_name = 'mocha'

    def start(self):
        dest = os.path.join(g.output_directory, 'tests', 'runner.html')
        self.render({}, 'mocha-runner.html', dest)


class IframeWriter(BaseWriter):
    writer_name = 'iframe'

    def start(self):
        if 'iframe' not in g.resource:
            return
        items = g.resource['iframe']
        for key in items:
            path, name = os.path.split(key)
            dest = os.path.join(
                g.output_directory, path, 'iframe-' + name) + '.html'
            self.render({'iframe': items[key]}, 'iframe.html', dest)
