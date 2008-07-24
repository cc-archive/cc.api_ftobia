import logging
import lxml.etree
from StringIO import StringIO

from cc.api.lib.base import abort, request, BaseController

import cc.license

log = logging.getLogger(__name__)

class LicenseController(BaseController):

    def index(self, lclass, function):
        if lclass is None:
            abort(404)
        if function is not None and function not in ('get', 'issue'):
            abort(404)

        selectors = cc.license.selectors.list()
        if lclass not in selectors:
            return self.generate_error('invalidclass', 'Invalid License Class.')

        # get locale option
        try:
            locale = request.GET['locale']
        except KeyError:
            locale = 'en'

        sel = cc.license.selectors.choose(lclass)

        if function is None: # then return questions
            tmpl = self.loader.load('license_questions.xml')
            stream = tmpl.generate(selector=sel,
                                   locale=locale)
            return stream.render(method='xml')
        elif function == 'get': # grab answers from GET
            answers_dict = request.GET.copy() # no parsing to do
                                              # FIXME handle locale
        elif function == 'issue': # grab answers from POST
            try:
                xml_string = request.POST['answers']
            except KeyError:
                return self.generate_error('missingparam', 
                               'A value must be provided for answers.')

            root = lxml.etree.parse(StringIO(xml_string)).getroot()

            answers_element = root.find('license-%s' % lclass)
            if answers_element is None:
                return self.generate_error('missingparam',
                               'A value must be provided for answers.')

            answers_dict = {}
            for e in answers_element.getchildren():
                answers_dict[e.tag] = e.text

            # get locale
            locale = root.find('locale')
            if locale is None:
                locale = 'en'

        else:
            abort(500) # this should be unreachable

        lic = sel.by_answers(answers_dict) # TODO wrap in try
                                           # return error if broken

        # render license
        return self.license2xml(lic)
