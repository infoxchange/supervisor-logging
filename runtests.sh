#!/bin/sh -e

coverage erase
coverage run -m unittest "$@"
coverage report
