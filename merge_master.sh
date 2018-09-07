#!/bin/bash
# file: merge_master.sh
git checkout master
git pull origin master
git merge develop
git push origin master
