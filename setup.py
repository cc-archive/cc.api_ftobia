try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='cc.api',
    version='0.01',
    description='Creative Commons license web API',
    classifiers=[],
    keywords='',
    author='Creative Commons',
    author_email='software@creativecommons.org',
    url='http://wiki.creativecommons.org/API',
    install_requires=[
                      'Pylons>=0.9.6.2',
                      'setuptools',
                      'zope.interface',
                      'nose',
                      'lxml',
                      'coverage',
                      'Genshi',
                      'cc.license',
                     ],
    packages=find_packages(exclude=['ez_setup','examples','tests']),
    include_package_data=True,
    test_suite='nose.collector',
    #package_data={'ccapi': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'ccapi': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = cc.api.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
