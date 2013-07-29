from setuptools import setup, find_packages
import os


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
]

setup(
    author="Eric Brelsford",
    author_email="eric@596acres.org",
    name='django-external-data-sync',
    description=('A simple Django app for periodically locally synchronizing '
                 'data that is stored externally.'),
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/596acres/django-external-data-sync/',
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.3.1',
    ],
    packages=find_packages(),
    include_package_data=True,
)
