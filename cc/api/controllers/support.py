import logging
import os

from cc.api.lib.base import request, BaseController
from cc.api.lib.helpers import js_wrap
import cc.license

log = logging.getLogger(__name__)

class SupportController(BaseController):

    def index(self):
        abort(404) # XXX what should the behavior be?

    def jurisdictions(self):
        jurisdictions = cc.license.jurisdictions.list()

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

        tmpl = self.loader.load('options.xml')
        stream = tmpl.generate(jurisdictions=jurisdictions, 
                               lang=lang,
                               strip=strip,
                               name=select)
        return stream.render(method='xml')

    def javascript(self):
        return js_wrap(self.jurisdictions())
