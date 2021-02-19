# docs

## To get more informations

Please, read the public documentation web site:
* [https://www.abcdesktop.io](https://www.abcdesktop.io)
* [https://abcdesktopio.github.io/](https://abcdesktopio.github.io/)


## abcdesktopio documentation files markup language

abcdesktop use mkdocs

```
git clone --recurse-submodules https://github.com/abcdesktopio/docs
```

To run the documentation website

```
make install
make docs
make serve
```

or

```
cd docs
pip3 install -r requirements.txt
mkdocs serve -f opsdocs/mkdocs.yml
```

TODO:
add make test

