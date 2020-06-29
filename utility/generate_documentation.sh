#!/bin/bash
#
# Utility to generate sphinx documentation and reconfigure for GitHub pages.
cd sphinx
make html
mv _build/html/* ../docs/
rm -rf _build
