# docs
abcdesktopio documentation files markup language

abcdesktop use mkdocs tools

```
git clone git://github.com/abcdesktopio/docs.git
cd docs
git submodule update --init --recursive --remote
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

