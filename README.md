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
