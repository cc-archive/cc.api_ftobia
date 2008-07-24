import logging
import os

from cc.api.lib.base import request, BaseController
import cc.license

log = logging.getLogger(__name__)

class ClassesController(BaseController):

    def index(self):
        lclasses = []
        # get list of selectors / license classes
        for lname in cc.license.selectors.list():
            lclasses.append(cc.license.selectors.choose(lname))

        # get locale option
        try:
            locale = request.GET['locale']
        except KeyError:
            locale = 'en'

        # display them
        tmpl = self.loader.load('classes.xml')
        stream = tmpl.generate(lclasses=lclasses,
                               locale=locale)
        return stream.render(method='xml')
