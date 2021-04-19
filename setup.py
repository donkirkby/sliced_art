"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup
from os import path
import sliced_art

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='sliced_art',
      version=sliced_art.__version__,
      description='a drawing puzzle',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/donkirkby/sliced_art',
      author='Don Kirkby',
      classifiers=[  # https://pypi.org/classifiers/
          'Development Status :: 3 - Alpha',
          'Intended Audience :: End Users/Desktop',
          'Topic :: Games/Entertainment',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.9'],
      keywords='puzzle art drawing',
      packages=['sliced_art'],
      install_requires=['PySide2'],
      extras_require={'dev': ['pytest',
                              'coverage']},
      entry_points={
          'gui_scripts': ['sliced_art=sliced_art.sliced_art:main']},
      project_urls={
          'Bug Reports': 'https://github.com/donkirkby/sliced_art/issues',
          'Source': 'https://github.com/donkirkby/sliced_art'})
