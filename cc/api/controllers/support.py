import logging
import os

from cc.api.lib.base import request, BaseController
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

    # TODO: implement all possible options
    def jurisdictions(self):
        jurisdictions = cc.license.jurisdictions()
        try:
            lang = request.GET['locale']
        except KeyError:
            lang = 'en'

        tmpl = loader.load('options.xml')
        stream = tmpl.generate(jurisdictions=jurisdictions, lang=lang)
        return stream.render(method='xml')
