#!/bin/bash
builddate=$(git log -1 --format=%cd --date=iso)
lastcommit=$(git log -1 --format=%H)
version=$(git rev-list --count HEAD)
echo "{ \"date\": \"$builddate\", \"commit\": \"$lastcommit\", \"version\": \"$version\" }" > version.json
