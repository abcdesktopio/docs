# docs

## For More Information

Refer to the public documentation website:
* [https://abcdesktopio.github.io/](https://abcdesktopio.github.io/)
* [https://www.abcdesktop.io/](https://www.abcdesktop.io/)

## Documentation Markup Language

The abcdesktop.io documentation is built with [MkDocs](https://www.mkdocs.org/). Clone the repository including all submodules with the following command:

```
git clone --recurse-submodules https://github.com/abcdesktopio/docs
```

To build and serve the documentation website, run:

```
make install
make docs
```

To preview your local changes, install the Python dependencies and start the development server:

```
pip3 install -r requirements.txt
mkdocs serve
# open your browser: http://127.0.0.1:8000
```

Alternatively, from within the `docs` directory:

```
cd docs
pip3 install -r requirements.txt
mkdocs serve -f opsdocs/mkdocs.yml
```
