import logging
import os

from cc.api.lib.base import BaseController
from genshi.template import TemplateLoader
import cc.license

log = logging.getLogger(__name__)

loader = TemplateLoader(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    auto_reload=True
)

class LocalesController(BaseController):

    def index(self):
        locales = cc.license.locales()
        tmpl = loader.load('locales.xml')
        stream = tmpl.generate(locales=locales)
        return stream.render(method='xml')#, doctype='xml')
