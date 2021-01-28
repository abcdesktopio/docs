# Documentation

## Version
The current documentation version is 0.1

## Location
This documentation is located at
[https://github.com/abcdesktopio/docs](https://github.com/abcdesktopio/docs)

### Installing Make
Install the Make package using apt-get
```
sudo apt-get install make
```

### Installing MkDocs

Install the mkdocs package using the ```Makefile```:

```
make install
```

```make install``` command runs :

* pip install mkdocs 
* pip install mkdocs-material

Make sure that the pip command is installed on you system.


## How to build the documentation

### Build documentation files
```
git clone https://github.com/abcdesktopio/docs
cd docs
make docs
INFO    -  Cleaning site directory 
INFO    -  Building documentation to directory: /home/alex/src/docs/opsdocs/site 
```

All HTML files are located in the building documentation directory

## How to view the documentation
### Serve documentation files
```
make serve
INFO    -  Serving on http://127.0.0.1:8000
INFO    -  Start watching changes
INFO    -  Start detecting changes
```

Now connect http://127.0.0.1:8000 with any Web Navigator to browse through the documentation.






