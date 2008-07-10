import logging
import os

from cc.api.lib.base import BaseController
from genshi.template import TemplateLoader
import cc.license

log = logging.getLogger(__name__)

# TODO: remove duplication of redefining template loader in every controller
loader = TemplateLoader(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    auto_reload=True
)

class ClassesController(BaseController):

    def index(self):
        lclasses = []
        # get list of selectors / license classes
        for lname in cc.license.selectors.list():
            lclasses.append(cc.license.selectors.choose(lname))

        # display them
        tmpl = loader.load('classes.xml')
        stream = tmpl.generate(lclasses=lclasses)
        return stream.render(method='xml')
