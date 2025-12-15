#!/bin/bash

# Simple script to build and install a python module
# Copyright 2023 Dandelion Systems <dandelion.systems@gmail.com>
# SPDX-License-Identifier: MIT

# Things to mind before running this script 
# 1. Make sure python3-build and twine packages are installed, if not - install them
# 2. twine requires pkginfo version =>1.10 otherwise this script will fail with 
#    InvalidDistribution error, see https://github.com/pypa/twine/issues/1070
# 3. Normally this module should be installen in a Python venv, but if this parameter
#    is omitted the script will attempt to install it system-wide
# 4. Install other dependencies in the same venv.
# 5. When using the testpypi repository, there may be a delay before the package 
#    becomes available for installation after it gets uploaded. So you may find you 
#    still get the old version of the package after successfuly uploading a new one.

function print_usage() {
	echo ""
	echo "Usage: ./build_and_install.sh REPOSITORY MODULE [VENV]"
	echo ""
	echo "Where:"
	echo "	REPOSITORY	- either testpypi or pypi"
	echo "	MODULE 		- module name"
	echo "	VENV 		- full path to Python venv"
	echo ""
	echo "pyproject.toml file must be in the same directory as this script."
	echo "The supplied MODULE name must match the 'name =' string in the "
	echo "[project] section of the pyproject.toml file. This requirement is"
	echo "just to double-check you are doing the right thing."
	echo ""
}

NUMARGS=$#
REPOSITORY=$1
MODULE=$2
VENV=$3

if [ $NUMARGS -lt 2 ]; then
	print_usage
	exit 1
fi

PROJECTNAME=$(cat pyproject.toml | tr '\n' ' ' | sed 's/^.*\[project\][[:space:]]*//' | sed 's/name[[:space:]]*=[[:space:]]*"//' | sed 's/".*//')

if [ "$PROJECTNAME" != "$MODULE" ]; then
	print_usage
	echo "Supplied module name '$MODULE' does not match project name '$PROJECTNAME' in the pyproject.toml file."
	echo ""
	exit 1
fi

if [ "$VENV" != "" ]; then
	source $VENV/bin/activate
fi

rm ./dist/$MODULE*

case "$REPOSITORY" in
	"testpypi")
		echo "Building and uploading to testpypi.org"
		python3 -m build
		python3 -m twine upload --repository testpypi dist/*
		echo "Installing new package $MODULE"
		pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade $MODULE
		;;
	"pypi")
		echo "Building and uploading to pypi.org"
		python3 -m build
		python3 -m twine upload --repository pypi dist/*
		echo "Installing new package $MODULE"
		pip install --index-url https://pypi.org/simple/ --no-deps --upgrade $MODULE
		;;
	*)
		print_usage
		exit 1
		;;
esac

