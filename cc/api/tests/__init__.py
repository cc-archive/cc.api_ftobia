"""Pylons application test package

When the test runner finds and executes tests within this directory,
this file will be loaded to setup the test environment.

It registers the root directory of the project in sys.path and
pkg_resources, in case the project hasn't been installed with
setuptools. It also initializes the application via websetup (paster
setup-app) with the project's test.ini configuration file.
"""
import os
import sys
import random
import operator
import lxml
import lxml.etree
from StringIO import StringIO
from unittest import TestCase

import pkg_resources
import paste.fixture
import paste.script.appinstall
from paste.deploy import loadapp
from routes import url_for

__all__ = [
           'url_for',
           'TestController',
           'RELAX_PATH',
           'relax_validate',
          ]

RELAX_PATH = os.path.join(
                 os.path.abspath(os.curdir),
                 'cc', 'api', 'tests', 'schemata')
  # TODO: decide on a better way to create RELAX_PATH
TOO_MANY = 25
print RELAX_PATH

here_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.dirname(os.path.dirname(os.path.dirname(here_dir)))

sys.path.insert(0, conf_dir)
pkg_resources.working_set.add_entry(conf_dir)
pkg_resources.require('Paste')
pkg_resources.require('PasteScript')

test_file = os.path.join(conf_dir, 'test.ini')
cmd = paste.script.appinstall.SetupCommand('setup-app')
cmd.run([test_file])


def relax_validate(schema_filename, instance_buffer):
    """Validates xml string instance_buffer against RelaxNG schema 
       located in file schema_filename. By convention, schema_filename 
       is a constant defined in the test module. Schema files are 
       located in tests/schemata."""

    relaxng = lxml.etree.RelaxNG(lxml.etree.parse(schema_filename))
    instance = lxml.etree.parse(StringIO(instance_buffer))

    if not relaxng.validate(instance):
        print relaxng.error_log.last_error
        return False
    else:
        return True

class TestData:
    """Generates test data for use in exercising the CC API."""

    def __init__(self):
        """Configure app to query CC API. This is for using live,
           rather than canned, data."""
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = paste.fixture.TestApp(wsgiapp)

    def _permute(self, lists): #TODO: document function
        if lists:
            result = map(lambda i: (i,), lists[0])
            for list in lists[1:]:
                curr = []
                for item in list:
                    new = map(operator.add, result, [(item,)]*len(result))
                    curr[len(curr):] = new
                result = curr
        else:
            result = []
        return result

    def license_classes(self):
        return ['standard', 'publicdomain', 'recombo']

    def _field_enums(self, lclass):
        """Retrieve the license information for this class, and generate 
           a set of answers for use with testing."""
        enums = []
        if lclass == 'publicdomain':
            pass
        elif lclass == 'recombo':
            enums.append(('jurisdiction', ['', 'tw']))
                              # 'br' doesnt exist for 'ncsamplingplus'
            enums.append(('sampling', ['sampling', 'samplingplus',
                                       'ncsamplingplus']))
        else:
            enums.append(('jurisdiction', ['', 'us', 'de', 'uk']))
            enums.append(('commercial', ['y', 'n']))
            enums.append(('derivatives', ['y', 'sa', 'n']))
        return enums

    def locales(self, canned=True):
        """Return a list of supported locales.
        Can return canned data, or the list of locales that
        /locales returns."""
        locales = None
        if canned:
            locales = [
                        'en', # English
                        'de', # German
                        # 'he', # Hebrew TODO: fix html rtl formatting
                        'el', # Greek
                      ]
        else:
            res = app.get('/locales')
            locale_doc = lxml.etree.parse(StringIO(res.body))
            locales = [n for n in locale_doc.xpath('//locale/@id')
                                              if n not in ('he',)]
        return locales

    def params(self, lclass, canned=True):
        all_params = []
        all_answers = self._field_enums(lclass)
        all_locales = self.locales(canned)
        for ans_combo in self._permute([n[1] for n in all_answers]):
            for locale in all_locales:
                params = zip([n[0] for n in all_answers], ans_combo)
                params.append(('locale', locale))
                all_params.append(params)
        # thin out param list if there are too many
        if len(all_params) > TOO_MANY:
            r = random.Random(42) # deterministic b/c seeded w/ constant
            all_params = r.sample(all_params, TOO_MANY)
        return all_params

    # TODO: fix hackery
    def xml_answers(self, lclass):
        all_params = self.params(lclass)
        for params in all_params:
            answers_xml = lxml.etree.Element('answers')
            locale_node = lxml.etree.SubElement(answers_xml, 'locale')
            locale_node.text = [n[1] for n in params if n[0]=='locale'][0]
            class_node = lxml.etree.SubElement(answers_xml, 'license-%s' % lclass)
            for a in [n for n in params if n[0]!='locale']:
                a_node = lxml.etree.SubElement(class_node, a[0])
                a_node.text = a[1]
            yield lxml.etree.tostring(answers_xml)

    def query_string_answers(self, lclass):
        all_params = self.params(lclass)
        for params in all_params:
            param_strs = ['='.join(n) for n in params]
            result = '?' + '&'.join(param_strs)
            yield result


class TestController():
    """Base class of test classes for the CC API. Defines test fixture
       behavior for creating and destroying webtest.TestApp instance of 
       the WSGI server."""

    def __init__(self):
        self.data = TestData()
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = paste.fixture.TestApp(wsgiapp)

    def setUp(self):
        """Test fixture for nosetests:
           - sets up the WSGI app server
           - creates test data generator"""
        # all setup defined in __init__
        pass

    def tearDown(self):
        """Test fixture for nosetests:
           - tears down the WSGI app server"""
        pass

    def makexml(self, bodystr):
        """Wraps text in a root element and escapes some special characters
           so as to make non-conforming HTML into XML."""
        retval = bodystr.replace('&', '&amp;') # makes the xml parser choke
        retval = '<root>' + retval + '</root>' # b/c it's not valid xml
        return retval

