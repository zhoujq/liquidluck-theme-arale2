from jinja2 import contextfilter


def same_category(posts, category):
    items = []
    for item in posts:
        if item.category == category:
            items.append(item)

    items = sorted(items, key=lambda o: o.order)
    return items


def first_category(posts, category):
    items = []
    for item in posts:
        if item.category == category:
            items.append(item)

    items = sorted(items, key=lambda o: o.order)
    if items:
        return items[0]
    return None


@contextfilter
def src_js(ctx, files):
    import os
    from liquidluck.options import g
    from liquidluck.utils import get_relative_base

    writer = ctx.get('writer')
    base = get_relative_base(writer['filepath'])
    src = os.path.abspath(os.path.join(g.source_directory, 'src'))

    dct = {}
    for f in files:
        f = os.path.abspath(f)
        name = f[len(src) + 1:]
        if src in f and name.endswith('.js') and '/' not in name:
            dct[name[:-3]] = '%s/src/%s' % (base, name)
    return dct


@contextfilter
def iframe(ctx, content):
    #: together with IframeWriter
    import re
    import os
    import logging
    from liquidluck.options import g
    from liquidluck.utils import get_relative_base
    writer = ctx.get('writer')
    base = get_relative_base(writer['filepath'])
    regex = ur'\[\[iframe:(\S*?)\]\]'

    def repl(m):
        key = m.group(1)
        item = g.resource['iframe'].get(key)
        h = ''
        if item:
            height = item.get('height')
            if height:
                h = 'height="%s"' % height
        else:
            logging.warn('Iframe not found: %s' % key)

        path, name = os.path.split(key)
        src = '%s/%s/iframe-%s.html' % (base, path, name.lower())
        return ('<div class="ff-iframe">'
                '<iframe src="%s" allowtransparency="true" '
                'frameborder="0" scrolling="0" %s></iframe>'
                '</div>'
               ) % (src, h)

    return re.sub(regex, repl, content)


def json_dumps(dct):
    try:
        import json
    except ImportError:
        import simplejson
        json = simplejson
    return json.dumps(dct)
