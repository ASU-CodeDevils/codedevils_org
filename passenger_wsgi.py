"""
This file is the WSGI module for Phusion Passenger (currently used on DreamHost).
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

VENV = "/home/codedevils_admin/.envs/codedevils.org/"
INTERP = VENV + "bin/python3"

# INTERP is present twice so that the new python interpreter
# knows the actual executable path
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# This allows easy placement of apps within the interior
# codedevils_org directory.
ROOT_DIR = Path(__file__).resolve(strict=True)
sys.path.append(str(ROOT_DIR / "codedevils_org"))

# add the project and virtual environment to the system path
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + "/codedevils.org")
sys.path.insert(0, VENV + "bin")
sys.path.insert(0, VENV + "lib/python3.7/site-packages")

# set the settings file
# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"

application = get_wsgi_application()
# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

# meta data
__author__ = "Kevin Shelley"
__copyright__ = "Copyright 2020, CodeDevils - An Arizona State University student organization"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "webmaster@codedevils.org"
