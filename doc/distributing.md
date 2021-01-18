# Distributing

This package is a library intended to be uploaded to pypi and installed with pip or a similar tool (e.g. `pipenv`)

## How to distribute a new version

The procedure generally follows the steps of the [official packaging guide](https://packaging.python.org/tutorials/packaging-projects/).

The instructions above assume a compatible venv (python 3.7+) is activated.

### Install distribution tools

`pip install setuptools wheel twine`

### Prepare the package for distribution 

- bump the version in `version.txt` according to semantic versioning rules

### Build and upload to the index

- `python setup.py sdist bdist_wheel`
- `python -m twine upload dist/*`