"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render

from genshi.template import TemplateLoader
import os

import cc.api.lib.helpers as h
import cc.api.model as model

class BaseController(WSGIController):

    def __init__(self):
        self.loader = TemplateLoader(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                         'templates'),
            auto_reload=True
        )

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        return WSGIController.__call__(self, environ, start_response)

    # TODO: add support for jurisdictions
    def license2xml(self, license, locale='en'):
        """Turn a cc.license.License object into XML"""
        tmpl = self.loader.load('license.xml')
        stream = tmpl.generate(license=license,
                               locale=locale)
        return stream.render(method='xml')

    def generate_error(self, id, msg):
        tmpl = self.loader.load('error.xml')
        stream = tmpl.generate(id=id, msg=msg)
        return stream.render(method='xml')


# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
