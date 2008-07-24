import logging

from cc.api.lib.base import abort, request, BaseController

import cc.license

log = logging.getLogger(__name__)

class LicenseController(BaseController):

    def index(self, lclass, function):
        if lclass is None:
            abort(404)

        selectors = cc.license.selectors.list()
        if lclass not in selectors:
            return self.generate_error('invalidclass', 'Invalid License Class.')

        # get locale option
        try:
            locale = request.GET['locale']
        except KeyError:
            locale = 'en'

        # TODO handle function
        sel = cc.license.selectors.choose(lclass)

        # render and return
        tmpl = self.loader.load('license_questions.xml')
        stream = tmpl.generate(selector=sel,
                               locale=locale)
        return stream.render(method='xml')

