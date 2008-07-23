import logging

from cc.api.lib.base import request, BaseController
import cc.license

log = logging.getLogger(__name__)

# TODO: need to fix license.xml template to populate <html> appropriately
class DetailsController(BaseController):

    def index(self):
        if request.GET.has_key('license-uri'):
            uri = request.GET['license-uri']
        elif request.POST.has_key('license-uri'):
            uri = request.POST['license-uri']
        else:
            return self._generate_error('missingparam', 
                         'A value for license-uri must be supplied.')
        
        # XXX known issue: no general way of generically getting a
        # license from a URI, without going through a selector first
        sel = cc.license.selectors.choose('standard') # just use std for now
        try:
            license = sel.by_uri(uri)
        except cc.license.CCLicenseError:
            return self._generate_error('invalid', 'Invalid license uri.')

        return self.license2xml(license)

    def _generate_error(self, id, msg):
        tmpl = self.loader.load('error.xml')
        stream = tmpl.generate(id=id, msg=msg)
        return stream.render(method='xml')
