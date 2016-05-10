# -*- coding:utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.1b2'
description = 'A liveblogging solution for Plone.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='collective.liveblog',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        # 'Framework :: Plone :: 5.1',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: News/Diary',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone liveblogging dexterity',
    author='Simples Consutoria',
    author_email='produtos@simplesconsultoria.com.br',
    url='https://github.com/collective/collective.liveblog',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.dexterity',
        'plone.app.layout',
        'plone.app.textfield',
        'plone.batching',
        'plone.dexterity',
        'plone.memoize',
        'plone.namedfile [blobs]',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.annotation',
        'zope.component',
        'zope.container',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.lifecycleevent',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.testing',
            'Products.statusmessages',
            'robotsuite',
            'zope.viewlet',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
