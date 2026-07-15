# eesyapi.py

## Contributing

### Building the code

In a BASH terminal:

```
py -m pip install --upgrade build
py -m build
```

### Running code within the package

To run the code as a package, first install it:

```
pip install --upgrade --force-reinstall "dist/eesyapi-0.1.0-py3-none-any.whl"
```

Note this may take a while if some virtual environment initialisation is needed. And you may need to restart your Python environment as well.

Then run it as normal:

```
import eesyapi
eesyapi.api_url()
```

### Running tests

Basic pytest tests have been added to check that some of the main functions run.

If pytest isn't yet installed, open a bash terminal and paste


py -m pip install pytest


Then run the tests from the project folder:


py -m pytest


To test get_publications, in a Bash terminal, paste : pytest tests/test_get_publications.py -v

The tests are located in the `tests` folder.

These tests are quite simple and mainly check that functions run and return something. some tests will fail depending on the data returned from the api