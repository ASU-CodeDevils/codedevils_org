#!/bin/bash
#
# Utility to generate sphinx documentation and reconfigure for GitHub pages.
cd sphinx
make html
mv ../docs/html/* ../docs/
rm -rf ../docs/html
