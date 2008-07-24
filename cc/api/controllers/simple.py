import logging

from cc.api.lib.base import request, BaseController
from cc.api.lib.helpers import js_wrap

import cc.license

log = logging.getLogger(__name__)

class SimpleController(BaseController):

    def index(self):
        abort(404) # XXX what should the behavior be?

    
    def chooser(self):
        # FIXME TEMPORARY
        licenses = []
        std = cc.license.selectors.choose('standard')
        for c in ('by','by-sa','by-nc','by-nd','by-nc-sa','by-nc-nd'):
            licenses.append( std.by_code(c) )

        # TODO add jurisdiction support

        # locale option
        try:
            lang = request.GET['locale']
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
        return js_wrap(self.jurisdictions())
