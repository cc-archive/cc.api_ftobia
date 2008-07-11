import logging
import os

from cc.api.lib.base import request, BaseController
from cc.api.lib.helpers import js_wrap
from genshi.template import TemplateLoader
import cc.license

log = logging.getLogger(__name__)

# TODO: do something about this code duplication!
loader = TemplateLoader(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    auto_reload=True
)

class SupportController(BaseController):

    def index(self):
        abort(404) # XXX what should the behavior be?

    def jurisdictions(self):
        jurisdictions = cc.license.jurisdictions()

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

        tmpl = loader.load('options.xml')
        stream = tmpl.generate(jurisdictions=jurisdictions, 
                               lang=lang,
                               strip=strip,
                               name=select)
        return stream.render(method='xml')

    def javascript(self):
        return js_wrap(self.jurisdictions())
