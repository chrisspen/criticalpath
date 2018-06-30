#!/bin/bash
# CS 2017.4.14
# Only run pep8 checks on locally modified files.
# Note, this won't find files in directories that haven't been added to git's index,
# so be sure to run `git status` to review changes and `git add .` to add if appropriate.
FILES=`git status --porcelain | grep -E "*\.py$" | grep -v migration | grep -v "^D  " | grep -v "^ D " | grep -v "^R  " | awk '{print $2}'`
if [ -z "$FILES" ]
then
    echo "No Python changes detected."
else
    echo "Checking: $FILES"
    pylint --rcfile=pylint.rc $FILES
fi
