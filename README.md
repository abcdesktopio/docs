# docs

## To get more informations

Please, read the public documentation web site:
* [https://abcdesktopio.github.io/](https://abcdesktopio.github.io/)
* [https://www.abcdesktop.io/](https://www.abcdesktop.io/)

## abcdesktopio documentation files markup language

abcdesktop use mkdocs

```
git clone --recurse-submodules https://github.com/abcdesktopio/docs
```

To run the documentation website

```
make install
make docs
```

To test your local changes

```
pip3 install -r requirements.txt
mkdocs serve
# open your browser: http://127.0.0.1:8000
```

or

```
cd docs
pip3 install -r requirements.txt
mkdocs serve -f opsdocs/mkdocs.yml
```
