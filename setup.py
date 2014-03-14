from distutils.core import setup

setup(
    name='jaws-scraper',
    version='0.1.0',
    author='Louis Fogel',
    author_email='fogel@alexkarpinski.com',
    packages=['jaws',],
    scripts=[],
    url='https://github.com/iccelou91/JAWS',
    license='LICENSE.txt',
    description='Just Another Web Scraper.',
    long_description=open('README.md').read(),
    install_requires=[
        "mechanize==0.2.5",
        "requests==2.2.1",
    ],
)
