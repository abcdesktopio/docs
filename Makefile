all: version docs

version:
	$(shell ./mkversion.sh)

install:
	pip3 install -r requirements.txt

docs:
	# $(MAKE) -C api/oc.user.18.04 docs
	# cp api/oc.user.18.04/composer/node/spawner-service/spawner-service.md opsdocs/docs/services
	# cp api/oc.user.18.04/composer/node/file-service/file-service.md opsdocs/docs/services
	
	# only to build md 
	# comment take too long time use cache 
	# $(MAKE) -C oc.apps docs
	cp oc.apps/*.md opsdocs/docs/applications
	ls -la opsdocs/docs/applications
	mkdir -p opsdocs/docs/applications/icons
	cp oc.apps/icons/* opsdocs/docs/applications/icons
	mkdocs build -f opsdocs/mkdocs.yml

serve: 
	mkdocs serve -a 0.0.0.0:8080 -f opsdocs/mkdocs.yml
