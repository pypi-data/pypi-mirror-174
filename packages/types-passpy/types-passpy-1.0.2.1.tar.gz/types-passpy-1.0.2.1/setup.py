from setuptools import setup

name = "types-passpy"
description = "Typing stubs for passpy"
long_description = '''
## Typing stubs for passpy

This is a PEP 561 type stub package for the `passpy` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `passpy`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/passpy. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `e7e94dd101276cbe69bde26524a4723bb0dcc7ac`.
'''.lstrip()

setup(name=name,
      version="1.0.2.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/passpy.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['passpy-stubs'],
      package_data={'passpy-stubs': ['__init__.pyi', 'exceptions.pyi', 'store.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
