#!/bin/bash
set -e

CURRENT_DATETIME=$(date +"%s")
CURRENT_REPO=$(basename `git rev-parse --show-toplevel`)_web_ui
CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD | sed 's/\//_/g'`
CURRENT_COMMIT_HASH=`git log --pretty=format:"%h" -1`

earthly ${@} --max-remote-cache --build-arg CURRENT_DATETIME=$CURRENT_DATETIME --build-arg CURRENT_BRANCH=$CURRENT_BRANCH --build-arg CURRENT_COMMIT_HASH=$CURRENT_COMMIT_HASH --build-arg CURRENT_REPO=$CURRENT_REPO +base
earthly ${@} --max-remote-cache --build-arg CURRENT_DATETIME=$CURRENT_DATETIME --build-arg CURRENT_BRANCH=$CURRENT_BRANCH --build-arg CURRENT_COMMIT_HASH=$CURRENT_COMMIT_HASH --build-arg CURRENT_REPO=$CURRENT_REPO +tag-image

# Returns all images with the label buildtime=$CURRENT_DATETIME
docker image ls --filter "label=buildtime=$CURRENT_DATETIME" --format "{{.Repository}}:{{.Tag}}" | grep -v '_linux_' | xargs
