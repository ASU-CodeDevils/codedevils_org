This folder contains all the static resources for the website.
The public directory is the directory used by DreamHost and
Phusion Passenger to serve static resources during deployment.
All folders (this one should be blocked by htaccess) are public.

DreamHost has a WebFTP feature that allows you to upload files
without having to use the shell. You should upload these files
to the public/static/dh directory. This directory is ignored
during git commits, and will help you avoid issues updating the
project.

All files in public/meda are ignored by default.