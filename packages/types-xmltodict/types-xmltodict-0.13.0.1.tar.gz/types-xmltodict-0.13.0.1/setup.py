from setuptools import setup

name = "types-xmltodict"
description = "Typing stubs for xmltodict"
long_description = '''
## Typing stubs for xmltodict

This is a PEP 561 type stub package for the `xmltodict` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `xmltodict`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/xmltodict. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `b8659e69f5bdc189091508b860378206107b44de`.
'''.lstrip()

setup(name=name,
      version="0.13.0.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/xmltodict.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['xmltodict-stubs'],
      package_data={'xmltodict-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
