# eesyapi.py

## Contributing

### Building the code

In a BASH terminal:

```bash
py -m pip install --upgrade build
py -m build
```

### Running code within the package

To run the code as a package, first install it:

```bash
pip install --upgrade --force-reinstall "dist/eesyapi-0.1.0-py3-none-any.whl"
```

Note this may take a while if some virtual environment initialisation is needed. You may also need to restart your Python environment afterwards.

Then run it as normal:

```python
import eesyapi
eesyapi.api_url()
```

### Running tests

Basic pytest tests have been added to check that some of the main functions run.

If pytest is not yet installed, open a BASH terminal and run:

```bash
py -m pip install pytest
```

Then run the tests from the project folder:

```bash
py -m pytest
```

The tests are located in the `tests` folder.

These tests are quite simple and mainly check that functions run and return results. Some tests may fail depending on the data currently returned by the API.

### Building the documentation locally

The project uses MkDocs with the Bootstrap 4 theme to generate the documentation.

If MkDocs is not installed, install the required packages:

bash
py -m pip install mkdocs mkdocs-bootstrap4


From the project root, start the local documentation server:

bash
mkdocs serve


The documentation will then be available at:


http://127.0.0.1:8000


Any changes made to the documentation files will automatically be rebuilt and reflected in your browser.

