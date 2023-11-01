#!/bin/bash

# Simple script to build and install a python module
# Copyright 2023 Dandelion Systems <dandelion.systems@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

function print_usage() {
	echo ""
	echo "Usage: build_and_install REPOSITORY MODULE"
	echo ""
	echo "Where:"
	echo "	REPOSITORY	- either testpypi or pypi"
	echo "	MODULE 		- module name"
	echo ""
	echo "pyproject.toml file must be in the same directory as this script"
	echo ""
}

NUMARGS=$#
REPOSITORY=$1
MODULE=$2

if [ $NUMARGS -lt 2 ]; then
	print_usage
	exit 1
fi

case "$REPOSITORY" in
	"testpypi")
		echo "Building and uploading to testpypi.org"
		python3 -m build
		python3 -m twine upload --repository testpypi dist/*
		echo "Installing new package $MODULE"
		python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade $MODULE
		;;
	"pypi")
		echo "Building and uploading to pypi.org"
		python3 -m build
		python3 -m twine upload --repository pypi dist/*
		echo "Installing new package $MODULE"
		python3 -m pip install --index-url https://pypi.org/simple/ --no-deps --upgrade $MODULE
		;;
	*)
		print_usage
		exit 1
		;;
esac

