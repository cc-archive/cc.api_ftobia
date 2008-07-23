import logging

from cc.api.lib.base import request, BaseController
import cc.license

log = logging.getLogger(__name__)

class DetailsController(BaseController):

    def index(self):
        if not request.GET.has_key('license-uri') and \
           not request.POST.has_key('license-uri'):
            return self._generate_error('missingparam', 
                         'A value for license-uri must be supplied.')

        return 'Hello, World!' # FIXME

    def _generate_error(self, id, msg):
        tmpl = self.loader.load('error.xml')
        stream = tmpl.generate(id=id, msg=msg)
        return stream.render(method='xml')
