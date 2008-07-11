import logging
import os

from cc.api.lib.base import BaseController
import cc.license

log = logging.getLogger(__name__)

class LocalesController(BaseController):

    def index(self):
        locales = cc.license.locales()
        tmpl = self.loader.load('locales.xml')
        stream = tmpl.generate(locales=locales)
        return stream.render(method='xml')
