import logging

from cc.api.lib.base import abort, request, BaseController
from cc.api.lib.helpers import js_wrap

import cc.license

log = logging.getLogger(__name__)

class SimpleController(BaseController):

    def index(self):
        abort(404) # XXX what should the behavior be?

    
    def chooser(self):

        # jurisdiction option
        try:
            jurisdiction = request.GET['jurisdiction']
        except KeyError:
            jurisdiction = None

        # TODO: handle case of invalid jurisdiction

        # FIXME TEMPORARY
        licenses = []
        std = cc.license.selectors.choose('standard')
        for c in ('by','by-sa','by-nc','by-nd','by-nc-sa','by-nc-nd'):
            licenses.append( std.by_code(c, jurisdiction=jurisdiction) )

        # exclude option
        try:
            exclude = request.GET['exclude']
            for l in licenses:
                if exclude in l.uri:
                    licenses.remove(l)
        except KeyError:
            pass # don't exclude anything :)

        # locale option
        try:
            lang = request.GET['locale']
            if lang not in cc.license.locales():
                lang = 'en' # unknown locale falls back to default
        except KeyError:
            lang = 'en'

        # select option
        strip = True
        select = None
        try:
            select = request.GET['select']
            # if it works, we don't strip the select line
            strip = False
        except KeyError:
            pass

        tmpl = self.loader.load('chooser_options.xml')
        stream = tmpl.generate(licenses=licenses,
                               lang=lang,
                               strip=strip,
                               name=select)
        return stream.render(method='xml')

    def javascript(self):
        return js_wrap(self.chooser())
