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

- `rm dist/*`
- `python setup.py sdist bdist_wheel`
- `python -m twine upload dist/*`
  - for testing `python -m twine upload --repository testpypi dist/*`

### Installing the package

just run `pip install py_headless_daw`, this will install the latest version uploaded to the main pypi

if you want to install from testpypi, the command changes to
`pip install --upgrade --index-url https://test.pypi.org/simple/ py_headless_daw`
  
#### Known issue with uploading to testpypi
`numpy` is a dependency of this library. When installing from `testpypi` as described above, somehow it has been seen to require compiling `numpy` from scratch which takes a lot of time and often (so far, always) fails for some reason with some compilation errors.
Because of that, at the moment, I have not yet found a way to reliably install this package with dependencies from testpypi.

Instead, I upload new versions to main pypi which does not trigger this problem.


#### Upgrading

to upgrade the package, add `--upgrade` to your pip commands above, e.g. ` pip install --upgrade py_headless_daw`